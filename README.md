# book-review-website

A book review website. Users will be able to register in the website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. Also a third-party API by Goodreads, another book review website, has been used, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via the website’s API.

## Getting Started

-> set environment variable FLASK_APP to be application.py

-> set up a postgre database (online(Heroku) or offine) and add the link to the DATABASE_URL environment variable

-> run the import.py to setup the database

-> flask run to run on localhost, additionally set FLASK_DEBUG to 1 to enable debugger
