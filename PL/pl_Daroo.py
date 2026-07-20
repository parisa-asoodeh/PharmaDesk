from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# موجودیت --------------------------------
from BLL.bl_Daroo import forosh_daroo
from DAL.repository import Mojodiat
Mojodiat()
# ساخت پنجره جدید--------------------------------
from BLL.bl_Daroo import get_All_Daroo


from BE.be_Daroo import *
from BLL.bl_Daroo import BlDaroo


import time
import threading

from datetime import datetime
import jdatetime


import customtkinter as ctk
from PIL import Image as PILImage   # 👈 مهم: ماژول درست
# from PIL import Image


from customtkinter import CTk, CTkFrame
from tkinter import Canvas
from PIL import Image, ImageTk

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "assets" / "images"



class AppDaroo(CTkFrame):
    def __init__(self, screen):
        super().__init__(screen)
        self.pack(fill="both", expand=True)

        # بارگذاری تصویر اصلی
        self.bg_image_pil = Image.open(IMAGE_DIR / "page.png")

        # ساخت Canvas
        self.canvas = Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # متن دلخواه
        self.text_x = 130
        self.text_y = 200
        self.text_font = ("BNazanin", 55)
        self.text_color = "#70E000"
        self.text_content = "اپلیکیشن مدیریت داروخانه"

        # فراخوانی Create_Widget
        self.Create_Widget()

        # بایند کردن تغییر اندازه پنجره
        self.canvas.bind("<Configure>", self.resize_background)

    def Create_Widget(self):
        # تصویر و متن اولیه (تصویر بدون resize)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_pil)
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)
        self.text_id = self.canvas.create_text(self.text_x, self.text_y,
                                               text=self.text_content,
                                               fill=self.text_color,
                                               font=self.text_font,
                                               anchor="nw")

    def resize_background(self, event):
        # resize تصویر به اندازه Canvas
        width = event.width
        height = event.height
        bg_resized = self.bg_image_pil.resize((width, height))
        self.bg_image_tk = ImageTk.PhotoImage(bg_resized)

        # جایگزین کردن تصویر بک‌گراند
        self.canvas.itemconfig(self.bg_id, image=self.bg_image_tk)



        photoEnter = CTkImage(Image.open(IMAGE_DIR / "enter.png"), size=(100, 100))
        self.btnenter = CTkButton(self.master, text="", image=photoEnter, fg_color="#0c141b", hover=False,command=self.Enter)
        self.btnenter.place(relx=0.0, rely=0.83)

        # ------------------------------------ContentFrame----------------------------------
        self.contentframe = CTkFrame(self.master, fg_color="#3A506B", width=1350,height=700)
        self.contentframe.place_forget()

        # بارگذاری عکس بک‌گراند
        bg_content_img = Image.open(IMAGE_DIR / "bg_content.jpg")  # اسم فایلت
        bg_content_photo = CTkImage(light_image=bg_content_img, dark_image=bg_content_img, size=(1350, 700))

        # لیبل با عکس بک‌گراند
        self.bg_label_content = CTkLabel(self.contentframe, image=bg_content_photo, text="")
        self.bg_label_content.place(x=0, y=0, relwidth=1, relheight=1)

        self.photoVorod = ctk.CTkImage(Image.open(IMAGE_DIR / "vorod.png"), size=(60, 60))
        self.btnMenu = CTkButton(self.contentframe, text="",image=self.photoVorod,width=2, font=("Vazir", 20),hover=False
                                 ,fg_color="#dff5f2",command=self.open_menu)
        self.btnMenu.place(relx=0.93, rely=0.01)

        self.label_Welcom=Label(self.contentframe,text="داروخانه دکتر فریدونی",fg="#2EC4B6",bg="#dff5f2",
                                   width=14,height=2,font="BNazanin 55")
        self.label_Welcom.place(relx=0.26, rely=0.29)




        self.menu_width = 0
        self.max_width = 250
        self.height = 700
        self.contentframe_width = 1360

        self.menuframe=CTkFrame(self.contentframe,fg_color="#1B3A4B",width=250,height=700)
        self.menuframe.place(x=self.contentframe_width,y=0) # دقیقا بیرون سمت راست



    # **************************************************************************************************
    # ********************************************CustomerFrame*****************************************

        self.CustomerFrame = CTkFrame(self.contentframe, width=800, height=600, fg_color="#006466")
        self.CustomerFrame.place_forget()

        self.lblFirstname = CTkLabel(self.CustomerFrame, text="نام", text_color="#EDEDE9", fg_color="#006466",font=("Vazir", 18)).place(x=605, y=45)
        self.lblLastname = CTkLabel(self.CustomerFrame, text="نام خانوادگی", text_color="#EDEDE9", fg_color="#006466",font=("Vazir", 18)).place(x=605, y=75)
        self.lblPhone = CTkLabel(self.CustomerFrame, text="شماره تماس", text_color="#EDEDE9", fg_color="#006466",font=("Vazir", 18)).place(x=605, y=105)
        self.lblAdress = CTkLabel(self.CustomerFrame, text="آدرس", text_color="#EDEDE9", fg_color="#006466",font=("Vazir", 18)).place(x=605, y=135)
        self.lblRegDate = CTkLabel(self.CustomerFrame, text="تاریخ ثبت نام", text_color="#EDEDE9", fg_color="#006466",font=("Vazir", 18)).place(x=605, y=165)

        self.lable = CTkLabel(self.CustomerFrame, text="", font=("Vazir", 18), text_color="#EDEDE9")
        # self.lable.place(x=310,y=160)

        self.varCustomer_Id = IntVar()
        self.varFirstname = StringVar()
        self.varLastname = StringVar()
        self.varPhone = StringVar()
        self.varAdress = StringVar()
        self.varRegDate = StringVar()

        self.txtFirstname = CTkEntry(self.CustomerFrame, textvariable=self.varFirstname)
        self.txtFirstname.configure(fg_color="#90E0EF", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtFirstname.place(x=450, y=40)

        self.txtLastname = CTkEntry(self.CustomerFrame, textvariable=self.varLastname)
        self.txtLastname.configure(fg_color="#90E0EF", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtLastname.place(x=450, y=70)

        self.txtPhone = CTkEntry(self.CustomerFrame, textvariable=self.varPhone)
        self.txtPhone.configure(fg_color="#90E0EF", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtPhone.place(x=450, y=100)

        self.txtAdress = CTkEntry(self.CustomerFrame, textvariable=self.varAdress)
        self.txtAdress.configure(fg_color="#90E0EF", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtAdress.place(x=450, y=130)

        self.txtRegDate = CTkEntry(self.CustomerFrame, textvariable=self.varRegDate)
        self.txtRegDate.configure(fg_color="#90E0EF", text_color="#003566", font=("Vazir", 18), justify=RIGHT)
        self.txtRegDate.place(x=450, y=160)

        self.photoReg = ctk.CTkImage(Image.open(IMAGE_DIR / "register.png"), size=(70, 70))
        self.photoEdit = ctk.CTkImage(Image.open(IMAGE_DIR / "Edit.png"), size=(70, 70))
        self.photoDelete = ctk.CTkImage(Image.open(IMAGE_DIR / "delete.png"), size=(70, 70))
        self.photoClose = ctk.CTkImage(Image.open(IMAGE_DIR / "close.png"), size=(30, 30))
        self.photoSearch = ctk.CTkImage(Image.open(IMAGE_DIR / "search.png"), size=(40, 40))
        self.photoReport = ctk.CTkImage(Image.open(IMAGE_DIR / "report.png"), size=(70, 70))

        self.btnClose = CTkButton(self.CustomerFrame, text="", image=self.photoClose, fg_color="#006466", hover=False,
                                  width=5, command=self.CloseCustomerFrame)
        self.btnClose.place(x=757, y=1)

        self.btnReg = CTkButton(self.CustomerFrame, text="", image=self.photoReg, fg_color="#006466", hover=False,
                                width=5, command=self.RegistrationCustomer)
        self.btnReg.place(x=610, y=270)
        self.btnReg.bind("<Enter>", lambda event: self.show_text_customer("ثبت نام"))
        self.btnReg.bind("<Leave>", lambda event: self.hide_text())

        self.btnEdit = CTkButton(self.CustomerFrame, text="", image=self.photoEdit, fg_color="#006466", hover=False,
                                 width=5, command=self.EditCustomer)
        self.btnEdit.place(x=610, y=375)
        self.btnEdit.bind("<Enter>", lambda event: self.show_text_customer("ویرایش"))
        self.btnEdit.bind("<Leave>", lambda event: self.hide_text())

        self.btnDelete = CTkButton(self.CustomerFrame, text="", image=self.photoDelete, fg_color="#006466", hover=False,
                                   width=5, command=self.DeleteCustomer)
        self.btnDelete.place(x=610, y=475)
        self.btnDelete.bind("<Enter>", lambda event: self.show_text_customer("حذف"))
        self.btnDelete.bind("<Leave>", lambda event: self.hide_text())

        self.btnSearch = CTkButton(self.CustomerFrame, text="", image=self.photoSearch, fg_color="#006466", hover=False,
                                   width=5, command=self.ShowHideSearchCustomer)
        self.btnSearch.place(x=50, y=195)

        self.btnReport = CTkButton(self.CustomerFrame, text="", image=self.photoReport, fg_color="#006466", hover=False,
                                   width=5, command=self.ShowHideReportCustomer)
        self.btnReport.place(x=30, y=20)

        self.btnAddtoInvoice = CTkButton(self.CustomerFrame, text="افزودن به فاکتور", fg_color="#0D1B2A",
                                          text_color="#faf684", font=("Vazir", 18), hover=False,
                                         command = self.AddCustomerToInvoice)
        self.btnAddtoInvoice.place(x=450, y=215)

        # ----------------------ReportFrame-------------------------
        self.ReportCustomerFrame = CTkFrame(self.CustomerFrame, width=200, height=150, fg_color="#8ECAE6")
        self.ReportCustomerFrame.place_forget()

        self.vardate1 = StringVar()
        self.vardate2 = StringVar()

        self.txtdate1 = CTkEntry(self.ReportCustomerFrame, textvariable=self.vardate1, width=130,text_color="#003566")
        self.txtdate1.place(x=15, y=20)
        self.txtdate1.configure(fg_color="white",font=("Vazir", 15))

        self.txtdate2 = CTkEntry(self.ReportCustomerFrame, textvariable=self.vardate2, width=130,text_color="#003566")
        self.txtdate2.place(x=15, y=65)
        self.txtdate2.configure(fg_color="white",font=("Vazir", 15))

        self.lbldate1 = CTkLabel(self.ReportCustomerFrame, text="از تاریخ", font=("Vazir", 15), fg_color="#8ECAE6",
                                 text_color="#003566").place(x=150, y=19)
        self.lbldate2 = CTkLabel(self.ReportCustomerFrame, text="تا تاریخ", font=("Vazir", 15), fg_color="#8ECAE6",
                                 text_color="#003566").place(x=150, y=62)

        self.btnReportCustomer = CTkButton(self.ReportCustomerFrame, text="گزارش گیری", fg_color="#EDEDE9",
                                           text_color="purple", font=("Vazir", 19), width=5, command=self.report)
        self.btnReportCustomer.place(x=30, y=110)

        # --------------------SearchFrame--------------------------
        self.SearchCustomerFrame = CTkFrame(self.CustomerFrame, width=320, height=50, fg_color="#8ECAE6")
        self.SearchCustomerFrame.place_forget()

        self.btnSearchCustomer = CTkButton(self.SearchCustomerFrame, text="جستجو", fg_color="#EDEDE9",
                                           text_color="purple",
                                           font=("Vazir", 20), width=10, command=self.SearchCustomer)
        self.btnSearchCustomer.place(x=15, y=10)

        self.varSearchCustomer = StringVar()
        self.txtSearchCustomer = CTkEntry(self.SearchCustomerFrame, textvariable=self.varSearchCustomer, width=230)
        self.txtSearchCustomer.place(x=80, y=10)
        self.txtSearchCustomer.configure(fg_color="white",text_color="#003566",font=("Vazir", 16))

        self.tblCustomer = ttk.Treeview(self.CustomerFrame, columns=("c1", "c2", "c3", "c4", "c5", "c6"),
                                        show="headings", height=15)

        self.tblCustomer.heading("#6", text="کد مشتری")
        self.tblCustomer.column("#6", width=60, anchor=CENTER)
        self.tblCustomer.heading("#5", text="نام")
        self.tblCustomer.column("#5", width=80, anchor=CENTER)
        self.tblCustomer.heading("#4", text="نام خانوادگی")
        self.tblCustomer.column("#4", width=95, anchor=CENTER)
        self.tblCustomer.heading("#3", text="شماره تماس")
        self.tblCustomer.column("#3", width=110, anchor=CENTER)
        self.tblCustomer.heading("#2", text="آدرس")
        self.tblCustomer.column("#2", width=100, anchor=CENTER)
        self.tblCustomer.heading("#1", text="تاریخ ثبت نام")
        self.tblCustomer.column("#1", width=90, anchor=CENTER)
        self.tblCustomer.place(x=50, y=250)
        self.tblCustomer.bind("<<TreeviewSelect>>", self.GetSelectionCustomer)


    # *************************************************************************************************
    # *********************************************ProductFrame****************************************
        self.ProductFrame = CTkFrame(self.contentframe, width=850, height=650, fg_color="#006466")
        self.ProductFrame.place_forget()


        self.lblGeneric = CTkLabel(self.ProductFrame, text="نام ژنریک", text_color="#FFE5EC",fg_color="#006466", font=("Vazir", 18)).place(
            relx=0.8, rely=0.11)
        self.lblTejari = CTkLabel(self.ProductFrame, text="نام تجاری", text_color="#FFE5EC",fg_color="#006466", font=("Vazir", 18)).place(
            relx=0.8, rely=0.17)
        self.lblDooz = CTkLabel(self.ProductFrame, text="دوز", text_color="#FFE5EC",fg_color="#006466", font=("Vazir", 18)).place(
            relx=0.8, rely=0.23)
        self.lblDasteh = CTkLabel(self.ProductFrame, text="دسته دارویی", text_color="#FFE5EC",fg_color="#006466", font=("Vazir", 18)).place(
            relx=0.8, rely=0.29)

        self.lblShekl = CTkLabel(self.ProductFrame, text="شکل دارویی", text_color="#FFE5EC",fg_color="#006466",
                                         font=("Vazir", 18)).place(relx=0.5, rely=0.11)
        self.lblEngheza = CTkLabel(self.ProductFrame, text="تاریخ انقضا", text_color="#FFE5EC",fg_color="#006466",
                                      font=("Vazir", 18)).place(relx=0.5, rely=0.17)
        self.lblPrice = CTkLabel(self.ProductFrame, text="قیمت", text_color="#FFE5EC",fg_color="#006466",
                                         font=("Vazir", 18)).place(relx=0.5, rely=0.23)
        self.lblSefaresh_Aval = CTkLabel(self.ProductFrame, text="سفارش اولیه", text_color="#FFE5EC", fg_color="#006466",
                                  font=("Vazir", 18)).place(relx=0.5, rely=0.29)
        self.lblMojodi = CTkLabel(self.ProductFrame, text="موجودی انبار", text_color="#FFE5EC",fg_color="#006466",
                                         font=("Vazir", 18)).place(relx=0.5, rely=0.35)


        self.lblProduct = CTkLabel(self.ProductFrame, text="", text_color="#FFE5EC", font=("Vazir", 18))
        self.lblProduct.place(relx=0.01, rely=0.05)

        self.btnCloseProduct = CTkButton(self.ProductFrame, text="", image=self.photoClose, fg_color="#006466", width=5,
                                         hover=False, command=self.CloseProductFrame).place(relx=0.95, rely=0.0)

        self.btnRegProduct = CTkButton(self.ProductFrame, text="", image=self.photoReg, fg_color="#006466", width=5,
                                       font=("Vazir", 16), hover=False, command=self.RegistrationProduct)
        self.btnRegProduct.place(relx=0.1, rely=0.01)
        self.btnRegProduct.bind("<Enter>", lambda event: self.show_text_Product("ثبت نام"))
        self.btnRegProduct.bind("<Leave>", lambda event: self.hide_text_Product())

        # self.photoEditProduct = PhotoImage(file="editProduct.png")
        self.btnEditProduct = CTkButton(self.ProductFrame, text="", image=self.photoEdit, fg_color="#006466",width=5,
                                        font=("Vazir", 16), hover=False, command=self.EditProduct)
        self.btnEditProduct.place(relx=0.1, rely=0.16)
        self.btnEditProduct.bind("<Enter>", lambda event: self.show_text_Product("ویرایش"))
        self.btnEditProduct.bind("<Leave>", lambda event: self.hide_text_Product())

        # self.photoDeleteProduct = PhotoImage(file="deleteProduct.png")
        self.btnDeleteProduct = CTkButton(self.ProductFrame, text="", image=self.photoDelete, fg_color="#006466",width=7,
                                          font=("Vazir", 16), hover=False, command=self.DeleteProduct)
        self.btnDeleteProduct.place(relx=0.1, rely=0.3)
        self.btnDeleteProduct.bind("<Enter>", lambda event: self.show_text_Product("حذف"))
        self.btnDeleteProduct.bind("<Leave>", lambda event: self.hide_text_Product())

        self.btnAddtoInvoice2 = CTkButton(self.ProductFrame, text="افزودن به فاکتور", fg_color="#0D1B2A",
                                          text_color="#faf684", font=("Vazir", 18), hover=False,
                                          command=self.AddProductToInvoice)
        self.btnAddtoInvoice2.place(relx=0.79, rely=0.42)

        self.varProductId = IntVar()
        self.varGeneric = StringVar()
        self.varTejari = StringVar()
        self.varDooz = StringVar()
        self.varDasteh = StringVar()
        self.varShekl = StringVar()
        self.varEngheza = StringVar()
        self.varPrice = StringVar()
        self.varSefaresh_Aval=StringVar()
        self.varMojodi= StringVar()


        self.txtGeneric = CTkEntry(self.ProductFrame, textvariable=self.varGeneric)
        self.txtGeneric.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtGeneric.place(relx=0.62, rely=0.11)

        self.txtTejari = CTkEntry(self.ProductFrame, textvariable=self.varTejari)
        self.txtTejari.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtTejari.place(relx=0.62, rely=0.17)

        self.txtDooz = CTkEntry(self.ProductFrame, textvariable=self.varDooz)
        self.txtDooz.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtDooz.place(relx=0.62, rely=0.23)

        self.txtDasteh = CTkEntry(self.ProductFrame, textvariable=self.varDasteh)
        self.txtDasteh.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtDasteh.place(relx=0.62, rely=0.29)

        self.txtShekl = CTkEntry(self.ProductFrame, textvariable=self.varShekl)
        self.txtShekl.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtShekl.place(relx=0.32, rely=0.11)

        self.txtEngheza = CTkEntry(self.ProductFrame, textvariable=self.varEngheza)
        self.txtEngheza.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 16), justify=RIGHT)
        self.txtEngheza.place(relx=0.32, rely=0.17)

        self.txtPrice = CTkEntry(self.ProductFrame, textvariable=self.varPrice)
        self.txtPrice.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 16), justify=RIGHT)
        self.txtPrice.place(relx=0.32, rely=0.23)

        self.txtSefaresh_Aval=CTkEntry(self.ProductFrame,textvariable=self.varSefaresh_Aval)
        self.txtSefaresh_Aval.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 16), justify=RIGHT)
        self.txtSefaresh_Aval.place(relx=0.32, rely=0.29)

        self.txtMojodi = CTkEntry(self.ProductFrame,textvariable=self.varMojodi)
        self.txtMojodi.configure(fg_color="#FFC8DD", text_color="#3A506B", font=("Vazir", 16), justify=RIGHT)
        self.txtMojodi.place(relx=0.32, rely=0.35)


        self.tblProduct = ttk.Treeview(self.ProductFrame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7",
                                                                   "c8", "c9","c10"),show="headings", height=15)

        self.tblProduct.heading("#10", text="کد کالا")
        self.tblProduct.column("#10", width=50, anchor=CENTER)
        self.tblProduct.heading("#9", text="نام ژنریک")
        self.tblProduct.column("#9", width=100, anchor=CENTER)
        self.tblProduct.heading("#8", text="نام تجاری")
        self.tblProduct.column("#8", width=100, anchor=CENTER)
        self.tblProduct.heading("#7", text="دوز")
        self.tblProduct.column("#7", width=60, anchor=CENTER)
        self.tblProduct.heading("#6", text="دسته دارویی")
        self.tblProduct.column("#6", width=90, anchor=CENTER)
        self.tblProduct.heading("#5", text="شکل دارویی")
        self.tblProduct.column("#5", width=90, anchor=CENTER)
        self.tblProduct.heading("#4", text="تاریخ انقضا")
        self.tblProduct.column("#4", width=90, anchor=CENTER)
        self.tblProduct.heading("#3", text="قیمت")
        self.tblProduct.column("#3", width=85, anchor=CENTER)
        self.tblProduct.heading("#2", text="سفارش اولیه")
        self.tblProduct.column("#2", width=75, anchor=CENTER)
        self.tblProduct.heading("#1", text="موجودی انبار")
        self.tblProduct.column("#1", width=70, anchor=CENTER)
        self.tblProduct.place(relx=0.02, rely=0.48)

        self.tblProduct.bind("<<TreeviewSelect>>", self.GetSelectionProduct)


        # ****************************************************************************************************
        # ***********************************************InvoicesFrame****************************************
        self.InvoicesFrame = CTkFrame(self.contentframe, width=800, height=600, fg_color="#006466")
        self.InvoicesFrame.place_forget()

        self.lblInvoiceCodeIn = CTkLabel(self.InvoicesFrame, text="کد فاکتور", text_color="#FCF6BD",
                                         font=("Vazir", 18)).place(relx=0.76, rely=0.11)
        self.lblCustomerCodeIn = CTkLabel(self.InvoicesFrame, text="کد مشتری", text_color="#FCF6BD",
                                          font=("Vazir", 18)).place(relx=0.76, rely=0.17)
        self.lblProductCodeIn = CTkLabel(self.InvoicesFrame, text="کد دارو", text_color="#FCF6BD",
                                         font=("Vazir", 18)).place(relx=0.76, rely=0.23)
        self.lblProductNumberIn = CTkLabel(self.InvoicesFrame, text="تعداد", text_color="#FCF6BD",
                                           font=("Vazir", 18)).place(relx=0.76, rely=0.29)

        self.lblCustomerNameIn = CTkLabel(self.InvoicesFrame, text="نام مشتری", text_color="#FCF6BD",
                                          font=("Vazir", 18)).place(relx=0.5, rely=0.05)
        self.lblGenericNameIn = CTkLabel(self.InvoicesFrame, text="نام دارو", text_color="#FCF6BD",
                                          font=("Vazir", 18)).place(relx=0.5, rely=0.11)
        self.lblSheklDarooIn = CTkLabel(self.InvoicesFrame, text="شکل دارویی", text_color="#FCF6BD",
                                          font=("Vazir", 18)).place(relx=0.5, rely=0.17)
        self.lblProductPriceIn = CTkLabel(self.InvoicesFrame, text="قیمت واحد", text_color="#FCF6BD",
                                          font=("Vazir", 18)).place(relx=0.5, rely=0.23)
        self.lblProductAllPriceIn = CTkLabel(self.InvoicesFrame, text="قیمت کل", text_color="#FCF6BD",
                                             font=("Vazir", 18)).place(relx=0.5, rely=0.29)
        self.lblInvoiceDate = CTkLabel(self.InvoicesFrame, text="تاریخ", text_color="#FCF6BD",
                                       font=("Vazir", 18)).place(relx=0.5, rely=0.35)

        self.lblInvoice = CTkLabel(self.InvoicesFrame, text="", text_color="#FCF6BD", font=("Vazir", 20))
        self.lblInvoice.place(relx=0.01, rely=0.05)

        self.varInvoiceCodeIn = IntVar()
        self.varCustomerCodeIn = IntVar()
        self.varProductCodeIn = IntVar()
        # self.varProductCodeIn.set(1)
        self.varProductNumberIn = StringVar()
        self.varCustomerNameIn = StringVar()
        self.varGenericNameIn = StringVar()
        self.varSheklDarooIn = StringVar()
        self.varProductPriceIn = StringVar()
        self.varProductAllPriceIn = StringVar()

        self.txtInvoiceCodeIn = CTkEntry(self.InvoicesFrame, width=35, textvariable=self.varInvoiceCodeIn)
        self.txtInvoiceCodeIn.configure(fg_color="#FCF6BD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT,state=DISABLED)
        self.txtInvoiceCodeIn.place(relx=0.7, rely=0.11)

        self.txtCustomerCodeIn = CTkEntry(self.InvoicesFrame, width=35, textvariable=self.varCustomerCodeIn)
        self.txtCustomerCodeIn.configure(fg_color="#FCF6BD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtCustomerCodeIn.place(relx=0.7, rely=0.17)

        self.txtProductCodeIn = CTkEntry(self.InvoicesFrame, width=35, textvariable=self.varProductCodeIn)
        self.txtProductCodeIn.configure(fg_color="#FCF6BD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtProductCodeIn.place(relx=0.7, rely=0.23)

        self.comboProductNumberIn = ttk.Combobox(self.InvoicesFrame,values = [str(i) for i in range(1,101)],
                                                background="#E9E984", foreground="#3A506B", justify=CENTER, width=2)
        self.comboProductNumberIn.place(relx=0.7, rely=0.29)
        print("start")
        self.comboProductNumberIn.bind("<<ComboboxSelected>>", self.Calculate_Price)
        print("end")


        self.txtCustomerNameIn = CTkEntry(self.InvoicesFrame, textvariable=self.varCustomerNameIn)
        self.txtCustomerNameIn.configure(fg_color="#FCF6BD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtCustomerNameIn.place(relx=0.31, rely=0.05)

        self.txtGenericNameIn = CTkEntry(self.InvoicesFrame,textvariable=self.varGenericNameIn)
        self.txtGenericNameIn.configure(fg_color="#FCF6BD",text_color="#3A506B",font=("Vazir", 18),justify=RIGHT)
        self.txtGenericNameIn.place(relx=0.31, rely=0.11)

        self.txtSheklDarooIn = CTkEntry(self.InvoicesFrame, textvariable=self.varSheklDarooIn)
        self.txtSheklDarooIn.configure(fg_color="#FCF6BD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtSheklDarooIn.place(relx=0.31, rely=0.17)

        self.txtProductPriceIn = CTkEntry(self.InvoicesFrame, textvariable=self.varProductPriceIn)
        self.txtProductPriceIn.configure(fg_color="#FCF6BD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtProductPriceIn.place(relx=0.31, rely=0.23)

        self.txtProductAllPriceIn = CTkEntry(self.InvoicesFrame, textvariable=self.varProductAllPriceIn)
        self.txtProductAllPriceIn.configure(fg_color="#FCF6BD", text_color="#3A506B", font=("Vazir", 18), justify=RIGHT)
        self.txtProductAllPriceIn.place(relx=0.31, rely=0.29)

        self.varInvoicedate = StringVar()
        self.txtInvoicedate = CTkEntry(self.InvoicesFrame, textvariable=self.varInvoicedate)
        self.txtInvoicedate.configure(fg_color="#FCF6BD", text_color="#003566", font=("Vazir", 18), justify=RIGHT)
        self.txtInvoicedate.place(relx=0.31, rely=0.35)

        self.photoRegStore = ctk.CTkImage(Image.open(IMAGE_DIR / "Reg_Store.png"), size=(70, 70))
        self.btnRegStore = CTkButton(self.InvoicesFrame, text="", image=self.photoRegStore, fg_color="#006466", width=5,
                                      hover=False, command=self.Check_Mojodiat)
        self.btnRegStore.place(relx=0.12, rely=0.01)
        self.btnRegStore.bind("<Enter>", lambda event: self.show_text_RegStore("ثبت انبار"))
        self.btnRegStore.bind("<Leave>", lambda event: self.hide_text_RegStore())

        self.btnRegInvoice = CTkButton(self.InvoicesFrame, text="", image=self.photoReg, fg_color="#006466",width=5,
                                        hover=False, command=self.RegistrationInvoice)
        self.btnRegInvoice.place(relx=0.12, rely=0.15)
        self.btnRegInvoice.bind("<Enter>", lambda event: self.show_text_Invoices("ثبت فاکتور"))
        self.btnRegInvoice.bind("<Leave>", lambda event: self.hide_text_Invoices())


        self.btnToplevel = CTkButton(self.InvoicesFrame, text="موجودی انبار",font=("Vazir", 21),fg_color="#0D1B2A",
                                     text_color="#faf684",command=self.show_mojoodi_window)
        self.btnToplevel.place(relx=0.07, rely=0.33)

        self.btnCloseInvoice = CTkButton(self.InvoicesFrame, text="", image=self.photoClose, fg_color="#006466",
                                         width=5, font=("Vazir", 16), hover=False, command=self.CloseInvoicesFrame)
        self.btnCloseInvoice.place(relx=0.95, rely=0.0)


        self.tblInvoice = ttk.Treeview(self.InvoicesFrame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7",
                                                                    "c8", "c9", "c10"), show="headings", height=14)
        self.tblInvoice.heading("#10", text="کدفاکتور")
        self.tblInvoice.column("#10", width=50, anchor=CENTER)
        self.tblInvoice.heading("#9", text="کدمشتری")
        self.tblInvoice.column("#9", width=55, anchor=CENTER)
        self.tblInvoice.heading("#8", text="کد دارو")
        self.tblInvoice.column("#8", width=50, anchor=CENTER)
        self.tblInvoice.heading("#7", text="تعداد")
        self.tblInvoice.column("#7", width=50, anchor=CENTER)
        self.tblInvoice.heading("#6", text="نام مشتری")
        self.tblInvoice.column("#6", width=105, anchor=CENTER)
        self.tblInvoice.heading("#5", text="نام دارو")
        self.tblInvoice.column("#5", width=105, anchor=CENTER)
        self.tblInvoice.heading("#4", text="شکل دارویی")
        self.tblInvoice.column("#4", width=80, anchor=CENTER)
        self.tblInvoice.heading("#3", text="قیمت واحد")
        self.tblInvoice.column("#3", width=65, anchor=CENTER)
        self.tblInvoice.heading("#2", text="قیمت کل")
        self.tblInvoice.column("#2", width=90, anchor=CENTER)
        self.tblInvoice.heading("#1", text="تاریخ خرید")
        self.tblInvoice.column("#1", width=90, anchor=CENTER)
        self.tblInvoice.place(relx=0.03, rely=0.45)


        # ****************************************************************************************
        # *****************************************LoginFrame*************************************
        self.loginframe = CTkFrame(self.master, width=1350, height=700, fg_color="#001219")
        self.loginframe.place_forget()



        self.lblUser = CTkLabel(self.loginframe, text="نام کاربری", fg_color="#001219", text_color="#99D98C",
                                font=("BNazanin Bold", 27))
        self.lblUser.place(relx=0.47, rely=0.24)

        self.lblPass = CTkLabel(self.loginframe, text="رموز عبور", fg_color="#001219", text_color="#99D98C",
                                font=("BNazanin", 27))
        self.lblPass.place(relx=0.47, rely=0.39)

        self.varUser = StringVar()
        self.varPass = StringVar()

        self.txtUser = CTkEntry(self.loginframe, textvariable=self.varUser)
        self.txtUser.configure(fg_color="#D6CE93", text_color="purple", width=240, font=("Vazir", 20))
        self.txtUser.place(relx=0.42, rely=0.3)

        self.txtPass = CTkEntry(self.loginframe, textvariable=self.varPass)
        self.txtPass.configure(fg_color="#D6CE93", text_color="purple", width=240, font=("Vazir", 20), show="*")
        self.txtPass.place(relx=0.42, rely=0.45)

        self.btnShowHide = CTkButton(self.loginframe, text="نمایش/پنهان رمز", font=("Vazir", 25), fg_color="#1B3A4B",
                                     text_color="#D9ED92", hover=False, command=self.ShowHide)
        self.btnShowHide.place(relx=0.52, rely=0.67)

        self.btnLogin = CTkButton(self.loginframe, text="ورود", font=("Vazir", 25), fg_color="#1B3A4B",
                                  text_color="#D9ED92", hover=False, command=self.Login)
        self.btnLogin.place(relx=0.38, rely=0.67)



    # /////////////////////////////////////توابع مربوط به منو//////////////////////////////////
        self.menu_open = False

    # def toggle_menu(self):
    #     if self.menu_open:
    #         self.close_menu()
    #     else:
    #         self.open_menu()

    def open_menu(self):
        # انیمیشن باز شدن
        for w in range(0, self.max_width + 1, 20):
            self.menu_width = w
            self.menuframe.configure(width=w)
            self.menuframe.place(x=self.contentframe_width - w, y=0)
            self.contentframe.update()
            self.contentframe.after(10)
        self.menu_open = True


        # افزودن دکمه‌های منو
        self.photoCross = CTkImage(Image.open(IMAGE_DIR / "cross1.png"), size=(15, 15))
        self.btn_cross_menu = CTkButton(self.menuframe, text="", image=self.photoCross, width=2,hover=False,
                                        fg_color="#1B3A4B",command=self.close_menu)
        self.btn_cross_menu.place(relx=0.0, rely=0.0)


        photocustomer = ctk.CTkImage(Image.open(IMAGE_DIR / "customer.png"), size=(90, 90))
        self.btncustomer = ctk.CTkButton(self.menuframe, text="", image=photocustomer, fg_color="#1B3A4B",
                                         hover=False, command=self.ShowCustomerFrame).place(relx=0.4, rely=0.04)
        self.lblcustomer = CTkLabel(self.menuframe, text="مشتری ها", fg_color="#1B3A4B", text_color="#faf684",
                                    font=("Vazir", 29)).place(relx=0.1, rely=0.09)

        photoproduct = ctk.CTkImage(Image.open(IMAGE_DIR / "products.png"), size=(90, 90))
        self.btnproduct = CTkButton(self.menuframe, text="", image=photoproduct, fg_color="#1B3A4B", hover=False,
                                    width=8,command=self.ShowProductFrame).place(relx=0.49, rely=0.22)
        self.lblproduct = CTkLabel(self.menuframe, text="داروها", fg_color="#1B3A4B", text_color="#faf684",
                                   font=("Vazir", 29)).place(relx=0.16, rely=0.26)

        photoinvoice = ctk.CTkImage(Image.open(IMAGE_DIR / "invoices.png"), size=(90, 90))
        self.btninvoice = CTkButton(self.menuframe, text="", image=photoinvoice, fg_color="#1B3A4B", hover=False,
                                    width=8,command=self.ShowInvoicesFrame).place(relx=0.47, rely=0.4)
        self.lblinvoice = CTkLabel(self.menuframe, text="فاکتورها", fg_color="#1B3A4B", text_color="#faf684",
                                   font=("Vazir", 29)).place(relx=0.11, rely=0.44)

        photoBehdashti = ctk.CTkImage(Image.open(IMAGE_DIR / "Behdashti.png"), size=(90, 90))
        self.btnBehdashti = CTkButton(self.menuframe, text="", image=photoBehdashti, fg_color="#1B3A4B", hover=False,
                                    width=8).place(relx=0.47, rely=0.58)
        self.lblBehdashti = CTkLabel(self.menuframe, text="بهداشتی", fg_color="#1B3A4B", text_color="#faf684",
                                   font=("Vazir", 29)).place(relx=0.15, rely=0.63)

        photoArayeshi = ctk.CTkImage(Image.open(IMAGE_DIR / "Arayeshi.png"), size=(90, 90))
        self.btnArayeshi = CTkButton(self.menuframe, text="", image=photoArayeshi, fg_color="#1B3A4B", hover=False,
                                      width=8).place(relx=0.47, rely=0.76)
        self.lblArayeshi = CTkLabel(self.menuframe, text="آرایشی", fg_color="#1B3A4B", text_color="#faf684",
                                     font=("Vazir", 29)).place(relx=0.17, rely=0.82)



    def close_menu(self):
        # انیمیشن بسته شدن
        for w in range(self.max_width, -1, -30):
            self.menu_width = w
            self.menuframe.configure(width=w)
            self.menuframe.place(x=self.contentframe_width - w, y=0)
            self.contentframe.update()
            self.contentframe.after(10)
        self.menu_open = False
        for items in self.menuframe.winfo_children():
            items.destroy()


# /////////////////////////////توابع فریم مشتریان//////////////////////////////
    def hide_text(self):
        self.lable.place_forget()

    def show_text_customer(self, text):
        if text == "ثبت نام":
            self.lable.place(x=700, y=290)
            self.lable.configure(text=text)
        elif text == "ویرایش":
            self.lable.place(x=700, y=410)
            self.lable.configure(text=text)
        elif text == "حذف":
            self.lable.place(x=700, y=510)
            self.lable.configure(text=text)

    def ShowHideReportCustomer(self):
        if self.ReportCustomerFrame.winfo_ismapped():
            self.ReportCustomerFrame.place_forget()
        else:
            self.ReportCustomerFrame.place(x=120, y=8)

    def ShowHideSearchCustomer(self):
        if self.SearchCustomerFrame.winfo_ismapped():
            self.SearchCustomerFrame.place_forget()
        else:
            self.SearchCustomerFrame.place(x=110, y=194)

    def ShowCustomerFrame(self):
        self.CustomerFrame.place(relx=0.18, rely=0.08)
        self.InvoicesFrame.place_forget()
        self.ProductFrame.place_forget()
        self.txtRegDate.delete(0, "end")
        self.txtRegDate.insert(0, get_shamsidate())
        self.loadCustomer()

    def CloseCustomerFrame(self):
        # self.lbl_bg.place_forget()
        # self.lbl_welcome.place_forget()
        self.CustomerFrame.place_forget()

    def loadCustomer(self):
        self.tblCustomer.tag_configure("evenrow",background="#EDEDE9")
        self.tblCustomer.tag_configure("oddrow", background="white")
        for item in self.tblCustomer.get_children():
            self.tblCustomer.delete(item)
        objbl = BlDaroo()
        lstCustomers = objbl.blRead(Customer)
        # print(lstCustomers)
        # print(lstCustomers[0])
        # print(lstCustomers[0].first_name)
        for index,item in enumerate(lstCustomers):
            if index%2==0:
                self.tblCustomer.insert("", "end", values=[item.registration_date,item.adress,item.phone_number,item.last_name,
                                                           item.first_name,item.customer_id],tags=("evenrow",))
            else:
                self.tblCustomer.insert("", "end",values=[item.registration_date, item.adress, item.phone_number, item.last_name,
                                                          item.first_name,item.customer_id], tags=("oddrow",))




    def isExistCustomer(self):
        objp = Customer(first_name=self.varFirstname.get(),
                        last_name=self.varLastname.get(),
                        phone_number=self.varPhone.get(),
                        adress=self.varAdress.get(),
                        registration_date=self.varRegDate.get())

        objbl = BlDaroo()
        return objbl.blExist(Customer, objp)

    def RegistrationCustomer(self):
        if self.isExistCustomer():
            objcs = Customer(first_name=self.varFirstname.get(),
                             last_name=self.varLastname.get(),
                             phone_number=self.varPhone.get(),
                             adress=self.varAdress.get(),
                             registration_date=self.varRegDate.get())

            objbl = BlDaroo()
            result = objbl.blAdd(objcs)
            if result == True:
                self.loadCustomer()
                messagebox.showinfo("صحیح", "ثبت نام با موفقیت انجام شد")
                self.varFirstname.set("")
                self.varLastname.set("")
                self.varPhone.set("")
                self.varAdress.set("")
                self.txtFirstname.focus_set()
        else:
            messagebox.showwarning("توجه", "این فرد قبلا ثبت نام شده است")

    def GetSelectionCustomer(self, e):
        SelectRow = self.tblCustomer.selection()
        # print(SelectRow)
        if SelectRow != ():
            print(self.tblCustomer.item(SelectRow)["values"])

            idrow = self.tblCustomer.item(SelectRow)["values"][5]
            self.varCustomer_Id.set(idrow)

            firstnamerow = self.tblCustomer.item(SelectRow)["values"][4]
            self.varFirstname.set(firstnamerow)

            lastnamerow = self.tblCustomer.item(SelectRow)["values"][3]
            self.varLastname.set(lastnamerow)

            phonerow = self.tblCustomer.item(SelectRow)["values"][2]
            self.varPhone.set(phonerow)

            adressrow = self.tblCustomer.item(SelectRow)["values"][1]
            self.varAdress.set(adressrow)

            daterow = self.tblCustomer.item(SelectRow)["values"][0]
            self.varRegDate.set(daterow)



    def DeleteCustomer(self):
        ask = messagebox.askyesno("توجه", f"آیا از حذف داده{self.varCustomer_Id.get()} مطمین هستید؟ ")
        # print(self.varCustomer_Id.get())
        if ask == True:
            objbl = BlDaroo()
            result = objbl.blDelete(Customer, self.varCustomer_Id.get())
            if result == True:
                self.loadCustomer()
                messagebox.showinfo("صحیح", "عملیات حذف با موفقیت انجام شد")
            else:
                messagebox.showerror("خطا", "عملیات حذف ناموفق")

    def EditCustomer(self):
        if self.isExistCustomer() == True:
            objbl = BlDaroo()
            # آپدیت در جدول دیتابیس
            result = objbl.blUpdateDynamicCustomer(Customer, self.varCustomer_Id.get(),
                                                   first_name=self.varFirstname.get(),
                                                   last_name=self.varLastname.get(),
                                                   phone_number=self.varPhone.get(),
                                                   adress=self.varAdress.get(),
                                                   registration_date=self.varRegDate.get())
            if result == True:
                # آپدیت در جدول فرم
                self.loadCustomer()
                messagebox.showinfo("صحیح", "ویرایش با موفقیت انجام شد")
            else:
                messagebox.showerror("خطا", "ویرایش ناموفق")
        else:
            messagebox.showerror("خطا", "فردی با این اطلاعات قبلا ثبت شده است")

    def SearchCustomer(self):
        srch = self.varSearchCustomer.get()
        if srch == "":
            self.loadCustomer()
        else:
            objbl = BlDaroo()
            result = objbl.blSearch(Customer, srch)
            if result != []:
                for item in self.tblCustomer.get_children():
                    self.tblCustomer.delete(item)
                for item in result:
                    self.tblCustomer.insert("", "end", values=[item.registration_date,
                                                               item.adress,
                                                               item.phone_number,
                                                               item.last_name,
                                                               item.first_name,
                                                               item.customer_id])

    def report(self):
        d1 = self.vardate1.get()
        d2 = self.vardate2.get()
        startdate = jdatetime.datetime.strptime(d1, "%Y-%m-%d").strftime("%Y-%m-%d")
        enddate = jdatetime.datetime.strptime(d2, "%Y-%m-%d").strftime("%Y-%m-%d")
        objbl = BlDaroo()
        r = objbl.blreport(Customer, startdate, enddate)
        print(r)
        for item in self.tblCustomer.get_children():
            self.tblCustomer.delete(item)
        for item in r:
            self.tblCustomer.insert("", "end", values=[item.registration_date,
                                                       item.adress,
                                                       item.phone_number,
                                                       item.last_name,
                                                       item.first_name,
                                                       item.customer_id])

    def AddCustomerToInvoice(self):
        self.varCustomerNameIn.set(self.varFirstname.get() + "  " + self.varLastname.get())
        self.varCustomerCodeIn.set(self.varCustomer_Id.get())


    # ////////////////////////////////////توابع فریم داروها////////////////////////////

    def ShowProductFrame(self):
        self.ProductFrame.place(relx=0.18, rely=0.04)
        self.CustomerFrame.place_forget()
        self.InvoicesFrame.place_forget()
        # self.ReminderFrame.place_forget()
        # self.frmSetting.place_forget()
        self.loadProduct()

    def CloseProductFrame(self):
        # self.lbl_bg.place_forget()
        # self.lbl_welcome.place_forget()
        self.ProductFrame.place_forget()

    def hide_text_Product(self):
        self.lblProduct.place_forget()

    def show_text_Product(self, text):
        if text == "ثبت نام":
            self.lblProduct.place(relx=0.03, rely=0.05)
            self.lblProduct.configure(text=text)
        elif text == "ویرایش":
            self.lblProduct.place(relx=0.03, rely=0.19)
            self.lblProduct.configure(text=text)
        elif text == "حذف":
            self.lblProduct.place(relx=0.05, rely=0.33)
            self.lblProduct.configure(text=text)

    def GetSelectionProduct(self, e):
        SelectRow = self.tblProduct.selection()
        if SelectRow:
            value = self.tblProduct.item(SelectRow, "values")
            # print(value)
            self.varProductId.set(value[9])
            self.varGeneric.set(value[8])
            self.varTejari.set(value[7])
            self.varDooz.set(value[6])
            self.varDasteh.set(value[5])
            self.varShekl.set(value[4])
            self.varEngheza.set(value[3])
            self.varPrice.set(value[2])
            self.varSefaresh_Aval.set(value[1])
            self.varMojodi.set(value[0])


    def loadProduct(self):
        self.tblProduct.tag_configure("evenrow", background="#FFE5EC")
        self.tblProduct.tag_configure("oddrow", background="white")
        for item in self.tblProduct.get_children():
            self.tblProduct.delete(item)
        objbl = BlDaroo()
        lstProducts = objbl.blReadProduct(Product)
        # print(lstCustomers)
        # print(lstCustomers[0])
        # print(lstCustomers[0].first_name)
        for index, item in enumerate(lstProducts):
            if index % 2 == 0:
                self.tblProduct.insert("", "end", values=[item.mojodi,item.sefareshAval,item.price,item.engheza,item.shekl,item.dasteh,item.dooz,item.tejari,item.generic,
                                                          item.product_id],tags=("evenrow",))
            else:
                self.tblProduct.insert("", "end",values=[item.mojodi,item.sefareshAval, item.price, item.engheza, item.shekl, item.dasteh, item.dooz,item.tejari,item.generic,
                                                         item.product_id],tags=("oddrow",))


    def isExistProduct(self):
        objpd = Product(generic=self.varGeneric.get(),
                        tejari=self.varTejari.get(),
                        dooz=self.varDooz.get(),
                        dasteh=self.varDasteh.get(),
                        shekl=self.varShekl.get(),
                        engheza=self.varEngheza.get(),
                        price=self.varPrice.get(),
                        sefareshAval=self.varSefaresh_Aval.get(),
                        mojodi=self.varMojodi.get())
        objbl = BlDaroo()
        return objbl.blExistProduct(Product, objpd)

    def RegistrationProduct(self):
        if self.isExistProduct():
            objpd = Product(generic=self.varGeneric.get(),
                        tejari=self.varTejari.get(),
                        dooz=self.varDooz.get(),
                        dasteh=self.varDasteh.get(),
                        shekl=self.varShekl.get(),
                        engheza=self.varEngheza.get(),
                        price=self.varPrice.get(),
                        sefareshAval=self.varSefaresh_Aval.get(),
                        mojodi=self.varMojodi.get())
            objbl = BlDaroo()
            result = objbl.blAdd(objpd)
            if result == True:
                self.loadProduct()
                messagebox.showinfo("صحیح", "ثبت نام با موفقیت انجام شد")
                self.varGeneric.set("")
                self.varTejari.set("")
                self.varDooz.set("")
                self.varDasteh.set("")
                self.varShekl.set("")
                self.varEngheza.set("")
                self.varPrice.set("")
                self.varSefaresh_Aval.set("")
                self.varMojodi.set("")
                self.txtGeneric.focus_set()

        else:
            messagebox.showwarning("توجه", "این محصول قبلا ثبت شده است")



    def DeleteProduct(self):
        ask = messagebox.askyesno("توجه", f"آیا از حذف داده{self.varProductId.get()} مطمین هستید؟ ")
        # print(self.varProductId.get())
        if ask == True:
            objbl = BlDaroo()
            result = objbl.blDeleteProduct(Product, self.varProductId.get())
            if result == True:
                self.loadProduct()
                messagebox.showinfo("صحیح", "عملیات حذف با موفقیت انجام شد")
            else:
                messagebox.showerror("خطا", "عملیات حذف ناموفق")

    def EditProduct(self):
        if self.isExistProduct() == True:
            objbl = BlDaroo()
            # آپدیت در جدول دیتابیس
            result = objbl.blUpdateDynamicProduct(Product, self.varProductId.get(),
                                           generic=self.varGeneric.get(),
                                           tejari=self.varTejari.get(),
                                           dooz=self.varDooz.get(),
                                           dasteh=self.varDasteh.get(),
                                           shekl=self.varShekl.get(),
                                           engheza=self.varEngheza.get(),
                                           price=self.varPrice.get(),
                                           sefareshAval=self.varSefaresh_Aval.get(),
                                           mojodi=self.varMojodi.get())

            if result == True:
                # آپدیت در جدول فرم
                self.loadProduct()
                messagebox.showinfo("صحیح", "ویرایش با موفقیت انجام شد")
            else:
                messagebox.showerror("خطا", "ویرایش ناموفق")
        else:
            messagebox.showerror("خطا", "محصولی با این اطلاعات قبلا ثبت شده است")

    def AddProductToInvoice(self):
        self.varProductCodeIn.set(self.varProductId.get())
        self.varGenericNameIn.set(self.varGeneric.get())
        self.varSheklDarooIn.set(self.varShekl.get())
        self.varProductPriceIn.set(self.varPrice.get())


    # /////////////////////////////توابع فریم فاکتورها/////////////////////////////////

    def ShowInvoicesFrame(self):
        self.InvoicesFrame.place(relx=0.17, rely=0.07)
        # self.lbl_welcome.place_forget()
        self.CustomerFrame.place_forget()
        self.ProductFrame.place_forget()
        # self.ReminderFrame.place_forget()
        # self.frmSetting.place_forget()
        self.txtInvoicedate.delete(0, "end")
        self.txtInvoicedate.insert(0, get_shamsidate())
        self.loadInvoice()

    def CloseInvoicesFrame(self):
        # self.lbl_bg.place_forget()
        # self.lbl_welcome.place_forget()
        self.InvoicesFrame.place_forget()


    def hide_text_Invoices(self):
        self.lblInvoice.place_forget()

    def show_text_Invoices(self, text):
        if text == "ثبت فاکتور":
            self.lblInvoice.place(relx=0.02, rely=0.18)
            self.lblInvoice.configure(text=text)


    def hide_text_RegStore(self):
        self.lblInvoice.place_forget()

    def show_text_RegStore(self, text):
        if text == "ثبت انبار":
            self.lblInvoice.place(relx=0.04, rely=0.05)
            self.lblInvoice.configure(text=text)


    def Calculate_Price(self, event):
        result = int(self.comboProductNumberIn.get()) * int(self.varProductPriceIn.get())
        print(result)
        self.varProductAllPriceIn.set(str(result))


    def loadInvoice(self):
        self.tblInvoice.tag_configure("evenrow", background="#FCF6BD")
        self.tblInvoice.tag_configure("oddrow", background="white")
        for item in self.tblInvoice.get_children():
            self.tblInvoice.delete(item)
        objbl = BlDaroo()
        lstInvoices = objbl.blRead(Invoice)
        # print(lstCustomers)
        # print(lstCustomers[0])
        # print(lstCustomers[0].first_name)
        for index, item in enumerate(lstInvoices):
            if index % 2 == 0:
                self.tblInvoice.insert("", "end", values=[item.date,item.total_price,item.one_price,item.shekl_daroo,item.generic_name,item.customer_name,
                                                      item.number,item.product_id,item.customer_id,
                                                      item.invoice_id],tags=("evenrow",))
            else:
                self.tblInvoice.insert("", "end", values=[item.date, item.total_price, item.one_price, item.shekl_daroo,item.generic_name, item.customer_name,
                                                      item.number, item.product_id, item.customer_id,
                                                      item.invoice_id], tags=("oddrow",))



    def isExistInvoice(self):
        objpd = Invoice(customer_id=self.varCustomerCodeIn.get(),
                        product_id=self.varProductCodeIn.get(),
                        number=self.comboProductNumberIn.get(),
                        customer_name=self.varCustomerNameIn.get(),
                        generic_name=self.varGenericNameIn.get(),
                        shekl_daroo=self.varSheklDarooIn.get(),
                        one_price=self.varProductPriceIn.get(),
                        total_price=self.varProductAllPriceIn.get(),
                        date=self.varInvoicedate.get())
        objbl = BlDaroo()
        return objbl.blExistInvoice(Invoice, objpd)

    def RegistrationInvoice(self):
        if (self.varCustomerCodeIn.get() and self.varProductCodeIn.get()
            and self.comboProductNumberIn.get() and self.varCustomerNameIn.get()
            and self.varGenericNameIn.get() and self.varSheklDarooIn.get()
            and self.varProductPriceIn.get() and self.varProductAllPriceIn.get()
            and self.varInvoicedate.get())=="":
            messagebox.showwarning("هشدار", "هیچکدام از فیلدها نمی تواند خالی باشد")
            return
        if self.isExistInvoice():
            objIn = Invoice(customer_id=self.varCustomerCodeIn.get(),
                        product_id=self.varProductCodeIn.get(),
                        number=self.comboProductNumberIn.get(),
                        customer_name=self.varCustomerNameIn.get(),
                        generic_name=self.varGenericNameIn.get(),
                        shekl_daroo=self.varSheklDarooIn.get(),
                        one_price=self.varProductPriceIn.get(),
                        total_price=self.varProductAllPriceIn.get(),
                        date=self.varInvoicedate.get())
            objbl = BlDaroo()
            result = objbl.blAdd(objIn)
            if result == True:
                self.loadInvoice()
                messagebox.showinfo("صحیح", "ثبت فاکتور با موفقیت انجام شد")
                self.varCustomerCodeIn.set(0)
                self.varProductCodeIn.set(0)
                self.comboProductNumberIn.set(0)
                self.varCustomerNameIn.set("")
                self.varGenericNameIn.set("")
                self.varSheklDarooIn.set("")
                self.varProductPriceIn.set("")
                self.varProductAllPriceIn.set("")

                self.varGeneric.set("")
                self.varTejari.set("")
                self.varDooz.set("")
                self.varDasteh.set("")
                self.varShekl.set("")
                self.varEngheza.set("")
                self.varPrice.set("")
                self.varSefaresh_Aval.set("")
                self.varMojodi.set("")

                self.varFirstname.set("")
                self.varLastname.set("")
                self.varPhone.set("")
                self.varAdress.set("")
        else:
            messagebox.showwarning("توجه", "این فاکتور قبلا برای این مشتری ثبت شده است")



# ___________________________مربوط به موجودیت انبار___________________________

    def Check_Mojodiat(self):
        drug_name=self.txtGeneric.get()
        try:
            amount=int(self.comboProductNumberIn.get())
        except ValueError:
            messagebox.showerror("خطا","عدد معتبر وارد کنید")
            return
        result=forosh_daroo(drug_name,amount)
        if result["status"]=="success":
            messagebox.showinfo("موفق",result["msg"])
        elif result["status"]=="warning":
            messagebox.showwarning("هشدار", result["msg"])
        else:
            messagebox.showerror("خطا", result["msg"])


# ------------------------------------ساخت پنجره جدید------------------------------------------

    def show_mojoodi_window(self):
        top=CTkToplevel(self)
        top.title("موجودی انبار")
        top.geometry("555x610+350+50")

        # -----------این بخش برای حل مشکلت------------
        top.lift()  # پنجره رو بیاره بالا
        top.focus_force()  # فوکوس رو بده به این پنجره
        top.attributes("-topmost", True)  # همیشه بالای بقیه باشه
        top.after(10, lambda: top.attributes("-topmost", False))
        # این خط برای اینکه فقط بار اول بالا بمونه و بعد مثل پنجره عادی بشه

        var_top = StringVar()
        txt_top = CTkEntry(top, textvariable=var_top, fg_color="white", text_color="black",font=("Vazir", 18), width = 200)
        txt_top.place(relx=0.245, rely=0.94)

        tree=ttk.Treeview(top,columns=("name","tejari","dooz","shekl","mojodi"),show="headings",height=27)
        tree.heading("name",text="نام دارو")
        tree.column("name", width=140, anchor=CENTER)
        tree.heading("tejari", text="نام تجاری")
        tree.column("tejari", width=140, anchor=CENTER)
        tree.heading("dooz", text="دوز")
        tree.column("dooz", width=90, anchor=CENTER)
        tree.heading("shekl", text="شکل دارویی")
        tree.column("shekl", width=110, anchor=CENTER)
        tree.heading("mojodi",text="موجودی")
        tree.column("mojodi", width=60, anchor=CENTER)
        tree.place(relx=0.01,rely=0.0)


        # def load_mojoodi_window(filter_text=""):
        #     tree.tag_configure("low", background="red")
        #     tree.tag_configure("half", background="orange")
        #     tree.tag_configure("normal", background="white")
        #
        #     tree.delete(*tree.get_children())
        #     all_drugs=get_All_Daroo()
        #
        #     for item in all_drugs:
        #         if filter_text.lower() in item.generic.lower():
        #             if item.mojodi <= 20:
        #                 tag = "low"
        #             elif item.mojodi <= 50:  # مثلا بین 21 تا 50
        #                 tag = "half"
        #             else:
        #                 tag = "normal"
        #             tree.insert("", "end", values=(item.generic,item.tejari,item.dooz,item.shekl, item.mojodi), tags=(tag,))


        # def load_mojoodi_window(filter_text=""):
        #     # تعریف رنگ‌ها و بازه‌ها به صورت لیست از دیکشنری
        #     ranges = [
        #         {"max": 20, "tag": "low", "color": "red"},
        #         {"max": 50, "tag": "half", "color": "orange"},
        #         {"max": float('inf'), "tag": "normal", "color": "white"}
        #     ]
        #
        #     # پیکربندی تگ‌ها
        #     for r in ranges:
        #         tree.tag_configure(r["tag"], background=r["color"])
        #
        #     tree.delete(*tree.get_children())
        #     all_drugs = get_All_Daroo()
        #
        #     for item in all_drugs:
        #         if filter_text.lower() in item.generic.lower():
        #             # پیدا کردن تگ مناسب بر اساس موجودی
        #             for r in ranges:
        #                 if item.mojodi <= r["max"]:
        #                     tag = r["tag"]
        #                     break
        #             tree.insert("", "end", values=(item.generic, item.tejari, item.dooz, item.shekl, item.mojodi),
        #                         tags=(tag,))


        def load_mojoodi_window(filter_text=""):
            tree.delete(*tree.get_children())
            all_drugs = get_All_Daroo()

            # پیدا کردن بیشترین موجودی برای نسبت‌دهی رنگ
            max_mojodi = max(item.mojodi for item in all_drugs) if all_drugs else 1

            for item in all_drugs:
                if filter_text.lower() in item.generic.lower():
                    percent = (item.mojodi / max_mojodi) * 100  # درصد موجودی نسبت به بیشترین موجودی

                    if percent <= 20:
                        tag = "low"
                        color = "red"
                    elif percent <= 50:
                        tag = "half"
                        color = "orange"
                    else:
                        tag = "normal"
                        color = "white"

                    tree.tag_configure(tag, background=color)
                    tree.insert("", "end", values=(item.generic, item.tejari, item.dooz, item.shekl, item.mojodi),
                                tags=(tag,))

        # def load_mojoodi_window(filter_text=""):
        #     tree.delete(*tree.get_children())
        #     all_drugs = get_All_Daroo()
        #
        #     # پیدا کردن بیشترین موجودی برای نسبت‌ دهی رنگ
        #     max_mojodi = max(item.mojodi for item in all_drugs) if all_drugs else 1
        #
        #     for item in all_drugs:
        #         if filter_text.lower() in item.generic.lower():
        #             percent = item.mojodi / max_mojodi  # درصد بین 0 و 1
        #
        #             # تبدیل درصد به رنگ طیفی از قرمز (کم) به سبز (زیاد)
        #             red = int(255 * (1 - percent))
        #             green = int(255 * percent)
        #             color = f'#{red:02x}{green:02x}00'  # رنگ به فرمت HEX
        #
        #             tag = f"color_{item.generic}"  # هر دارو یک تگ منحصر بفرد
        #             tree.tag_configure(tag, background=color)
        #
        #             tree.insert("", "end", values=(item.generic, item.tejari, item.dooz, item.shekl, item.mojodi),
        #                         tags=(tag,))

        label_search= CTkLabel(top, text="جستجو",font=("Vazir", 21),text_color="white",width=90)
        label_search.place(relx=0.61,rely=0.94)
        # ,command = lambda: load_mojoodi_window(var_top.get()) اگه میخواستیم با دکمه کار کنه
        var_top.trace_add("write", lambda *args: load_mojoodi_window(var_top.get()))

        load_mojoodi_window()



    # /////////////////////////////////////توابع مربوط به لاگین//////////////////////////////////
    def ShowHide(self):
        if self.txtPass.cget("show") == "*":
            self.txtPass.configure(show="")
        else:
            self.txtPass.configure(show="*")

    def Login(self):
        objl = Login("", self.txtUser.get(), self.txtPass.get(), "")
        objbl = BlDaroo()
        result = objbl.blLogin(Login, objl)
        # print(result)
        # print(result[0])
        # print(result[0].role)
        if result != False:
            if result[0].role == "مدیر":
                self.loginframe.place_forget()
                self.contentframe.place(relx=0.0,rely=0.0)
            if result[0].role == "پرسنل":
                self.loginframe.place_forget()
                self.contentframe.place(relx=0.0, rely=0.0)
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمزعبور اشتباه است")


    def Enter(self):
        self.loginframe.place(relx=0.0, rely=0.0)