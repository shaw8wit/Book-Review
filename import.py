import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# #creating table users
# db.execute("""CREATE TABLE users (
# 		username VARCHAR PRIMARY KEY,
# 		password VARCHAR NOT NULL,
# 		email VARCHAR NOT NULL
# 	);""")
# db.commit()

# #creating table for books
# db.execute("""CREATE TABLE books (
# 		isbn VARCHAR PRIMARY KEY,
# 		name VARCHAR NOT NULL,
# 		author VARCHAR NOT NULL,
# 		year INTEGER NOT NULL
# 	);""")
# db.commit()

#creating table for reviews
# db.execute("""CREATE TABLE reviews (
# 		id SERIAL PRIMARY KEY,
# 		rating VARCHAR NOT NULL,
# 		content VARCHAR NOT NULL,
# 		username VARCHAR REFERENCES users,
# 		isbn VARCHAR REFERENCES books
# 	);""")
# db.commit()

# out = csv.reader(open("books.csv"))
# for data in out:
# 	db.execute("INSERT into books (isbn, name, author, year) VALUES (:isbn, :name, :author, :year)",{"isbn": data[0], "name": data[1], "author": data[2], "year": data[3]})
# 	print("adding.....")
# db.commit()