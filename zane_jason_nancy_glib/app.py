from flask import Flask
from flask import render_template, request, session
from pymongo import MongoClient
import auth

client = MongoClient()
db = client.db

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/', methods=["GET", "POST"])
def home():
	d = auth.load_stories()

	if request.method == "GET": #GET
		return render_template("home.html", d=d)

	#POST
	data = request.form
	logged_in = auth.login(data['usern'], data['passw'])
	d['logged_in'] = logged_in

	return render_template("home.html", d=d)

@app.route('/account')
def account():
	if (session['user'] == "user"):
		d = {}
		d['loggedIn'] = True
	return render_template("account.html", d=d)

#@app.route('/register')
#def register():
#	return render_template('register.html')

if __name__ == "__main__":
	app.debug = True
	app.run(port = 5000)
