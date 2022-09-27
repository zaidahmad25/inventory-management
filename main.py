from tkinter import *
from tkinter import ttk, filedialog, messagebox
from ctypes import windll
from unicodedata import name
from PIL import Image, ImageTk
import mysql.connector

window = Tk()
window.geometry('1350x800')
window.configure(bg = "#ffffff")

window.title('your title here')

notebook = ttk.Notebook(window)

home = Frame(notebook, bg='#fff') 
addProd = Frame(notebook) 
changeInfo = Frame(notebook) 
removeItem = Frame(notebook) 

notebook.add(home,text="Home")
notebook.add(addProd,text="Add Product")
notebook.add(changeInfo,text="Change Info")
notebook.add(removeItem,text="Remove Item")

notebook.pack(expand=True,fill="both")  

mydb = mysql.connector.connect(
    host = "localhost",
    user = "your-username",
    password = "your-password"
)
cursor = mydb.cursor()


hasRun = False

def makeDatabase():
    global hasRun
    
    if hasRun:
        return
    else:
        hasRun = True

        cursor.execute('create database inventory')
        cursor.execute('use inventory')
        cursor.execute('''create table product(name varchar(100),
                                               image varchar(350),
                                               price int(10),
                                               stock int(250), 
                                               hsn varchar(50),
                                               prodId varchar(150) primary key)''')

hasRun = True
makeDatabase()

windll.shcore.SetProcessDpiAwareness(1)

newFilePath = ''
imagePath = []
def openFile():
    global newFilePath
    newFilePath = filedialog.askopenfilename(title="Choose Image", filetypes= (("JPG Images","*.jpg"), ("PNG Images","*.png")))

def checkIfExists(prodId):
    cursor.execute('use inventory')
    cursor.execute('select prodId from product')
    l = []

    for i in cursor:
        for j in i:
            l.append(j)
    
    if str(prodId) in l:
        changeInfoDisplay(prodId)
    else:
        messagebox.showerror(title='Invalid Input!', message='No product with the given product ID exists.')

def addProduct():
    if newFilePath=='':
        messagebox.showerror(title='No image selected!', message='Please select an image')
    else:
        cursor.execute('use inventory')
        cursor.execute('insert into product values(%s, %s, %s, %s, %s, %s)', (addProdentry0.get(), newFilePath, addProdentry1.get(), addProdentry2.get(), addProdentry4.get(), addProdentry3.get()))
        mydb.commit()
        messagebox.showinfo(title='Product Added to Database', message='Product successfully added to the inventory.')

def showProducts():
    global imagePath
    cursor.execute('use inventory')
    cursor.execute('select * from product')
    index = 0
    imageFileCounter = 0
    for i in cursor:
        index += 1
        if len(i) != 0:
            image = Image.open(i[1])
            resize_image = image.resize((150, 150))
            title = i[0]
            price = i[2]
            itemNo = i[5]
            qty = i[3]  
            hsn = i[4]

            Label(home, text=str(index)+'.', font=('Arial', 16), bg='#fff').grid(column=1, row=index+1, padx=20) #serial number
            render = ImageTk.PhotoImage(resize_image) #image
            imagePath.append(render)
            Label(home, image=imagePath[imageFileCounter], bg='#fff', relief='ridge', bd=3).grid(column=2, row=index+1) #image
            Label(home, text=title, padx=40, pady=10, font=('Roboto', 17), bg='#fff').grid(column=3, row=index+1, padx=5) #name
            Label(home, text='₹'+str(price), padx=40, pady=10, font=('Roboto', 17), bg='#fff').grid(column=4, row=index+1, padx=5) #price
            Label(home, text=itemNo, padx=40, pady=10, font=('Roboto', 17), bg='#fff').grid(column=5, row=index+1, padx=5) #product id a.k.a. itemNo
            Label(home, text=qty, padx=40, pady=10, font=('Roboto', 17), bg='#fff').grid(column=6, row=index+1, padx=5) #stock a.k.a qty
            Label(home, text=hsn, padx=40, pady=10, font=('Roboto', 17), bg='#fff').grid(column=7, row=index+1, padx=5) #hsn

            imageFileCounter += 1

        else:
            Label(home, text="No Items in Inventory", padx=40, pady=10, font=('Roboto', 17), bg='#fff').grid(column=1, row=1, padx=5) 
    
def updateInfo(name, price, stock, hsn, prodId):
    cursor.execute('use inventory')
    query = 'update product set name=%s, price=%s, stock=%s, hsn=%s where prodId=%s'
    try:
        cursor.execute(query, (name,  price, stock, hsn, prodId))
        mydb.commit()
        messagebox.showinfo(title='Sucess', message='Product detail(s) changed successfully')
    except:
        mydb.rollback()

def removeProduct(toberemoved):
    # delete from product where prodId = 4567;
    cursor.execute('use inventory')
    answer =  messagebox.askquestion(title='Remove Product From Database',message='Are you sure you want to delete the product?')
    
    if answer == 'yes':
        cursor.execute('delete from product where prodId = %s',  (toberemoved,))
        mydb.commit()
        messagebox.showinfo(title='Sucess', message='Product deleted successfully')

changeWindowentry0_img = PhotoImage(file = f"tbfor3.png")
changeWindowbackground_img = PhotoImage(file = f"bg3.png")
changeWindowentry1_img = PhotoImage(file = f"tbfor3(1).png")
changeWindowentry2_img = PhotoImage(file = f"tbfor3(2).png")
changeWindowimg0 = PhotoImage(file = f"img0for3.png")
changeWindowimg1 = PhotoImage(file = f"img1for3.png")
changeWindowentry3_img = PhotoImage(file = f"tbfor3(3).png")
changeWindowentry4_img = PhotoImage(file = f"tbfor3(4).png")

def changeInfoDisplay(prodId):
    
    cursor.execute('use inventory')
    cursor.execute('select * from product where prodId = %s', (prodId,))
    details = []

    for i in cursor:
        for j in i:
            details.append(j)
    changeWindow = Toplevel()
    changeWindow.geometry('1350x800')
    changeWindow.configure(bg = "#ffffff")

    canvas = Canvas(
    changeWindow,
    bg = "#ffffff",
    height = 800,
    width = 1500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
    canvas.place(x = 0, y = 0)

    changeWindowentry0_bg = canvas.create_image(
        440.5, 225.0,
        image = changeWindowentry0_img)

    changeWindowentry0 = Entry(
        changeWindow,
        bd = 0,
        font=('Arial', 16), 
        bg = "#d6d6d6",
        highlightthickness = 0)

    changeWindowentry0.insert(END, details[0]) #Name

    changeWindowentry0.place(
        x = 277.0, y = 200,
        width = 327.0,
        height = 48)

    changeWindowbackground = canvas.create_image(
        538.0, 292.5,
        image=changeWindowbackground_img)

    changeWindowentry1_bg = canvas.create_image(
        359.5, 329.0,
        image = changeWindowentry1_img)

    changeWindowentry1 = Entry(
        changeWindow,
        bd = 0,
        bg = "#d6d6d6",
        font=('Arial', 16),
        highlightthickness = 0)

    changeWindowentry1.insert(END, str(details[2])) #price

    changeWindowentry1.place(
        x = 277.0, y = 304,
        width = 165.0,
        height = 48)

    changeWindowentry2_bg = canvas.create_image(
        858.5, 324.0,
        image = changeWindowentry2_img)

    changeWindowentry2 = Entry(
        changeWindow,
        bd = 0,
        font=('Arial', 16),
        bg = "#d6d6d6",
        highlightthickness = 0)

    changeWindowentry2.insert(END, str(details[3]))#stock

    changeWindowentry2.place(
        x = 695.0, y = 299,
        width = 327.0,
        height = 48)

    changeWindowb0 = Button(
        changeWindow,
        image = changeWindowimg0,
        borderwidth = 0,
        highlightthickness = 0,
        command = openFile,
        relief = "flat")

    changeWindowb0.place(
        x = 666, y = 183,
        width = 395,
        height = 67)

    changeWindowentry3_bg = canvas.create_image(
        359.5, 433.0,
        image = changeWindowentry3_img)

    changeWindowentry3 = Label(
        changeWindow,
        text= str(prodId),
        bd = 0,
        bg = "#d6d6d6",
        font=('Arial', 16),
        highlightthickness = 0)

    changeWindowentry3.place(
        x = 277.0, y = 408,
        width = 165.0,
        height = 48)

    changeWindowentry4_bg = canvas.create_image(
        858.5, 439.0,
        image = changeWindowentry4_img)

    changeWindowentry4 = Entry(
        changeWindow,
        bd = 0,
        bg = "#d6d6d6",
        font=('Arial', 16),
        highlightthickness = 0)

    changeWindowentry4.insert(END, str(details[5]))#hsn


    changeWindowentry4.place(
        x = 695.0, y = 414,
        width = 327.0,
        height = 48)

    changeWindowb1 = Button(
        changeWindow,
        image = changeWindowimg1,
        borderwidth = 0,
        highlightthickness = 0,
        command = lambda:updateInfo(changeWindowentry0.get(), changeWindowentry1.get(), changeWindowentry2.get(), changeWindowentry4.get(), prodId),
        relief = "flat")

    changeWindowb1.place(
        x = 462, y = 522,
        width = 379,
        height = 122)

# HOME PAGE
Button(home, text='Refresh Page', command=showProducts, width=15, font=('Roboto', 14), bg='#333', fg='#fff').grid(column=0, row=0, columnspan=5)

# ADD PRODUCT PAGE
canvas = Canvas(
    addProd,
    bg = "#ffffff",
    height = 800,
    width = 1500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

addProdentry0_img = PhotoImage(file = f"tb0.png")
entry0_bg = canvas.create_image(
    440.5, 225.0,
    image = addProdentry0_img)

addProdentry0 = Entry(
    addProd,
    bd = 0,
    bg = "#d6d6d6",
    font=('Arial', 16),
    highlightthickness = 0)

addProdentry0.place(
    x = 277.0, y = 200,
    width = 327.0,
    height = 48)

addProdbackground_img = PhotoImage(file = f"background.png")
addProdbackground = canvas.create_image(
    538.0, 292.5,
    image=addProdbackground_img)

addProdentry1_img = PhotoImage(file = f"tb1.png")
addProdentry1_bg = canvas.create_image(
    359.5, 329.0,
    image = addProdentry1_img)

addProdentry1 = Entry(
    addProd,
    bd = 0,
    bg = "#d6d6d6",
    font=('Arial', 16),
    highlightthickness = 0)

addProdentry1.place(
    x = 277.0, y = 304,
    width = 165.0,
    height = 48)

addProdentry2_img = PhotoImage(file = f"tb2.png")
entry2_bg = canvas.create_image(
    858.5, 324.0,
    image = addProdentry2_img)

addProdentry2 = Entry(
    addProd,
    bd = 0,
    font=('Arial', 16),
    bg = "#d6d6d6",
    highlightthickness = 0)

addProdentry2.place(
    x = 695.0, y = 299,
    width = 327.0,
    height = 48)

addProdentry3_img = PhotoImage(file = f"tb3.png")
entry3_bg = canvas.create_image(
    359.5, 433.0,
    image = addProdentry3_img)

addProdentry3 = Entry(
    addProd,
    bd = 0,
    font=('Arial', 16),
    bg = "#d6d6d6",
    highlightthickness = 0)

addProdentry3.place(
    x = 277.0, y = 408,
    width = 165.0,
    height = 48)

addProdentry4_img = PhotoImage(file = f"tb4.png")
addProdentry4_bg = canvas.create_image(
    858.5, 439.0,
    image = addProdentry4_img)

addProdentry4 = Entry(
    addProd,
    bd = 0,
    font=('Arial', 16),
    bg = "#d6d6d6",
    highlightthickness = 0)

addProdentry4.place(
    x = 695.0, y = 414,
    width = 327.0,
    height = 48)

addProdimg0 = PhotoImage(file = f"img0.png")
addProdb0 = Button(
    addProd,
    image = addProdimg0,
    borderwidth = 0,
    highlightthickness = 0,
    command = addProduct,
    relief = "flat")

addProdb0.place(
    x = 471, y = 532,
    width = 358,
    height = 103)

addProdimg1 = PhotoImage(file = f"img1.png")
addProdb1 = Button(
    addProd,
    image = addProdimg1,
    borderwidth = 0,
    highlightthickness = 0,
    command = openFile,
    relief = "flat")

addProdb1.place(
    x = 661, y = 183,
    width = 395,
    height = 67)

# CHANGE PRODUCT INFO
canvas2 = Canvas(
    changeInfo,
    bg = "#ffffff",
    height = 800,
    width = 1500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas2.place(x = 0, y = 0)

changeProdInfobackground_img = PhotoImage(file = f"background2.png")
background = canvas2.create_image(
    457.5, 263.0,
    image=changeProdInfobackground_img)

changeProdInfoentry0_img = PhotoImage(file = f"tb5.png")
changeProdInfoentry0_bg = canvas2.create_image(
    950.5, 263.0,
    image = changeProdInfoentry0_img)

changeProdInfoentry0 = Entry(
    changeInfo,
    font=('Arial', 16),
    bd = 0,
    bg = "#d6d6d6",
    highlightthickness = 0)

changeProdInfoentry0.place(
    x = 787.0, y = 238,
    width = 327.0,
    height = 48)

changeProdInfoimg0 = PhotoImage(file = f"img2.png")
changeProdInfob0 = Button(
    changeInfo,
    image = changeProdInfoimg0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:checkIfExists(changeProdInfoentry0.get()),
    relief = "flat")

changeProdInfob0.place(
    x = 461, y = 388,
    width = 382,
    height = 110)

# REMOVE ITEM PAGE
canvas3 = Canvas(
    removeItem,
    bg = "#ffffff",
    height = 800,
    width = 1500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas3.place(x = 0, y = 0)

removeItembackground_img = PhotoImage(file = f"background3.png")
background = canvas3.create_image(
    495.0, 263.0,
    image=removeItembackground_img)

removeItementry0_img = PhotoImage(file = f"tb6.png")
removeItementry0_bg = canvas3.create_image(
    909.5, 263.0,
    image = removeItementry0_img)

removeItementry0 = Entry(
    removeItem,
    bd = 0,
    font=('Arial', 16),
    bg = "#d6d6d6",
    highlightthickness = 0)

removeItementry0.place(
    x = 746.0, y = 238,
    width = 327.0,
    height = 48)

removeItemimg0 = PhotoImage(file = f"img3.png")
removeItemb0 = Button(
    removeItem,
    image = removeItemimg0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:removeProduct(removeItementry0.get()),
    relief = "flat")

removeItemb0.place(
    x = 472, y = 386,
    width = 370,
    height = 106)

    
window.mainloop()