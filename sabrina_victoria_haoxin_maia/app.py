import auth
from flask import Flask,render_template,session,redirect,request,url_for

app = Flask(__name__)
app.secret_key = "BLOGINATOR"
_ADMIN = 'ADMIN'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    if 'username' in session:
        return redirect(url_for('/'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('/'))
    elif request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if auth.authenticate(request.form['username'],request.form['pw']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        return "unrecognized user and/or pw" + render_template('login.html')

@app.route('/myacc',methods=['GET','POST'])
def myacc():
    if 'username' in session:
        if 'username' == _ADMIN:
            if method == 'GET':
                return render_template('adminAcc')
            else:
                return render_template('adminAcc')
        
        elif method == 'GET':
            return render_template('acc')
        else:
            return render_template('acc')

        
    return redirect(url_for('home'))

@app.route('/entry')
def entry():
    
