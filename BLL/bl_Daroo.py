from DAL.repository import Repository
from BE.be_Daroo import *
# موجودیت______________________________________
from DAL.repository import session2
from BE.be_Daroo import Product


class BlDaroo:

    def blAdd(self,obj):
        repose=Repository()
        result=repose.Add(obj)
        return result

    def blRead(self,Tablename):
        repose = Repository()
        result = repose.Read(Tablename)
        return result

    def blReadById(self,Tablename,id):
        repose = Repository()
        result=repose.ReadById(Tablename,id)
        return result

    def blDelete(self,Tablename,id):
        repose = Repository()
        print(id)
        obj=repose.ReadByIdCustomer(Tablename,id)
        result=repose.Delete(obj)
        return result

    def blExist(self,Tablename,newobj):
        repose = Repository()
        result=repose.Exist(Tablename,newobj)
        return result


    def blUpdateDynamicCustomer(self,Tablename,id,**kwargs):
        repose = Repository()
        obj = repose.ReadByIdCustomer(Tablename, id)
        return repose.UpdateDynamicCustomer(obj,**kwargs)


    def blSearch(self,Tablename,search):
        repose = Repository()
        lstobj=repose.Search(Tablename,search)
        return lstobj


    def blreport(self,Tablename,D1,D2):
        repose = Repository()
        result= repose.Report(Tablename,D1,D2)
        return result

# --------------------------------------------------------------------

    def blReadByIdProduct(self,Tablename,id):
        repose = Repository()
        result=repose.ReadByIdProduct(Tablename,id)
        return result

    def blReadProduct(self,Tablename):
        repose = Repository()
        result = repose.ReadProduct(Tablename)
        return result

    def blExistProduct(self,Tablename,newobj):
        repose = Repository()
        result=repose.ExistProduct(Tablename,newobj)
        return result

    def blUpdateDynamicProduct(self,Tablename,id,**kwargs):
        repose = Repository()
        obj = repose.ReadByIdProduct(Tablename, id)
        return repose.UpdateDynamicProduct(obj,**kwargs)

    def blDeleteProduct(self,Tablename,id):
        repose = Repository()
        print(id)
        obj=repose.ReadByIdProduct(Tablename,id)
        result=repose.Delete(obj)
        return result


# --------------------------------------------------------------------------
    def blExistInvoice(self,Tablename,newobj):
        repose = Repository()
        result=repose.ExistInvoice(Tablename,newobj)
        return result


# ----------------------------------------------------------------------

    def blLogin(self,Tablename,newobj):
        repose = Repository()
        result = repose.Login(Tablename,newobj)
        return result
# ___________________________مربوط به موجودیت انبار___________________________

def forosh_daroo(drug_name:str,amount:int):

    try:
        drug = session2.query(Product).filter(Product.generic == drug_name).first()
        if not drug:
            return {"status": "error", "msg": "دارو یافت نشد"}

        amount = int(amount)

        if drug.mojodi < amount:
            return {"status": "error", "msg": "موجودی کافی نیست"}

        drug.mojodi -= amount
        session2.commit()

        if drug.mojodi <= 10:
            return {"status": "warning", "msg": f"  موجودی {drug.generic} :کم شده است. موجودی فعلی {drug.mojodi} "}

        return {"status": "success", "msg": f"فروش موفق. موجودی جدید {drug.mojodi}"}
    finally:
        pass


# ------------------------------------ساخت پنجره جدید-------------------------------------
def get_All_Daroo():

    try:
        all_drugs=session2.query(Product).all()
        return all_drugs
    finally:
        pass

