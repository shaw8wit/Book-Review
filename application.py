import os
import requests
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	if session.get("username") is not None:
		return render_template("home.html", name=session.get("username"))
	return render_template("login.html")

@app.route("/home", methods=["POST"])
def home():
	session.clear()
	name = request.form.get("name")
	dbpwd = db.execute("SELECT password FROM users WHERE username = :username", {"username": name}).fetchone()
	if dbpwd != None:
		pwd = request.form.get("pwd")
		if pwd == dbpwd[0]:
			session["username"] = name
			return render_template("home.html", name=name)
	else:
		return redirect("/signup")
	return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
	session.clear()
	name = request.form.get("name")
	pwd = request.form.get("pwd")
	email = request.form.get("email")
	db.execute("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)",{"username": name, "password": pwd, "email": email})
	db.commit()
	session["username"] = name
	return render_template("home.html", name=name)

@app.route("/signup")
def signup():
	if session.get("username") is not None:
		return render_template("home.html", name=session.get("username"))
	return render_template("signup.html")

@app.route("/find", methods=["POST"])
def find():
	isbn = request.form.get("isbn")
	name = request.form.get("name")
	author = request.form.get("author")
	if len(isbn)==0:
		ans = queryOne("name",name) if len(author)==0 else queryOne("author", author) if len(name)==0 else queryTwo("name", name, "author", author)
	elif len(name)==0:
		ans = queryOne("isbn",isbn) if len(author)==0 else queryOne("author", author) if len(isbn)==0 else queryTwo("isbn", isbn, "author", author)
	elif len(author)==0:
		ans = queryOne("isbn",isbn) if len(name)==0 else queryOne("name", name) if len(isbn)==0 else queryTwo("isbn", isbn, "name", name)
	else:
		ans = db.execute(f"SELECT * FROM books WHERE isbn LIKE '%{isbn}%' AND name LIKE '%{name}%' AND author LIKE '%{author}%'").fetchall()
	return render_template("search_result.html", ans=ans)

def queryOne(name, value):
	ans = db.execute(f"SELECT * FROM books WHERE {name} LIKE '%{value}%'").fetchall()
	return ans

def queryTwo(n1, v1, n2, v2):
	ans = db.execute(f"SELECT * FROM books WHERE {n1} LIKE '%{v1}%' AND {n2} LIKE '%{v2}%'").fetchall()
	return ans

@app.route("/details/<isbn>")
def details(isbn):
	ans = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
	response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": 'JkwcGThDCN97xqvW7Stg', "isbns": isbn})
	sna = response.json()
	if response.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
	reviews = db.execute("SELECT rating, content, username FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
	return render_template("details.html", res=ans, avg=sna['books'][0]['average_rating'], rating=sna['books'][0]['average_rating'], total=sna['books'][0]['ratings_count'], reviews=reviews)

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

@app.route("/review/<isbn>", methods=["POST"])
def review(isbn):
	username = session.get("username")
	ans = db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND username = :username", {"isbn": isbn, "username": username}).fetchall()
	if ans == []:
		rating = request.form.get("rating")
		content = request.form.get("content")
		db.execute("INSERT INTO reviews (rating, content, username, isbn) VALUES (:rating, :content, :username, :isbn)",{"rating": rating, "content": content, "username": username, "isbn": isbn})
		db.commit()
	return redirect("/details/"+isbn)

@app.route("/api/<isbn>", methods=['GET'])
def api(isbn):
    row = db.execute("SELECT name, author, year, books.isbn, COUNT(reviews.id) as review_count, AVG(CAST(reviews.rating AS INTEGER)) as average_score FROM books INNER JOIN reviews ON books.isbn = reviews.isbn WHERE books.isbn = :isbn GROUP BY name, author, year, books.isbn", {"isbn": isbn})
    if row.rowcount != 1:
        return jsonify({"Error": "No Data for this isbn"}), 422
    tmp = row.fetchone()
    result = dict(tmp.items())
    result['average_score'] = float('%.1f'%(result['average_score']))
    return jsonify(result)