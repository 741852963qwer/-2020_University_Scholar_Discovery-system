#encoding:utf-8
from flask import Flask,render_template,request,redirect,url_for
import config
from models import User
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = False
        username = request.form.get('username')
        password = request.form.get('password')
        for name,password1 in db.session.query(User.nickname,User.password):
            if name == username and password1 == password:
                user = True
        if user:
            # db.session['nickname'] = username
            return redirect(url_for('index'))
        else:
            return u'用户名或者密码错误'



@app.route('/recover/',methods=['get','post'])
def recover():
    if request.method == 'GET':
        return render_template('recover.html')
    else:
        pass
@app.route('/regist/',methods=['get','post'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        question = request.form.get('question')
        answer = request.form.get('answer')
        #验证
        user = True
        for name in db.session.query(User.nickname):
            if name == username:
                user = False
        if not user:
            return u'改用户名已被注册'
        else:
            if password != password1:
                return u'两次密码不相等'
            else:
                user = User(nickname=username,password=password,pw_secure_question=question,pw_secure_answer=answer)
                db.session.add(user)
                db.session.commit()
                #跳转
                return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
