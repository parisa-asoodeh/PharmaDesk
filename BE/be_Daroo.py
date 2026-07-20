import jdatetime
from sqlalchemy import create_engine,Column,Integer,String,NVARCHAR,ForeignKey,Table,Date
from sqlalchemy.orm import declarative_base,sessionmaker,relationship

Base=declarative_base()
engine=create_engine("sqlite:///Darookhaneh.db")

def get_shamsidate():
    now=jdatetime.datetime.now()
    return now.strftime("%Y-%m-%d")


class Customer(Base):
    __tablename__="Customer"
    customer_id=Column(Integer,primary_key=True,autoincrement=True)
    first_name=Column(NVARCHAR)
    last_name = Column(NVARCHAR)
    phone_number = Column(NVARCHAR)
    adress = Column(NVARCHAR)
    registration_date=Column(NVARCHAR,default=get_shamsidate)
    Invoice=relationship("Invoice",back_populates="Customer")
    # def __init__(self,first_name,last_name,email,.....):  متدسازنده الزامی نیست
    #     self.first_name=first_name
    #     self.....
    #     self...
    #


class Product(Base):
    __tablename__="Product"
    product_id=Column(Integer,primary_key=True,autoincrement=True)
    generic=Column(NVARCHAR)
    tejari = Column(NVARCHAR)
    dooz = Column(NVARCHAR)
    dasteh = Column(NVARCHAR)
    shekl = Column(NVARCHAR)
    engheza = Column(NVARCHAR)
    price = Column(NVARCHAR)
    sefareshAval=Column(Integer)
    mojodi = Column(Integer)
    Invoice=relationship("Invoice",back_populates="Product")



class Invoice(Base):
    __tablename__="Invoice"
    invoice_id=Column(Integer,primary_key=True,autoincrement=True)
    customer_id=Column(Integer,ForeignKey("Customer.customer_id"))
    Customer=relationship("Customer",back_populates="Invoice")

    product_id=Column(Integer,ForeignKey("Product.product_id"))
    Product=relationship("Product",back_populates="Invoice")

    number=Column(NVARCHAR)
    customer_name = Column(NVARCHAR)
    generic_name = Column(NVARCHAR)
    shekl_daroo = Column(NVARCHAR)
    one_price = Column(NVARCHAR)
    total_price = Column(NVARCHAR)
    date=Column(NVARCHAR,default=get_shamsidate)


class Login(Base):
    __tablename__="Login"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(NVARCHAR)
    username = Column(NVARCHAR)
    password = Column(NVARCHAR)
    role = Column(NVARCHAR)

    def __init__(self,Name,Username,Password,Role):
        self.name=Name
        self.username=Username
        self.password=Password
        self.role=Role



Base.metadata.create_all(engine)



session1=sessionmaker(bind=engine)
session2=session1()
user_exist=session2.query(Login).count()>0
if not user_exist:
    firstlogin=Login("Default","User1","1234","مدیر")
    session2.add(firstlogin)
    session2.commit()