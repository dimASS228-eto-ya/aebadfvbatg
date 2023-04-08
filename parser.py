"""Парсер vc.ru."""

import requests
import create_db

from bs4 import BeautifulSoup
from selenium import webdriver



# Просим пользователя ввести количество статей, которые надо спарсить.
while True:
	try:
		number_of_articles_to_parse = int(input("Введите количество статей, которые надо спарсить: "))
		break
	except:
		print("\nВводите только цулочисленные числа.")
		continue

# Открываем Chrome.
driver = webdriver.Chrome()
# Открываем сайт vc.ru.
driver.get("https://vc.ru/popular")


# Сохраняем весь контент в этой переменной.
html = driver.page_source
# Фильтруем весь контент и оставляем только html.
soup = BeautifulSoup(html, 'lxml')


# Получаем ссылки на все появившиеся статьи.
article_links = soup.find_all('a', class_="content-link", attrs={"data-analytics": "Popular — Feed Item"})

# Проверяем длину статей с длиной вводимым от пользователя.
if len(article_links) < number_of_articles_to_parse:
	while True:
		# Сравниваем оба значения.
		if len(article_links) < number_of_articles_to_parse:
			# Листаем сайт.
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			# Присоединяем к нашему списку данных еще и новые данные.
			article_links.extend(soup.find_all('a', class_="content-link", attrs={"data-analytics": "Popular — Feed Item"}))
		else:
			break

# Создадим нужный срез который выбрал пользователь.
article_links = article_links[:number_of_articles_to_parse]


# Перед добавлением данных в БД сначало надо ее очистить.
create_db.cur.execute("DELETE FROM articles")


# Перебираем весь список со всеми ссылками и парсим каждую из них.
for link in article_links:

	# Берем ссылку на статью.
	article_url = link.get("href")
	# Переходим по ссылке.
	response = requests.get(article_url)
	# Фильтруем весь контент и оставляем только html.
	article_soup = BeautifulSoup(response.text, 'lxml')



	# Получаем название автора, количество лайков и количество комментариев.
	try:
		article_data = article_soup.find('div', class_="l-hidden entry_data").get("data-article-info").replace("false", "False").replace("true", "True")
		
		# Преврашаем полученные данные в словарь.
		article_data = eval(article_data)
		
		# Название автора статьи.
		author_name = article_data["author_name"]
		
		# Количество написанных комментариев.
		article_comment = article_data["comments"]

		# Берем количество лайков.
		article_likes = article_data["likes"]

		# Сделать репост.
		favorites = article_data["favorites"]
	
	except:
		author_name = article_soup.find('a', class_="content-header-author__name").text.strip()

		article_comment = article_soup.find('div', class_="comments-header__title comments__title").text.strip()

		article_likes = "Нет данных"

		favorites = "Нет данных"



	# Название статьи.
	article_name = article_soup.find('h1', class_="content-title").text.strip().replace("\n\n\nСтатьи редакций", "")


	# Количество просмотров статьи.
	article_views = article_soup.find('span', class_="views__value").text.strip()


	# Тематика статьи.
	try:
		subject_article = article_soup.find('div', class_="content-header-author__name").text.strip()
	except:
		subject_article = "Нет данных"


	# Время добавлений статьи.
	article_publish_time = article_soup.find('time', class_="time", attrs={"air-module": "module.date"}).get("title")



	# Ссылка на автора статьи.
	try:
		author_link = article_soup.find('a', class_="content-header-author__name").get('href')
	except:
		author_link = "Нет данных"


	# Текст статьи.
	try:
		response = requests.get(article_url)
		soup = BeautifulSoup(response.text, "html.parser")
		article_text_list = ""

		teme = soup.find("div", class_="l-entry__content").find_all("p")
		
		for item in teme:
			article_text = item.text.strip()
			article_text_list += article_text
			
	except:
		article_text_list = "Нет данных"


	# Добавляем спарсенные данные в кортеж следующим видом (article_name, article_url, subject_article, article_views, article_publish_time, author_name, author_link, article_likes, article_comment, author_subscribers, favorites)


	# Добавляем данные в БД.
	create_db.cur.execute("INSERT INTO articles VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (article_name, article_url, subject_article, article_views, article_publish_time, author_name, author_link, article_likes, article_comment, favorites, article_text_list))

create_db.conn.commit()