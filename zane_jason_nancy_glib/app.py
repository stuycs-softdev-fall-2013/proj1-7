from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
	d = {}
	d['stories'] = ["","",""]
	if request.method == "GET":
		return render_template("home.html", d=d)
	else:
		d['loggedIn'] = True
		return render_template("home.html", d=d)

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=5000)
