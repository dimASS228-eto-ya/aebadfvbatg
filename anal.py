import sqlite3
import nltk
from nltk.corpus import stopwords
from collections import defaultdict


nltk.download('stopwords')

# Создаем БД или же подключаемся к ней.
conn = sqlite3.connect('articles.db')

# Создаем объект cursor
cur = conn.cursor()

# Функция для удаления стоп слов из текста
def remove_stopwords(text):
    stop_words = set(stopwords.words('russian'))
    tokens = [word.lower() for word in nltk.word_tokenize(text) if word.isalpha()]
    return [t for t in tokens if t not in stop_words]

# Анализируем статьи
popular_words = defaultdict(int)
unpopular_words = defaultdict(int)
popular_names = defaultdict(int)
topics_views = defaultdict(int)

cur.execute("SELECT * FROM articles")
rows = cur.fetchall()
for row in rows:
    # Удаляем стоп слова и заполняем семантическое ядро
    text = row[10]
    words = remove_stopwords(text)
    semantic_core = defaultdict(int)
    for word in words:
        semantic_core[word] += 1

    # Добавляем количество прочтений к слову
    for word in words:
        word_views = int(row[3]) * words.count(word)
        if word_views > 0:
            popular_words[word] += word_views
        else:
            unpopular_words[word] += word_views

    # Добавляем количество прочтений к имени автора
    author_name = row[5].split()[0]
    author_views = int(row[3])
    popular_names[author_name] += author_views

    # Считаем количество прочтений каждой тематики
    topic = row[2]
    topic_views = int(row[3])
    topics_views[topic] += topic_views

# Сортируем слова по популярности
popular_words = {k: v for k, v in sorted(popular_words.items(), key=lambda item: item[1], reverse=True)}
unpopular_words = {k: v for k, v in sorted(unpopular_words.items(), key=lambda item: item[1])}

# Выводим результаты
print("Самые популярные слова:")
for word, views in list(popular_words.items())[:100]:
    print(word, views)

print("\nСамые непопулярные слова:")
for word, views in list(unpopular_words.items())[:100]:
    print(word, views)

print("\nСамые популярные имена:")
for name, views in list(popular_names.items())[:50]:
    print(name, views)

print("\nКоличество прочтений каждой тематики:")
for topic, views in topics_views.items():
    print(topic, views)
