import psycopg2
import csv
connection = psycopg2.connect("dbname=lotr_database user=grahambrown host=/tmp/")
cur = connection.cursor()
data = open("data.csv", "r")
reader = csv.reader(data)
cur.execute("CREATE TABLE character (\
id serial PRIMARY KEY, \
name varchar, \
home_city varchar, \
age integer, \
race varchar)")
for row in reader:
    name = row[0]
    home = row[1]
    age = str(row[2])
    race = row[3]
    cur.execute('INSERT INTO character(name, home_city, age, race) \
VALUES(%s, %s, %s, %s)', (name, home, age, race))

connection.commit()
cur.close()
connection.close()
