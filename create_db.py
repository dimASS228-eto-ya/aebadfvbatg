import sqlite3


# Создаем БД или же подключаемся к ней.
conn =sqlite3.connect('articles.db')

# Создаем обьект cursor
cur = conn.cursor()

# Создаем таблицу в БД.
cur.execute("""CREATE TABLE IF NOT EXISTS articles(
	Название_статьи TEXT,
	Ссылка_статьи TEXT,
	Тематика_статьи TEXT,
	Количество_просмотров TEXT,
	Время_создания_статьи TEXT,
	Название_автора_статьи TEXT,
	Ссылка_на_автора TEXT,
	Количество_лайков TEXT,
	Количество_комментариев TEXT,
	Сделали_репост TEXT,
	Текст статьи TEXT);
""")
conn.commit()