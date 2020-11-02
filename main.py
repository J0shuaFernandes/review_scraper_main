from bs4 import BeautifulSoup
from urllib.request import urlopen
from tripadvisor import TripAdvisor
from openpyxl import Workbook
import time

if __name__ == '__main__':
	trip = TripAdvisor()
	total = 0
	scraped, not_scraped = 0, 0

	input_file = input('Enter filename: ')
	output_file = input('Output Filename: ')

	if not input_file.endswith('.txt'):
		input_file = ''.join([f, '.txt'])

	if not output_file.endswith('.xlsx'):
		output_file = ''.join([output_file, '.xlsx'])

	f = open(input_file, 'r') # load links from text file into memory
	links = f.readlines()
	links = [x.replace('\n','') for x in links]
	f.close()

	wb = Workbook()
	ws = wb.active

	name = None
	overall_score, no_of_reviews = '0', '0'
	last_review_date, last_review_score = '0', '0'
	reviews = ['0', '0', '0', '0', '0']

	ws.append(['Name','Overall Score','No of Reviews','Last Review Date','Last Review Score','Review1','Review2','Review3','Review4','Review5'])
	row = [name, overall_score, no_of_reviews, last_review_date, last_review_score] + reviews	
	
	start = time.time() # start counting seconds 
	for x in links:
		total += 1
		soup = BeautifulSoup(urlopen(x).read(), 'lxml')

		if (soup.find('h1', class_='YeV2SlB6')): # check if the page is valid
			name = trip.name(soup)
			
			if (soup.find('div', class_='ui_poi_review_rating')):
				overall_score = trip.overall_score(soup)
				no_of_reviews = trip.no_of_reviews(soup)
				last_review_date = trip.last_review_date(soup)
				last_review_score = trip.last_review_score(soup)
				reviews = trip.get_reviews(soup)

			scraped += 1
			row = [name, overall_score, no_of_reviews, last_review_date, last_review_score] + reviews
			ws.append(row)

			name = None
			overall_score, no_of_reviews = '0', '0'
			last_review_date, last_review_score = '0', '0'
			reviews = ['0', '0', '0', '0', '0']
			print('Link {}: Scraped'.format(total))
		
		else:
			print('Link {}: Invalid'.format(total))
			pass
			not_scraped += 1

	wb.save(output_file)
	
	end = time.time() # stop counting seconds
	print('\nLinks scraped:{}'.format(scraped))
	print('Total Links:{}'.format(scraped+not_scraped))
	print('\nTime taken: {} seconds'.format(end-start))
	input('\nPress any button to exit...')