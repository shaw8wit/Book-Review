# Book Review

<p>A book review website. Users will be able to register in the website and then log in using their username and password.</p>
<p>Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people.</p>
<p>Also a third-party API by Goodreads, another book review website, has been used, to pull in ratings from a broader audience.</p>
<p>Finally, users will be able to query for book details and book reviews programmatically via the website’s API and will get a json response if valid else an error.</p>


## Getting Started
<ul>
<li>set environment variable FLASK_APP to be application.py</li>
<li>set up a postgre database (online(Heroku) or offine) and add the link to the DATABASE_URL environment variable</li>
<li>run the import.py to setup the database</li>
<li>flask run, to run on localhost, additionally set FLASK_DEBUG to 1 to enable debugger</li>
</ul>
