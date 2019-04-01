from sqlalchemy import create_engine
from orm import model
engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                                    encoding='utf8', echo=True)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

def insertUser(username,password):
    result = session.add(model.User(username=username,password=password))
    session.commit()
    session.close()
    print(result)

def checkUser(username,password):
    result = session.query(model.User).filter(model.User.username==username). \
                filter(model.User.password==password).first()
    print('+++++++++',result)
    if result:
        return True
    else:
        return False
