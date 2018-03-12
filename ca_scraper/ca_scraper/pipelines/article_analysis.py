# -*- coding: utf-8 -*-
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import ca_scraper.utils.RAKE
RAKE_STOPLIST = 'ca_scraper/utils/stoplists/SmartStoplist.txt'
import json
from scrapy.exceptions import DropItem
from ca_scraper.items import Article, Legislator, PressRelease
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
class ArticleAnalysisPipeline(object):
   sentiment_intensity_calc = SentimentIntensityAnalyzer()
   issues = [{"key":"immigration","label":"Immigration","keywords":["immigration","undocumented"],"bigrams":["illegal immigration"]},{"key":"social_security","label":"Social Security","keywords":["entitlements"],"bigrams":["social security"]},{"key":"education","label":"Education","keywords":["education"],"bigrams":["common core","higher education","student debt"]},{"key":"taxes","label":"Taxes","keywords":["tax"],"bigrams":["tax reform","income tax","capital gains","carried interest"]},{"key":"economy","label":"Economy","keywords":["economy","unemployment","jobs","trade"],"bigrams":[]},{"key":"same_sex_marriage","label":"Same-Sex Marriage","keywords":["marriage","same-sex"],"bigrams":[]},{"key":"health_care","label":"Health Care","keywords":["health","health-care","obamacare"],"bigrams":["health care","health insurance","affordable care act"]},{"key":"gun_control","label":"Gun Control","keywords":["gun"],"bigrams":["gun control","gun right","gun law"]},{"key":"climate_change","label":"Climate Change","keywords":["environment","climate","warming","energy","greenhouse","methane","oil","coal","atmosphere"],"bigrams":["climate change","global warming","carbon dioxide","greenhouse gas","fossil fuel","natural gas","solar power","wind power","natural resources"]},{"key":"foreign_policy","label":"Foreign Policy","keywords":[],"bigrams":["foreign policy","foreign affairs"]},{"key":"women_rights","label":"Women's Rights","keywords":["women","abortion"],"bigrams":["women's right"]},{"key":"government_reform","label":"Government Reform","keywords":["washington"],"bigrams":["government reform"]},{"key":"security","label":"Security","keywords":["security","terrorism","crime","al-qaeda","daesh","isil","isis","terrorist"],"bigrams":["national security","homeland security"]},{"key":"minorities","label":"Minorities","keywords":["race","racism","minority","minorities"],"bigrams":["civil rights"]},{"key":"minimum_wage","label":"Minimum Wage","keywords":["wage"],"bigrams":["minimum wage"]},{"key":"income_inequality","label":"Income Inequality","keywords":["wealth","poverty","homeless"],"bigrams":["income inequality","wage gap","income distribution"]},{"key":"lgbtq","label":"LGBTQ","keywords":["lgbt"],"bigrams":[]},{"key":"drugs","label":"Drugs","keywords":["overdose","drug","cocaine","weed","marijuana"],"bigrams":[]},{"key":"infrastructure","label":"Infrastructure","keywords":["infrastructure"],"bigrams":[]}]
   rake = ca_scraper.utils.RAKE.Rake(RAKE_STOPLIST, min_char_length=2, max_words_length=5)
   def process_item(self, item, spider):
      if isinstance(item, Article):
         return self.analyzeArticle(item, spider)
      elif isinstance(item, Legislator):
         return item
      elif isinstance(item, PressRelease):
         return item
   def analyzeArticle(self, item, spider):
      existing_issues, trigger_terms = self.find_issues(item.get('content'))
      if not trigger_terms:
         print('ITEM DROPPED')
         raise DropItem("Missing price in %s" % item)
      item['issues'] = json.dumps(existing_issues)
      analysis = TextBlob(item.get('content'))
      item['blob_keywords'] = json.dumps(analysis.noun_phrases)
      item['blob_sentiment'] = str(analysis.sentiment)
      #3: RAKE keywords for each page
      rake_results = self.rake.run(item.get('content'))
      item['rake_keywords'] = json.dumps(rake_results[:5])
      # 4 Sentiment
      item['nltk_sentiment'] = self.checkSentiment(item.get('content'))
      return item
   def checkSentiment(self, text):
      sentences = nltk.sent_tokenize(text)
      total_sentiment = 0
      for sentence in sentences:
         # example sentiment output: {'neu': 0.625, 'compound': 0.2023, 'neg': 0.0, 'pos': 0.375}
         sentence_sentiment = self.sentiment_intensity_calc.polarity_scores(sentence)
         total_sentiment += sentence_sentiment.get('compound')
      return total_sentiment
   def find_issues(self, text):
      existing_issues = []
      trigger_term = []
      for issue in self.issues:
         for keyword in (issue.get('bigrams') + issue.get('keywords')):
            keyword = keyword.lower()
            keyword_exists = keyword in text
            if keyword_exists:
               print(keyword)
               trigger_term.append(keyword)
               existing_issues.append(issue)
      return existing_issues, trigger_term
