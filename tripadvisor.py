from vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup

class TripAdvisor:
	def __init__(self):
		self.id_to_rating = { 'bubble_00':0, 'bubble_05':0.5, 'bubble_10':1.0,
			'bubble_15':1.5, 'bubble_20':2.0, 'bubble_25':2.5, 'bubble_30':3.0, 
			'bubble_35':3.5, 'bubble_40':4.0, 'bubble_45':4.5, 'bubble_50':5.0 }
		self.sent =  SentimentIntensityAnalyzer()

	def sentiment(self, text):
		if str((self.sent.polarity_scores(text))['compound'])[0] == '-':
			return text.upper()
		else: return text

	def name(self, soup, source='trip'):
		x = soup.find('h1', class_='YeV2SlB6 propertyHeading')
		if x: return x.text
		else: return None

	def no_of_reviews(self, soup, source='trip'):
		x = soup.find('div', class_='ui_poi_review_rating')
		if x: return ((soup.find('div', class_='ui_poi_review_rating').text).split(' '))[0]
		else: return None

	def overall_score(self, soup, source='trip'):
		x = soup.find('div', class_='ui_poi_review_rating')
		if x:
			elem = x.find('span', class_='ui_bubble_rating')
			return self.id_to_rating[(elem['class'])[1]]
		else: return None

	def last_review_score(self, soup, source='trip'):
		last_rating = soup.find('div', class_='rating')
		if last_rating:
			return self.id_to_rating[((last_rating.find('span', class_='ui_bubble_rating'))['class'])[1]]
		else:
			return None

	def last_review_date(self, soup, source='trip'):
		last_rating = soup.find('div', class_='rating')
		if last_rating: return last_rating.find('span', class_='ratingDate')['title']
		else: return None

	def get_reviews(self, soup, source='trip'):
		reviews = []
		revs = soup.find_all('div', class_='review-container')
		if revs: 
			for x in revs:
				for y in x.find('div', class_='prw_rup prw_reviews_text_summary_hsx'):
					reviews.append(self.sentiment(y.text))
			return reviews[:5]
		else:
			return None

"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
"""