from flask import Flask
from flask import render_template,session,redirect,request,url_for
import auth
import posts
from time import strftime


app = Flask(__name__)
app.secret_key = "BLOGINATOR"
_loggedin = False
_link = ""

@app.route('/',methods=['POST','GET'])
def home():
    blogs = posts.getPosts()
    datum = iden() 
    if request.method == 'GET':
        return render_template('home.html',blogs=blogs,data=datum)
    if request.method == "POST":
        if request.form['btn']:
            global _link
            _link = request.form['btn']
            return redirect(url_for("post"))

@app.route('/register',methods = ['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    datum = iden()
    if request.method == 'GET':
        return render_template('Register.html',data=datum)
    if request.method == "POST":
        fname = request.form['Firstname']
        lname = request.form['Lastname']
        name = request.form['username']
        pw = request.form['pw']
        pw2 = request.form['pw2']
        if pw != pw2:
            m = "passwords to not match, please try again."
            return render_template("Register.html",data=datum,m=m)
        if auth.register(fname,lname,name,pw):
            global _loggedin
            _loggedin = True
            session["username"]= name
            return redirect(url_for('home'))
        else:
            m = "username already registered. Try a differnt one"
            return render_template("Register.html",data=datum,m=m)
        return redirect(url_for('home'))
        

@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    datum = iden()
    if request.method == 'GET':
        return render_template('Login.html',data=datum)
    if request.method == "POST":
        uname = request.form['username']
        pw = request.form['pw']
        if auth.authenticate(uname,pw):
            session['username']= uname
            global _loggedin
            _loggedin = True
            return redirect(url_for('home'))
        response = "unrecognized username and/or password combination"
        return render_template('Login.html',response = response,data=datum)

@app.route('/manage',methods=['GET','POST'])
def manage():
    if 'username' not in session:
        return redirect(url_for('login'))
    datum = iden()
    uname = session['username']
    if request.method == 'GET':
        return render_template('manage.html',uname = uname,data=datum)
    if request.method == 'POST':
        pw = request.form['oldPassWord']
        newpw = request.form['newPassWord']
        newpw2 = request.form['newPassWord2']
        if not auth.authenticate(session['username'],pw):
            m = "incorrect current password"
            return render_template('manage.html',m=m,uname=uname,data=datum)
        elif newpw != newpw2:
            m = "new passwords do not match"
            return render_template('manage.html',m=m,data=datum,uname=uname)
        else:
            auth.changepw(session['username'],newpw)
            return redirect(url_for('myacc'))
    

@app.route('/myacc',methods=['GET','POST'])
def myacc():
    if 'username' in session:
        name = auth.getName(session['username'])
        blogs = posts.getPosts()
        datum = {}
        global _loggedin
        datum['user'] = _loggedin
        datum['admin'] = auth.admin(name)
        return render_template('MyAccountNormal.html',name=name,data=datum,blogs=blogs)   
    return redirect(url_for('login'))

@app.route('/post',methods =['GET','POST'])
def post():
    datum = iden()
    global _loggedin
    global _link
    text = posts.single(_link)
    if request.method=='GET':
        return render_template('post.html',text=text,data=datum,loggedin=_loggedin)
    if request.method=='POST':
        if request.form['btn'] == "write":
            comment = request.form['comment']
            time = strftime("%X %x")
            posts.commentate(_link,session['username'],time,comment)
        else:
            commentNum = request.form['btn']
            posts.upvoteComment(_link,commentNum)
        text = posts.single(_link)
        return render_template('post.html',text=text,data=datum,loggedin=_loggedin)

@app.route('/write',methods=['GET','POST'])
def write():
    if 'username' not in session:
        return redirect(url_for('login'))
    datum = iden()
    if request.method=='GET':
        return render_template('newpost.html',data=datum)
    elif request.method == 'POST':
        t = request.form['title']
        p = request.form['content']
        ti = strftime("%X %x")
        if not posts.write(t,ti,p):
            m = "another post with the same title exist, please rename your piece"
            return render_template('newpost.html',m=m,data=datum)
        return redirect(url_for("home"))        

@app.route('/logout')
def logout():
    session.pop('username',None)
    global _loggedin
    _loggedin = False
    return redirect(url_for("home"))

def iden():
    datum={}
    global _loggedin
    datum['user'] = _loggedin
    if _loggedin:
        datum['admin'] =  auth.admin(session['username'])
    else: datum['admin']= False
    return datum

@app.route('/delete')
def delete():
    posts.delete(link)
    return redirect(url_for('myacc'))

if __name__ == '__main__':
    app.debug = True
    app.run()
