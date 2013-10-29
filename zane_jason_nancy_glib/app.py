from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
	d = {'stories': []}
	story = ["Title", "Line.", "Another line.", "A third line."]
	for i in range(3):
		d['stories'].append(story)

	if request.method == "GET": #GET
		return render_template("home.html", d=d)
	else: #POST
		d['loggedIn'] = True
		return render_template("home.html", d=d)

@app.route("/account")
def account():
	return render_template("account.html")


if __name__ == "__main__":
	app.debug = True
	app.run()
