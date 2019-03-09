import requests
from bs4 import BeautifulSoup
import time

def extract_news(parser):
	""" Extract news from a given web page """
	news_list = []
	par = parser.find_all("tr", attrs = {"class": "athing"})
	newsss = parser.find_all("a", attrs = {"class":"storylink"})
	points = parser.find_all("span", attrs = {"class":"score"})
	author = parser.find_all("a", attrs = {"class":"hnuser"})
	news2 = parser.find_all("td", attrs = {"class":"subtext"})


	for i in range(len(par)):
		cm = news2[i].find_all("a")
		if cm[3].text == "discuss" or cm[3].text == "hide":
			comments = "0"
		else:
			comments = cm[3].text.split()[0]
		news ={
		'author':author[i].text,
		'comments':comments,
		'points':points[i].text.split()[0],
		'title':newsss[i].text,
		'url':newsss[i]['href'],
			}
		news_list.append(news)
	return news_list


def extract_next_page(parser):
	""" Extract next page URL """
	y = parser.find("a", attrs = {"class":"morelink"})
	next_page = y['href']
	return next_page


def get_news(url, n_pages=1):
	""" Collect news from a given web page """
	news = []
	while n_pages:
		print("Collecting data from page: {}".format(url))
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		news_list = extract_news(soup)
		next_page = extract_next_page(soup)
		url = "https://news.ycombinator.com/" + next_page
		news.extend(news_list)
		n_pages -= 1
		time.sleep(30)
	return news

