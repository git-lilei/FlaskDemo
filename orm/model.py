from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
# class Book():
#
#     def __init__(self,_id=None,_name=None,_price=None):
#         self.id=_id
#         self.name=_name
#         self.price=_price
#
#     def __str__(self):
#         return 'id: %s name: %s price: %s',(self.id,self.name,self.price)

engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                                    encoding='utf8', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(bind=engine)

from sqlalchemy import Column,String,Integer,ForeignKey
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    username = Column(String(20),nullable=False)
    password = Column(String(20),nullable=False)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    bookname = Column(String(20),nullable=False)
    author = Column(String(20),nullable=False)
    price = Column(Integer,nullable=False)
    abstract = Column(String(255), nullable=False)
    userid = Column(Integer,ForeignKey('user.id',ondelete='RESTRICT',onupdate='RESTRICT'))
    user =  relationship('User',backref='t')

# if __name__ == "__main__":
#     Base.metadata.create_all(bind=engine)