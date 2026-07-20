from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
# موجودیت________________________________
from BE.be_Daroo import Base


engine=create_engine("sqlite:///Darookhaneh.db")


session1=sessionmaker(bind=engine)
session2=session1()

class Repository:

    def Add(self,object):
        session2.add(object)
        session2.commit()
        return True

    def Read(self,Tablename):
        return session2.query(Tablename).all()

    def ReadByIdCustomer(self,Tablename,id):
        return session2.query(Tablename).filter(Tablename.customer_id==id).first()


    def Delete(self,obj):
        session2.delete(obj)
        session2.commit()
        return True


    def Exist(self,Tablename,newobj):
        result=session2.query(Tablename).filter((Tablename.first_name==newobj.first_name) &
                                                (Tablename.last_name==newobj.last_name) &
                                                (Tablename.phone_number==newobj.phone_number)).all()
        if result==[]:
            return True
        else:
            return False



    def UpdateDynamicCustomer(self,oldobj,**kwargs):
        # print(kwargs)
        # print(kwargs.items())
        for key,val in kwargs.items():
            setattr(oldobj,key,val)
        session2.commit()
        return True


    def Search(self,Tablename,search):
        result=session2.query(Tablename).filter((Tablename.customer_id.like(f"%{search}%"))|
                                                (Tablename.first_name.like(f"%{search}%"))|
                                                (Tablename.last_name.like(f"%{search}%"))|
                                                (Tablename.phone_number.like(f"%{search}%"))|
                                                (Tablename.adress.like(f"%{search}%"))|
                                                (Tablename.registration_date.like(f"%{search}%"))).all()
        return result


    def Report(self,Tablename,D1,D2):
        return session2.query(Tablename).filter(Tablename.registration_date.between(D1,D2)).all()

# -------------------------------------------------------------------------------------------------------


    def ReadByIdProduct(self,Tablename,id):
        return session2.query(Tablename).filter(Tablename.product_id==id).first()

    def ReadProduct(self,Tablename):
        return session2.query(Tablename).all()


    def ExistProduct(self,Tablename,newobj):
        result=session2.query(Tablename).filter((Tablename.generic==newobj.generic) &
                                                (Tablename.tejari==newobj.tejari) &
                                                (Tablename.dooz==newobj.dooz)).all()
        if result==[]:
            return True
        else:
            return False

    def UpdateDynamicProduct(self,oldobj,**kwargs):
        # print(kwargs)
        # print(kwargs.items())
        for key,val in kwargs.items():
            setattr(oldobj,key,val)
        session2.commit()
        return True


# --------------------------------------------------------------------------------------------------

    def ExistInvoice(self,Tablename,newobj):
        result=session2.query(Tablename).filter((Tablename.customer_id==newobj.customer_id) &
                                                (Tablename.product_id==newobj.product_id) &
                                                (Tablename.customer_name==newobj.customer_name) &
                                                (Tablename.generic_name==newobj.generic_name)).all()
        if result==[]:
            return True
        else:
            return False


# ------------------------------------------------------------------------------------------------
    def Login(self,Tablename,newobj):
        print("Username:", newobj.username)
        print("Password:", newobj.password)
        result = session2.query(Tablename).filter((Tablename.username==newobj.username) &
                                                 (Tablename.password == newobj.password)).all()
        if result==[]:
            return False
        else:
            return result

# ________________________________________مربوط به موجودیت انبار_________________________________________
def Mojodiat():
    Base.metadata.create_all(engine)


