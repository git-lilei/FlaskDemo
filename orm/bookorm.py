from sqlalchemy import create_engine, and_
from orm import model

engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                       encoding='utf8', echo=True)
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


# 添加书籍
def insertBook(bookname, author, price, abstract, userid):
    session.add(model.Book(bookname=bookname, author=author, price=price, abstract=abstract, userid=userid))
    session.commit()
    session.close()


# 删除书籍
def deleteBook(id):
    session.query(model.Book).filter(model.Book.id == id).delete()
    session.commit()
    session.close()


# 根据id修改书籍信息
def updateBookById(id, bookname, author, price, abstract):
    session.query(model.Book).filter(model.Book.id == id) \
        .update({model.Book.bookname: bookname, model.Book.author: author, \
                 model.Book.price: price, model.Book.abstract: abstract})
    session.commit()
    session.close()


# 查询所有书籍
def checkBooks(user):
    result = session.query(model.User).filter(model.User.username == user).first().t
    return result


# 根据用户名查询用户id
def checkUseridByName(user):
    result = session.query(model.User.id).filter(model.User.username == user).all()[0][0]
    return result


# 根据id查询书籍
def checkBookById(id):
    result = session.query(model.Book.id, model.Book.bookname, \
                           model.Book.author, model.Book.price, model.Book.abstract).filter(model.Book.id == id).all()
    return result


# 根据书籍名字模糊查询
def checkBookByName(name, userid):
    result = session.query(model.Book) \
        .filter(and_(model.Book.bookname.like('%' + name + '%'))) \
        .filter(model.Book.userid == userid) \
        .all()
    return result


# 根据价格区间查询书籍
def checkBookByPrice(beginprice, endprice, userid):
    result = session.query(model.Book) \
        .filter(model.Book.price.between(beginprice, endprice)) \
        .filter(model.Book.userid == userid) \
        .all()
    return result


# 价格降序查询书籍
def checkBookByPriceDesc(userid):
    result = session.query(model.Book).filter(model.Book.userid == userid).order_by(model.Book.price.desc()).all()
    return result


# 价格升序查询书籍
def checkBookByPriceAsc(userid):
    result = session.query(model.Book).filter(model.Book.userid == userid).order_by(model.Book.price).all()
    return result
