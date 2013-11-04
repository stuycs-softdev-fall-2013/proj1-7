from flask import Flask
from flask import render_template,session,redirect,request,url_for
import auth
import posts
from time import strftime


app = Flask(__name__)
app.secret_key = "BLOGINATOR"
_loggedin = False

@app.route('/')
def home():
    blogs = posts.getPosts()
    datum = {}
    global _loggedin
    datum['user'] = _loggedin
    if _loggedin:
        datum['admin'] =  auth.admin(session['username'])
    else: datum['admin']=False
    return render_template('home.html',blogs=blogs,data=datum)

@app.route('/register',methods = ['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        datum={}
        global _loggedin
        datum['user'] = _loggedin
        if _loggedin:
            datum['admin'] =  auth.admin(session['username'])
        else: datum['admin']= False
        return render_template('Register.html',data=datum)
    if request.method == "POST":
        fname = request.form['Firstname']
        lname = request.form['Lastname']
        name = request.form['username']
        pw = request.form['pw']
        pw2 = request.form['pw2']
        if auth.register(fname,lname,name,pw,pw2) == 0:
            _loggedin = True
            session["username"]= fname +" "+lname
            return redirect(url_for('home'))
        elif auth.register(fname,lname,name,pw,pw2) == 1:
            m = "username already registered. Try a differnt one"
            data = {'user':False,'admin':False}
            return render_template("Register.html",data=data,m=m)
        return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        datum = {}
        global _loggedin
        datum['user'] = _loggedin
        datum['admin'] =  False
        return render_template('Login.html',data=datum)
    if request.method == "POST":
        if auth.authenticate(request.form['username'],request.form['pw']):
            session['username'] = request.form['username']
            _loggedin = True
            return redirect(url_for('home'))
        response = "unrecognized username and/or password combination"
        data = {'user':False,'admin':False}
        return render_template('Login.html',response = response,data=data)

@app.route('/manage')
def manage():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        datum = {}
        global _loggedin
        datum['user'] = _loggedin
        datum['admin'] = auth.admin(session['username'])
        return render_template('manage.html',uname = session['username'],data=datum)
    if request.method == 'POST':
        pw = request.form['oldPassWord']
        newpw = request.form['newPassWord']
        newpw2 = request.form['newPassWord']
        if not auth.authenticate(session['username'],pw):
            return "incorrect current password" + render_template('manage.html')
        elif newpw != newpw2:
            return "new passwords do not match" + render_template('manage.html' )
        else:
            auth.changepw(session['username'],newpw)
            return redirect(url_for('myacc'))
    

@app.route('/myacc',methods=['GET','POST'])
def myacc():
    if 'username' in session:
        name = session['username']
        datum = {}
        global _loggedin
        datum['user'] = _loggedin
        datum['admin'] = auth.admin(name)
        return render_template('MyAccountNormal.html',name = name,data=datum)   
    return redirect(url_for('login'))

@app.route('/post',methods =['GET','POST'])
def post(link):
    if request.method=='GET':
        datum = {}
        global _loggedin
        datum['user'] = _loggedin
        datum['admin'] = auth.admin(session['username'])
        return render_template('post.html',text=posts.single(link),data=datum)

@app.route('/write',methods=['GET','POST'])
def write():
    if request.method=='GET':
        datum = {}
        global _loggedin
        datum['user'] = _loggedin
        datum['admn'] = auth.admin(session['username'])
        return render_template('newpost.html',data=datum)
    elif request.method == 'POST':
        t = request.form['title']
        p = request.form['content']
        ti = strftime("%X %x")
        if not posts.write(t,ti,p):
            m = "another post with teh same title exist, please rename your piece"
            return render_template('write.html',m=m)
        return redirect(url_for("home"))        

@app.route('/logout')
def logout():
    session.pop('username',None)
    global _loggedin
    _loggedin = False
    return redirect(url_for("home"))

@app.route('/delete')
def delete():
    posts.delete(link)
    return redirect(url_for('myacc'))

if __name__ == '__main__':
    app.debug = True
    app.run()
