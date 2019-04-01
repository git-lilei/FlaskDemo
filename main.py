from flask import Flask, render_template, request, redirect, make_response
from orm import manageorm as manage
from orm import bookorm as bm
import datetime

app = Flask(__name__)


# 首页
@app.route('/')
def index():
    user = None
    user = request.cookies.get('name')
    return render_template('index.html', userinfo=user)


# 退出
@app.route('/quit')
def quit():
    resp = make_response(redirect('/'))
    resp.delete_cookie('name')
    return resp


# 注册
@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    elif request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        try:
            manage.insertUser(account, password)
            return redirect('/login')
        except:
            return redirect('/regist')


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        try:
            result = manage.checkUser(account, password)
            if result == True:
                res = make_response(redirect('/list'))
                res.set_cookie('name', account, expires=datetime.datetime.now() + datetime.timedelta(days=7))
                return res
            else:
                return redirect('/login')
        except:
            return redirect('/login')


# 列表页
@app.route('/list')
def list():
    user = request.cookies.get('name')
    res = bm.checkBooks(user)

    return render_template('list.html', prolist=res, userinfo=user)


# 详情页
@app.route('/detail/<id>')
def detail(id):
    user = request.cookies.get('name')
    res = bm.checkBookById(id)
    return render_template('detail.html', userinfo=user, booklist=res)


# 添加书籍
@app.route('/insertbook', methods=['POST', 'GET'])
def insertbook():
    if request.method == 'GET':
        user = request.cookies.get('name')
        return render_template('insertbook.html', userinfo=user)
    elif request.method == 'POST':
        bookname = request.form['bookname']
        author = request.form['author']
        price = request.form['price']
        abstract = request.form['abstract']
        user = request.cookies.get('name')
        userid = bm.checkUseridByName(user)
        try:
            bm.insertBook(bookname, author, price, abstract, userid)
            return redirect('/list')
        except:
            return redirect('/insertbook')


# 根据id删除书籍
@app.route('/deletebook/<id>')
def deleteBook(id):
    try:
        bm.deleteBook(id)
        return redirect('/list')
    except:
        return redirect('/list')


# 根据id修改书籍信息
@app.route('/updatebook/<id>', methods=['POST', 'GET'])
def updatebook(id):
    if request.method == 'GET':
        user = request.cookies.get('name')
        res = bm.checkBookById(id)
        return render_template('updatebook.html', id=id, booklist=res, userinfo=user)
    elif request.method == 'POST':
        bookname = request.form['bookname']
        author = request.form['author']
        price = request.form['price']
        abstract = request.form['abstract']
        try:
            bm.updateBookById(id, bookname, author, price, abstract)
            return redirect('/list')
        except:
            return '失败'


# 根据书籍名称模糊查询
@app.route('/searchBookByName/<name>')
def searchBookByName(name):
    user = request.cookies.get('name')
    userid = bm.checkUseridByName(user)
    res = bm.checkBookByName(name, userid)
    return render_template('list.html', prolist=res, userinfo=user)


# 根据价格区间查询书籍
@app.route('/searchBookByPrice', methods=['POST', 'GET'])
def searchBookByPrice():
    if request.method == 'POST':
        user = request.cookies.get('name')
        userid = bm.checkUseridByName(user)
        beginprice = request.form['beginprice']
        endprice = request.form['endprice']
        res = bm.checkBookByPrice(beginprice, endprice, userid)
        return render_template('list.html', prolist=res, userinfo=user)


# 价格降序查询书籍
@app.route('/checkBookByPriceDesc')
def checkBookByPriceDesc():
    user = request.cookies.get('name')
    userid = bm.checkUseridByName(user)
    res = bm.checkBookByPriceDesc(userid)
    return render_template('list.html', prolist=res, userinfo=user)


# 价格升序查询书籍
@app.route('/checkBookByPriceAsc')
def checkBookByPriceAsc():
    user = request.cookies.get('name')
    userid = bm.checkUseridByName(user)
    res = bm.checkBookByPriceAsc(userid)
    return render_template('list.html', prolist=res, userinfo=user)


if __name__ == ("__main__"):
    app.run()
