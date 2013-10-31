from flask import Flask
from flask import render_template, request, session

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/', methods=["GET", "POST"])
def home():
	d = {'stories': []}
	story = ["Title", "Line.", "Another line.", "A third line."]
	for i in range(3):
		d['stories'].append(story)

	if request.method == "GET": #GET
		return render_template("home.html", d=d)
	else: #POST
		session['user'] = "user"
		d['loggedIn'] = True
		return render_template("home.html", d=d)

@app.route("/account")
def account():
	if (session['user'] == "user"):
		d = {}
		d['loggedIn'] = True
	return render_template("account.html", d=d)


if __name__ == "__main__":
	app.debug = True
	app.run(port = 5005)
