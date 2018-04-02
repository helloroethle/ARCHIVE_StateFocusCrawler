from sqlalchemy.orm import sessionmaker
from ca_scraper.models import PressReleases, db_connect, Articles
from datetime import datetime
from sqlalchemy import and_
# Imports from article_analysis.py
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import ca_scraper.utils.RAKE
RAKE_STOPLIST = 'ca_scraper/utils/stoplists/SmartStoplist.txt'
import json
from textstat.textstat import textstat
word_tokenizer = nltk.tokenize.RegexpTokenizer("[\w']+")
english_stops = set(nltk.corpus.stopwords.words('english'))
issues = [{"key":"immigration","label":"Immigration","keywords":["immigration","undocumented"],"bigrams":["illegal immigration"]},{"key":"social_security","label":"Social Security","keywords":["entitlements"],"bigrams":["social security"]},{"key":"education","label":"Education","keywords":["education"],"bigrams":["common core","higher education","student debt"]},{"key":"taxes","label":"Taxes","keywords":["tax"],"bigrams":["tax reform","income tax","capital gains","carried interest"]},{"key":"economy","label":"Economy","keywords":["economy","unemployment","jobs","trade"],"bigrams":[]},{"key":"same_sex_marriage","label":"Same-Sex Marriage","keywords":["marriage","same-sex"],"bigrams":[]},{"key":"health_care","label":"Health Care","keywords":["health","health-care","obamacare"],"bigrams":["health care","health insurance","affordable care act"]},{"key":"gun_control","label":"Gun Control","keywords":["gun"],"bigrams":["gun control","gun right","gun law"]},{"key":"climate_change","label":"Climate Change","keywords":["environment","climate","warming","energy","greenhouse","methane","oil","coal","atmosphere"],"bigrams":["climate change","global warming","carbon dioxide","greenhouse gas","fossil fuel","natural gas","solar power","wind power","natural resources"]},{"key":"foreign_policy","label":"Foreign Policy","keywords":[],"bigrams":["foreign policy","foreign affairs"]},{"key":"women_rights","label":"Women's Rights","keywords":["women","abortion"],"bigrams":["women's right"]},{"key":"government_reform","label":"Government Reform","keywords":["washington"],"bigrams":["government reform"]},{"key":"security","label":"Security","keywords":["security","terrorism","crime","al-qaeda","daesh","isil","isis","terrorist"],"bigrams":["national security","homeland security"]},{"key":"minorities","label":"Minorities","keywords":["race","racism","minority","minorities"],"bigrams":["civil rights"]},{"key":"minimum_wage","label":"Minimum Wage","keywords":["wage"],"bigrams":["minimum wage"]},{"key":"income_inequality","label":"Income Inequality","keywords":["wealth","poverty","homeless"],"bigrams":["income inequality","wage gap","income distribution"]},{"key":"lgbtq","label":"LGBTQ","keywords":["lgbt"],"bigrams":[]},{"key":"drugs","label":"Drugs","keywords":["overdose","drug","cocaine","weed","marijuana"],"bigrams":[]},{"key":"infrastructure","label":"Infrastructure","keywords":["infrastructure"],"bigrams":[]}]
summary = { 'issues':{} }

# def run_press_release_readability():
#     # Connecting to the databse
#     engine = db_connect()
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     for press_release in session.query(PressReleases):
#         if press_release.content.strip():
#             press_release.readability = textstat.flesch_kincaid_grade(press_release.content)
#             try:
#                 session.add(press_release)
#                 session.commit()
#             except:
#                 session.rollback()

def run_document_analysis():
    # run_press_release_analysis()
    run_article_analysis()

def run_press_release_analysis():
    # Connecting to the databse
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    for press_release in session.query(PressReleases):
        press_release_analysis = DocumentAnalysis(press_release, True)
        press_release_analysis.analysis()
        try:
            session.add(press_release_analysis.document)
            session.commit()
        except:
            session.rollback()


def run_article_analysis():
    # Connecting to the databse
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    for article in session.query(Articles):
        articleAnalysis = DocumentAnalysis(article, False)
        articleAnalysis.analysis()
    results = {}
    for issue in issues:
        key = issue.get('key')
        if key in summary['issues']:
            content = summary['issues'][key].get('content')
            examples = summary['issues'][key].get('examples')
            readability = 0
            sentiment = 0
            for example in examples:
                readability += example.get('readability')
                sentiment += sentiment
            content_words = get_lowercase(get_words(content))
            word_count = len(content_words)
            unique_word_count = len(set(content_words))
            content_words_without_stopwords = remove_stop_words(content_words)
            word_frequency = nltk.FreqDist(content_words_without_stopwords).most_common(20)
            results[key] = {
                'word_count': word_count,
                'unique_word_count': unique_word_count,
                '20_most_frequent': word_frequency,
                'instances': len(examples),
                'readability': readability/len(examples),
                'sentiment': sentiment,
            }
    print(results)
        # try:
        #     session.add(articleAnalysis.document)
        #     session.commit()
        # except:
        #     session.rollback()


# UTILITY METHODS
def get_words(content):
  return word_tokenizer.tokenize(content)

def get_lowercase(words):
  return [w.lower() for w in words]

def remove_stop_words(words):
  return [word for word in words if word not in english_stops]

# Content from article analysis reworked
class DocumentAnalysis(object):
    sentiment_intensity_calc = SentimentIntensityAnalyzer()
    rake = ca_scraper.utils.RAKE.Rake(RAKE_STOPLIST, min_char_length=2, max_words_length=5)
    def __init__(self, document, is_press_release):
        self.document = document
    def analysis(self):
        # Find political issues in document
        existing_issues, trigger_terms = self._find_issues()
        self.document.issues = json.dumps(existing_issues)
        #  Get text frequency words and basic document stats
        content_words = get_lowercase(get_words(self.document.content))
        self.document.word_count = len(content_words)
        self.document.unique_word_count = len(set(content_words))
        content_words_without_stopwords = remove_stop_words(content_words)
        self.document.word_frequency = json.dumps(nltk.FreqDist(content_words_without_stopwords).most_common(10))
        # Run Textblob's document analysis to get sentiment and noun phrases
        analysis = TextBlob(self.document.content)
        self.document.blob_keywords = json.dumps(analysis.noun_phrases)
        self.document.blob_sentiment = str(analysis.sentiment)
        #3: RAKE keywords for each page
        rake_results = self.rake.run(self.document.content)
        self.document.rake_keywords = json.dumps(rake_results[:5])
        # 4 Sentiment
        self.document.nltk_sentiment = self._check_sentiment()
        # 5 Readability
        if self.document.content.strip():
            self.document.readability = textstat.flesch_kincaid_grade(self.document.content)
        # Update Summary Object with Issue Information
        for issue in existing_issues:
            key = issue.get('key')
            if key not in summary['issues']:
                summary['issues'][key] = { 'examples': [], 'content': ''}
            summary['issues'][key]['content'] += (' ' + self.document.content)
            summary['issues'][key]['examples'].append({
                'title': self.document.title,
                'word_count': self.document.word_count,
                'unique_word_count': self.document.unique_word_count,
                'sentiment': self.document.nltk_sentiment,
                'readability': self.document.readability
            })
    def _check_sentiment(self):
        sentences = nltk.sent_tokenize(self.document.content)
        total_sentiment = 0
        for sentence in sentences:
            # example sentiment output: {'neu': 0.625, 'compound': 0.2023, 'neg': 0.0, 'pos': 0.375}
            sentence_sentiment = self.sentiment_intensity_calc.polarity_scores(sentence)
            total_sentiment += sentence_sentiment.get('compound')
        return total_sentiment
    def _find_issues(self):
        text = self.document.content
        existing_issues = []
        trigger_term = []
        for issue in issues:
            for keyword in (issue.get('bigrams') + issue.get('keywords')):
                keyword = keyword.lower()
                keyword_exists = keyword in text
                if keyword_exists:
                    trigger_term.append(keyword)
                    existing_issues.append(issue)
        return existing_issues, trigger_term


if __name__ == "__main__":
    run_document_analysis()
