from tkinter import *
from tkinter import messagebox
import tempfile
import os
from tinydb import TinyDB, Query
db = TinyDB('db.json')
#import pyrebase                                                                                 #import the pyrebase module which allows us to communicate with the firebase servers.
from time import sleep
import smtplib
import mysql.connector
mobile = 0
def openbill(mobile, crate_no):
    # mysql data
    
    mydb = mysql.connector.connect(
      host="localhost",
      user="admin",
      password="pi",
      database="mydatabase"
    )

    mycursor = mydb.cursor()
    #Email Variables
    SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
    SMTP_PORT = 587 #Server Port (don't change!)
    GMAIL_USERNAME = 'smartshop.3765@gmail.com' #change this to match your gmail account
    GMAIL_PASSWORD = 'wyajvfhlobjyrtmd'  #change this to match your gmail app-password


    sql = "SELECT name from shop WHERE phone_no = %s"
    info = (mobile,)
    mycursor.execute(sql, info)
    name = mycursor.fetchone()[0]
    sql = "SELECT password from shop WHERE phone_no = %s"
    info = (mobile,)
    mycursor.execute(sql, info)
    password = mycursor.fetchone()[0]
    sql = "SELECT email from shop WHERE name = %s"
    info = (name,)
    mycursor.execute(sql, info)
    c_mail = mycursor.fetchone()[0]
    total_bill = 0

    class Emailer:
        def sendmail(self, recipient, subject, content):

            #Create Headers
            headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                       "MIME-Version: 1.0", "Content-Type: text/html"]
            headers = "\r\n".join(headers)

            #Connect to Gmail Server
            session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            session.ehlo()
            session.starttls()
            session.ehlo()

            #Login to Gmail
            session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

            #Send Email & Exit
            session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
            session.quit
            

    config = {                                                             #define a dictionary named config with several key-value pairs that configure the connection to the database.
      "apiKey": "AIzaSyAEs6ayyqojMgfiNl-p4OqdwfIS2ztGKaE",
      "authDomain": "test-e8b6a.firebaseapp.com",
      "databaseURL": "https://test-e8b6a-default-rtdb.firebaseio.com",
      "storageBucket": "test-e8b6a.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    
    
    
    user = Query()

    trolley = crate_no

    root=Toplevel()
    root.title('Billing Manangement System')
    root.geometry('1280x700')
    bg_color='#2D9290'


    #=====================variables===================
    database = firebase.database()
    crate = database.child(trolley)
    biscuit_int = crate.child("biscuit").get().val()
    crate = database.child(trolley)
    maggi_int = crate.child("maggi").get().val()
    crate = database.child(trolley)
    chips_int = crate.child("chips").get().val()
    crate = database.child(trolley)
    chocolate_int = crate.child("chocolate").get().val()
    chips = IntVar()
    chocolate = IntVar()
    maggi = IntVar()
    biscuit = IntVar()
    Total = IntVar()
    chocolate.set(chocolate_int)
    maggi.set(maggi_int)
    chips.set(chips_int)
    biscuit.set(biscuit_int)

    ch=StringVar()
    b=StringVar()
    c=StringVar()
    m=StringVar()
    total_cost=StringVar()
    # ===========Function===============
    def total():
        if biscuit.get()==0 and maggi.get()==0 and chocolate.get()==0 and chips.get()==0:
            messagebox.showerror('Error','Please select number of quantity')
        else:
            Ch=chocolate.get()
            C=chips.get()
            M=maggi.get()
            B=biscuit.get()

            t=float(Ch*10+C*25+M*12+B*10)
            Total.set(Ch + C + M + B)
            total_cost.set(str(round(t, 2)))

            ch.set(str(round(Ch * 10, 2)))
            c.set(str(round(C*25,2)))
            m.set(str(round(M*12,2)))
            b.set(str(round(B*10,2)))



    def inventory():
        items = ["chips","chocolate","maggi","biscuit"]

        for item in items:
            database = firebase.database()                                        #take an instance from the firebase database which is pointing to the root directory of your database.
            crate = database.child(trolley)                        #get the child "RGBControl" path in your database and store it inside the "RGBControlBucket" variable.
            quantity_ = crate.child(item).get().val()
            result = db.get(Query()['item'] == item)
            leftover = int(result.get('quantity'))
            leftover = leftover - quantity_
            db.update({'quantity': leftover}, user.item == item)


    def receipt():
        textarea.delete(1.0,END)
        textarea.insert(END,' Items\tNumber of Items\t  Cost of Items\n')
        textarea.insert(END,f'\nchips\t\t{chips.get()}\t  {c.get()}')
        textarea.insert(END,f'\n\nchocolate\t\t{chocolate.get()}\t  {ch.get()}')
        textarea.insert(END,f'\n\nmaggi\t\t{maggi.get()}\t  {m.get()}')
        textarea.insert(END,f'\n\nbiscuit\t\t{biscuit.get()}\t  {b.get()}')
        textarea.insert(END, f"\n\n================================")
        textarea.insert(END,f'\nTotal Price\t\t{Total.get()}\t₹{total_cost.get()}')
        textarea.insert(END, f"\n================================")


    def print():
        q=textarea.get('1.0','end-1c')
        filename=tempfile.mktemp('.txt')
        open(filename,'w').write(q)
        os.startfile(filename,'Print')

    def email_sent():
        sender = Emailer()

        sendTo = c_mail
        emailSubject = "Smart Shop"
        content = "Thank you "+ name +" for shopping with us! Your bill was " + str(total_cost.get()) + " ruppees."
        emailContent = content

        sender.sendmail(sendTo, emailSubject, emailContent)

    def reset():
        textarea.delete(1.0,END)
        Bread.set(0)
        Wine.set(0)
        Rice.set(0)
        Gal.set(0)
        Total.set(0)

        cb.set('')
        cw.set('')
        cr.set('')
        cg.set('')
        total_cost.set('')

    def update_balance(bill):
        sql = "SELECT balance from shop WHERE name = %s"
        info = (name,)
        mycursor.execute(sql, info)
        debt = mycursor.fetchone()

        total = int(debt[0]) - bill
        sql = "UPDATE shop SET balance = %s WHERE name = %s"
        information = (total, name)

        mycursor.execute(sql,information)
        mydb.commit()
        
    def pay():
        receipt()
        inventory()
        email_sent()
        security()
    def exit():
        if messagebox.askyesno('Exit','Do you really want to exit'):
            root.destroy()

    title=Label(root,pady=5,text="Billing Manangement System",bd=12,bg=bg_color,fg='white',font=('times new roman', 35 ,'bold'),relief=GROOVE,justify=CENTER)
    title.pack(fill=X)

    #===============Product Details=================
    F1 = LabelFrame(root, text='Product Details', font=('times new romon', 18, 'bold'), fg='gold',bg=bg_color,bd=15,relief=RIDGE)
    F1.place(x=5, y=90,width=1270,height=500)

    #=====================Heading==========================
    itm=Label(F1, text='Items', font=('Helvetic',25, 'bold','underline'), fg='black',bg=bg_color)
    itm.grid(row=0,column=0,padx=20,pady=15)

    n=Label(F1, text='Number of Items', font=('Helvetic',25, 'bold','underline'), fg='black',bg=bg_color)
    n.grid(row=0,column=1,padx=30,pady=15)

    cost=Label(F1, text='Cost of Items', font=('Helvetic',25, 'bold','underline'), fg='black',bg=bg_color)
    cost.grid(row=0,column=2,padx=30,pady=15)

    #===============Product============

    Chips=Label(F1, text='Chips', font=('times new rommon',20, 'bold'), fg='lawngreen',bg=bg_color)
    Chips.grid(row=1,column=0,padx=20,pady=15)
    b_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=chips,justify=CENTER)
    b_txt.grid(row=1,column=1,padx=10,pady=15)
    cb_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=c,justify=CENTER)
    cb_txt.grid(row=1,column=2,padx=10,pady=15)

    Chocolate=Label(F1, text='Chocolate', font=('times new rommon',20, 'bold'), fg='lawngreen',bg=bg_color)
    Chocolate.grid(row=2,column=0,padx=20,pady=15)
    w_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=chocolate,justify=CENTER)
    w_txt.grid(row=2,column=1,padx=20,pady=15)
    cw_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=ch,justify=CENTER)
    cw_txt.grid(row=2,column=2,padx=20,pady=15)

    Maggi=Label(F1, text='Maggi', font=('times new rommon',20, 'bold'), fg='lawngreen',bg=bg_color)
    Maggi.grid(row=3,column=0,padx=20,pady=15)
    r_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=maggi,justify=CENTER)
    r_txt.grid(row=3,column=1,padx=20,pady=15)
    cr_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=m,justify=CENTER)
    cr_txt.grid(row=3,column=2,padx=20,pady=15)

    Biscuit=Label(F1, text='Biscuit', font=('times new rommon',20, 'bold'), fg='lawngreen',bg=bg_color)
    Biscuit.grid(row=4,column=0,padx=20,pady=15)
    g_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=biscuit,justify=CENTER)
    g_txt.grid(row=4,column=1,padx=20,pady=15)
    cg_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=b,justify=CENTER)
    cg_txt.grid(row=4,column=2,padx=20,pady=15)

    t=Label(F1, text='Total', font=('times new rommon',20, 'bold'), fg='lawngreen',bg=bg_color)
    t.grid(row=5,column=0,padx=20,pady=15)
    t_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=Total,justify=CENTER)
    t_txt.grid(row=5,column=1,padx=20,pady=15)
    totalcost_txt=Entry(F1,font='arial 15 bold',relief=SUNKEN,bd=7,textvariable=total_cost,justify=CENTER)
    totalcost_txt.grid(row=5,column=2,padx=20,pady=15)

    #=====================Bill area====================
    F2=Frame(root,relief=GROOVE,bd=10)
    F2.place(x=920,y=120,width=330,height=900)
    bill_title=Label(F2,text='Receipt',font='arial 11 bold',bd=7,relief=GROOVE).pack(fill=X)
    scrol_y=Scrollbar(F2,orient=VERTICAL)
    scrol_y.pack(side=RIGHT,fill=Y)
    textarea=Text(F2,font='arial 11',yscrollcommand=scrol_y.set)
    textarea.pack(fill=BOTH)
    scrol_y.config(command=textarea.yview)
    
    def wallet():
        receipt()
        inventory()
        update_balance(total_bill)
        email_sent()
        security()
    
    def verify(entry,Pass):
        
        if(entry == Pass):
            wallet()
    def security():
        update = ""
        if(chips_int == 0):
            update += "0"
        else:
            update += "1"
        if(maggi_int == 0):
            update += "0"
        else:
            update += "1"
        if(chocolate_int == 0):
            update += "0"
        else:
            update += "1"
        if(biscuit_int == 0):
            update += "0"
        else:
            update += "1"
        data = {
            "id": update,
        }
        database.child("rfid_security").set(data)
        
    def openpass(password):
        w4 = Toplevel()
        w4.title("Enter")
        w4.geometry("500x200")
        w4.configure(bg="#2d9290")
        
        pframe=Frame(w4,bd=5,relief=GROOVE)
        pframe.place(x=50,y=45,width=360,height=60)
        
        plabel=Label(pframe,text="password: " ,font=("Times New Roman",15))
        plabel.place(x=5,y=12)
        
        enpass= Entry(pframe,font=("Times New Roman",15),bd=5,relief=GROOVE,bg="#2d9290")
        enpass.place(x=120,y=8)
        
        enterbtn=Button(w4,text="Enter" , font=("Times New Roman",15),bd=5,relief=GROOVE, command=lambda:verify(enpass.get(),password))
        enterbtn.place(x=190,y=130,width=100)
    
    #=====================Buttons========================
    F3 =Frame(root,bg=bg_color,bd=15,relief=RIDGE)
    F3.place(x=5, y=570,width=1270,height=120)

    btn1 = Button(F3, text='PAY', font='arial 25 bold', padx=5, pady=5, bg='black',fg='white',width=29,command=pay)
    btn1.grid(row=0,column=0,padx=20,pady=15)

    btn2 = Button(F3, text='WALLET', font='arial 25 bold', padx=15, pady=5, bg='black',fg='white',width=29,command=lambda:openpass(password))
    btn2.grid(row=0,column=1,padx=20,pady=10)

    total()
    total_bill = int(chips_int*25+chocolate_int*10+maggi_int*12+biscuit_int*10)
    root.mainloop()
    

def bookin():
    
    w2=Toplevel()
    w2.configure(bg='#2d9290')
    w2.title("Customer Registeration")
    w2.geometry("1980x1080")
        
    headingFrame1 = Frame(w2)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Customer Registeration",bg='white', fg='black', font=('Times New Roman',30),bd=10,relief=GROOVE)
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(w2,bd=15,relief=GROOVE)
    labelFrame.place(relx=0.15,rely=0.35,relwidth=0.7,relheight=0.33)


    lb1 = Label(labelFrame,text="Name : ", fg='black',font=('Times New Roman',20))
    lb1.place(x=80,y=20)
            
    bookInfo2 = Entry(labelFrame,font=('Times New Roman',20),bg='#2d9290',bd=5,relief=GROOVE)
    bookInfo2.place(x=370,y=20,width=750)
            
    lb2 = Label(labelFrame,text="Phone : ", fg='black',font=('Times New Roman',20))
    lb2.place(x=80,y=90)
            
    bookInfo3 = Entry(labelFrame,font=('Times New Roman',20),bg='#2d9290',bd=5,relief=GROOVE)
    bookInfo3.place(x=370,y=90,width=750)
            
    lb3 = Label(labelFrame,text="Email : ", fg='black',font=('Times New Roman',20))
    lb3.place(x=80,y=160)
            
    bookInfo4 = Entry(labelFrame,font=('Times New Roman',20),bd=5,bg='#2d9290',relief=GROOVE)
    bookInfo4.place(x=370,y=160,width=750)
    
    lb4 = Label(labelFrame,text="Password : ", fg='black',font=('Times New Roman',20))
    lb4.place(x=80,y=230)
            
    bookInfo5 = Entry(labelFrame,font=('Times New Roman',20),bd=5,bg='#2d9290',relief=GROOVE)
    bookInfo5.place(x=370,y=230,width=750)
    
    def enter(a,b,c,d):
        mydb = mysql.connector.connect(
          host="localhost",
          user="admin",
          password="pi",
          database="mydatabase"
        )
        mycursor = mydb.cursor()
        print(type(b))
        sql = "INSERT INTO shop (name, phone_no, email, balance, password) VALUES (%s, %s, %s, %s, %s)"
        val = (a,b,c, 0, d)
        mycursor.execute(sql, val)

        mydb.commit()
    def opencart(mobile):
        w5 = Toplevel()
        w5.title("Enter your Cart Number")
        w5.geometry("400x200")
        w5.configure(bg="#2d9290")

        cartframe=Frame(w5,bd=5,relief=GROOVE)
        cartframe.place(x=50,y=45,width=300,height=60)

        cartlabel=Label(cartframe,text="Enter cart number: " ,font=("Times New Roman",15))
        cartlabel.place(x=5,y=12)

        enpass= Entry(cartframe,font=("Times New Roman",15),bd=5,relief=GROOVE,bg="#2d9290")
        enpass.place(x=180,y=8,width=90)

        cartbtn=Button(w5,text="Enter" , font=("Times New Roman",15),bd=5,relief=GROOVE,command=lambda:openbill(mobile, enpass.get()))
        cartbtn.place(x=150,y=130,width=100)
    rbtn = Button(w2,text="Register", fg='black',font=('Times New Roman',20),command=lambda: [enter(bookInfo2.get(), bookInfo3.get(), bookInfo4.get(), bookInfo5.get()),opencart(bookInfo3.get())])
    rbtn.config(bd=10,relief=GROOVE)
    rbtn.place(relx=0.25,rely=0.80, relwidth=0.5,relheight=0.08)


w1 = Tk()
w1.title("Smart Store")
w1.minsize(width=400,height=400)
w1.geometry("1980x1080")
w1.configure(bg='#2d9290')

def shift():
    x1,y1,x2,y2 = canvas.bbox("canv")
    if(x2<0 or y1<0): 
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height()//2
        canvas.coords("canv",x1,y1)
    else:
        canvas.move("canv", -2, 0)
    canvas.after(1000//fps,shift)

canvas=Canvas(w1,bg='#2d9290')
canvas.config(bd=12,relief=GROOVE)
canvas.pack(pady=100)

text_var="Welcome to Smart Shopping Store"
text=canvas.create_text(0,-2000,text=text_var,font=('Times New Roman',50,'bold'),fill='black',tags=("canv",),anchor='w')
x1,y1,x2,y2 = canvas.bbox("canv")
width = x2-x1
height = y2-y1
canvas['width']=width
canvas['height']=height
fps=40    
shift()

headingLabel = Label(w1, text="Enter Mobile Number:", fg='black', font=('Times New Roman',30,"underline"),bg='#2d9290')
headingLabel.pack(pady=50)


bookInfo1 = Entry(w1,bd=10,relief=GROOVE)
bookInfo1.config(font=("Times New Roman",25),width=30)
bookInfo1.pack(pady=70)

def opencart(mobile):
        w5 = Toplevel()
        w5.title("Enter your cart number")
        w5.geometry("400x200")
        w5.configure(bg="#2d9290")

        cartframe=Frame(w5,bd=5,relief=GROOVE)
        cartframe.place(x=50,y=45,width=300,height=60)

        cartlabel=Label(cartframe,text="Enter cart number: " ,font=("Times New Roman",15))
        cartlabel.place(x=5,y=12)

        enpass= Entry(cartframe,font=("Times New Roman",15),bd=5,relief=GROOVE,bg="#2d9290")
        enpass.place(x=180,y=8,width=90)

        cartbtn=Button(w5,text="Enter" , font=("Times New Roman",15),bd=5,relief=GROOVE,command=lambda:openbill(mobile, enpass.get()))
        cartbtn.place(x=150,y=130,width=100)
btn1 = Button(w1,text="Proceed to Bill",background='white', bd=10,relief=GROOVE,fg='black',command=lambda:opencart(bookInfo1.get()))
btn1.config(font=("Times New Roman",20) )
btn1.place(x=700, y=700)

btn2 = Button(w1,text="Add new customer",background='white', fg='black',bd=10,relief=GROOVE,command=bookin)
btn2.config(font=("Times New Roman",20) )
btn2.place(x=975, y=700)

w1.mainloop()
