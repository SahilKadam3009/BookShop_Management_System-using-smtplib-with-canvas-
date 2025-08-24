import tkinter as tk
import smtplib
from email.message import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4
import os 
import random 
import traceback
import re
import datetime
from datetime import datetime
from tkinter import Tk, ttk
from tkinter import *
import mysql.connector
import time
from tkinter import messagebox,simpledialog
from PIL import Image, ImageTk
try:
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="my-Bookshop"
    )
    mycursor=mydb.cursor() # add your own database
except mysql.connector.Error as err:
    messagebox.showerror("Database Error",f"Error:{err}")

sp_admin_pass="SK_bookshop@123" # adjust with your database

SENDER_EMAIL = "your_email" #add you/sender email address  
SENDER_PASSWORD = "you_API" #add you gmail api 

verification_code = None
is_verified = False

w = tk.Tk()
w.title("BookShop Management")
w.geometry("500x500")
window_width = 1400
window_height = 800
w.geometry(f"{window_width}x{window_height}")


#image_path = "E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_Images\\kimberly-farmer-lUaaKCUANVI-unsplash.jpg"
#image_path="E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_logo4.PNG"

#image_path="F:\\SEMISTER IV\\Python\\python gui\\project2\\bg_logos\\bg_logo3.PNG"
image_path="E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_logos\\bg_logo3.PNG"
#image_path="E:\\SEMISTER IV\\Python\\python gui\\project2\\logo_bg.PNG"
image = Image.open(image_path)
image = image.resize((window_width, window_height)) 
bg_image = ImageTk.PhotoImage(image)

bg_label = tk.Label(w, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)



role = StringVar(value="User") 

def getting_text(event):
    username = entry_username.get()
    password = entry_password.get()
    selected_role = role.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password!")
        return
    
    try:
        if selected_role == "Admin":
            query = "SELECT * FROM admin WHERE username=%s AND password=%s"
        else:
            query = "SELECT * FROM user_data WHERE username=%s AND password=%s"

        mycursor.execute(query, (username, password))
        user = mycursor.fetchone()
        
        if user:
            messagebox.showinfo("Login Successful", f"Welcome to SK BookShop, {username}!")
            if selected_role=="Admin":
                new_gui()
                #admin_management()
            else:
                #user_management()
                user_interface()
            print("***********************************************************************************")
            print("*****************************LOGIN SUCCESSFULLY!!**********************************")
            print("***********************************************************************************")

            print("        *****   ***    ***    *      *  *****   *     *   ***   ******             ")
            print("        *    * *   *  *   *   *    *    *       *     *  *   *  *     *            ")
            print("        *    * *   *  *   *   *  *      *       *     *  *   *  *     *            ")
            print("        *****  *   *  *   *   **        *****   *******  *   *  ******             ")
            print("        *    * *   *  *   *   *  *          *   *     *  *   *  *                  ")
            print("        *    * *   *  *   *   *    *        *   *     *  *   *  *                  ")
            print("        *****   ***    ***    *      *  *****   *     *   ***   *                  ")

            print("***********************************************************************************")
            print("*****************************LOGIN SUCCESSFULLY!!**********************************")
            print("***********************************************************************************")                    
        else:
            if selected_role=="Admin":
                messagebox.showerror("Error", "Admin does not exist. Please Register!")
            else:
                messagebox.showerror("Error", "User does not exist. Please Register!")
                    
  
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def admin_key():
    selected_role=role.get()

    if selected_role=="Admin":
        admin_key=simpledialog.askstring("Admin Key","Enter The Admin Key:",show='$')
        if admin_key:
            messagebox.showinfo("Info",f"successfully Register")
        else:
            messagebox.showerror("Error","Invalid Admin Key!")  



def register(*args):
    username=entry_username.get()
    password=entry_password.get()
    selected_role=role.get()

    if not (username and password):
        messagebox.showerror("Error","Please enter username and password!")
        return
    if selected_role=="Admin":
        sp_password=entry_sp.get()
        if sp_password != sp_admin_pass:
            messagebox.showerror("Error","Invalid Admin Key!! Registration denied.")
            return    
    try:
        if selected_role=="Admin":
            insert="INSERT INTO admin (username, password) VALUES (%s,%s)"
        else:
            insert="INSERT INTO user_data (username, password) VALUES (%s,%s)"
        mycursor.execute(insert, (username,password) )
        mydb.commit()    
        messagebox.showinfo("Registration Successful",f"{selected_role} register successfully")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")





def new_gui():
    w.withdraw()
    gui_win = tk.Toplevel()
    gui_win.title("New window")
    gui_win.geometry("900x700")

    top_banner = tk.Label(gui_win, text="Grab Bestselling Books upto 50% Off!",
                          bg="#e53935", fg="white", font=("Helvetica", 12))
    top_banner.pack(fill=tk.X)

    header_frame = tk.Frame(gui_win, bg="white", pady=10)
    header_frame.pack(fill=tk.X)

    logo = tk.Label(header_frame, text="SK\nBOOKS", fg="red", font=("Arial", 16, "bold"))
    logo.pack(side=tk.LEFT, padx=20)

    search_frame = tk.Frame(header_frame, bg="white", bd=2, relief=tk.SOLID)
    search_frame.pack(side=tk.LEFT, padx=10)

    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=60, bd=0)
    search_entry.insert(0, "Search By Title, Author, Publisher Or ISBN")
    search_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def on_entry_click(event):
        if search_entry.get() == "Search By id, Title, Author, Or ISBN":
            search_entry.delete(0, tk.END)

    search_entry.bind("<FocusIn>", on_entry_click)

    def search_action():
        query = search_entry.get()
        if not query or query.strip() == "" or query == "Search By Title, Author, Publisher Or ISBN":
            messagebox.showwarning("Input Error", "Please enter a valid search query.")
            return

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="my-bookshop"
            )
            mycursor = mydb.cursor(buffered=True)

            query_like = f"%{query}%"
            sql = "SELECT id, title, author, price, qty FROM book_inventory WHERE id=%s OR title LIKE %s OR author LIKE %s OR isbn LIKE %s"
            mycursor.execute(sql, (query, query_like, query_like, query_like))
            result = mycursor.fetchone()

            if result:
                book_id, title, author, price, qty = result
                msg = (
                    f"📚 Book Found:\n\n"
                    f"🆔 ID: {book_id}\n"
                    f"📖 Title: {title}\n"
                    f"✍️ Author: {author}\n"
                    f"💰 Price: ₹{price:.2f}\n"
                    f"📦 Stock: {qty} available"
                )
                messagebox.showinfo("Search Result", msg)
            else:
                messagebox.showinfo("Not Found", "Sorry, no matching book found.")

            mycursor.close()
            mydb.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


    search_icon = tk.Button(search_frame, text="🔍", bg="red", fg="white", command=search_action)
    search_icon.pack(side=tk.LEFT, padx=5, pady=5)

    nav_frame = tk.Frame(gui_win, bg="white")
    nav_frame.pack(fill=tk.X, pady=5)

    nav_buttons = [
        ("ADD_BOOKS", add_book),
        ("Update_Book", update_book),
        ("Delete Book", delete_book),
        ("View book", view_book),
        ("Request a Book", send_verification_email),
        ("Exit", exit_Store)
        ]

    for btn_text, btn_command in nav_buttons:
        btn = tk.Button(
            nav_frame,
            text=btn_text,
            bd=0,
            fg="red",
            font=("Arial", 10),
            command=btn_command if btn_command else lambda: None
        )
        btn.pack(side=tk.LEFT, padx=10)

    trending_banner = tk.Label(gui_win,
                               text="TRENDING, THRILLING AND TOTALLY UNSTOPPABLE READS",
                               font=("Arial", 16, "bold"),
                               bg="#fceabb", fg="black", pady=10)
    trending_banner.pack(fill=tk.X, pady=5)

    manga_frame = tk.Frame(gui_win, bg="#424242", padx=20, pady=20)
    manga_frame.pack(fill=tk.X)

    manga_title = tk.Label(manga_frame, text="MANGA & COMICS", font=("Arial", 20, "bold"), fg="white", bg="#424242")
    manga_title.pack(anchor='w')

    #book_frame = tk.Frame(manga_frame, bg="#424242")
    #book_frame.pack(pady=10)

    # Scrollable Canvas for Books
    scroll_canvas = tk.Canvas(manga_frame, bg="#424242", height=200, highlightthickness=0)
    scroll_canvas.pack(fill=tk.X, side=tk.TOP, expand=True)

    h_scrollbar = tk.Scrollbar(manga_frame, orient=tk.HORIZONTAL, command=scroll_canvas.xview)
    h_scrollbar.pack(fill=tk.X, side=tk.TOP)

    scroll_canvas.configure(xscrollcommand=h_scrollbar.set)

    book_frame = tk.Frame(scroll_canvas, bg="#424242")
    scroll_canvas.create_window((0, 0), window=book_frame, anchor='nw')

    def update_scrollregion(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    book_frame.bind("<Configure>", update_scrollregion)


    book_images = [
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b2.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b3.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b4.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b6.jpeg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b5.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b5.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b8.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b9.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b10.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b11.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b12.jpg"
    ]

    book_labels = []
    for img_file in book_images:
        try:
            img = Image.open(img_file).resize((120, 180))
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(book_frame, image=photo, bg="#424242")
            lbl.image = photo  # Reference to avoid garbage collection
            lbl.pack(side=tk.LEFT, padx=15)
            book_labels.append(lbl)
        except Exception as e:
            print(f"Error loading {img_file}: {e}")



def user_interface():
    w.withdraw()
    user_win = tk.Toplevel()
    user_win.title("New window")
    user_win.geometry("900x700")

    top_banner = tk.Label(user_win, text="Grab Bestselling Books upto 50% Off!",
                          bg="#e53935", fg="white", font=("Helvetica", 12))
    top_banner.pack(fill=tk.X)

    header_frame = tk.Frame(user_win, bg="white", pady=10)
    header_frame.pack(fill=tk.X)

    logo = tk.Label(header_frame, text="SK\nBOOKS", fg="red", font=("Arial", 16, "bold"))
    logo.pack(side=tk.LEFT, padx=20)

    search_frame = tk.Frame(header_frame, bg="white", bd=2, relief=tk.SOLID)
    search_frame.pack(side=tk.LEFT, padx=10)

    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=60, bd=0)
    search_entry.insert(0, "Search By Title, Author, Publisher Or ISBN")
    search_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def on_entry_click(event):
        if search_entry.get() == "Search By Title, Author, Publisher Or ISBN":
            search_entry.delete(0, tk.END)

    search_entry.bind("<FocusIn>", on_entry_click)

    def search_action():
        query = search_entry.get()
        if not query or query.strip() == "" or query == "Search By Title, Author, Publisher Or ISBN":
            messagebox.showwarning("Input Error", "Please enter a valid search query.")
            return

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="my-bookshop"
            )
            mycursor = mydb.cursor(buffered=True)

            query_like = f"%{query}%"
            query_id = int(query) if query.isdigit() else 0
            sql = "SELECT id, title, author, price, qty FROM book_inventory WHERE id=%s OR title LIKE %s OR author LIKE %s OR isbn LIKE %s"
            mycursor.execute(sql, (query_id, query_like, query_like, query_like))
            result = mycursor.fetchone()

            if result:
                book_id, title, author, price, qty = result
                msg = (
                    f"📚 Book Found:\n\n"
                    f"🆔 ID: {book_id}\n"
                    f"📖 Title: {title}\n"
                    f"✍️ Author: {author}\n"
                    f"💰 Price: ₹{price:.2f}\n"
                    f"📦 Stock: {qty} available"
                )
                messagebox.showinfo("Search Result", msg)
            else:
                messagebox.showinfo("Not Found", "Sorry, no matching book found.")

            mycursor.close()
            mydb.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    search_icon = tk.Button(search_frame, text="🔍", bg="red", fg="white", command=search_action)
    search_icon.pack(side=tk.LEFT, padx=5, pady=5)

    nav_frame = tk.Frame(user_win, bg="white")
    nav_frame.pack(fill=tk.X, pady=5)

    nav_buttons = [
        ("ADD_BOOKS",None),
        ("Update_Book",None),
        ("view Book ", view_book),
        ("Buy Book", buy_book_gui),
        ("Request a Book", send_verification_email),
        ("Exit Store", exit_Store)
    ]

    for btn_text, btn_command in nav_buttons:
        btn = tk.Button(
            nav_frame,
            text=btn_text,
            bd=0,
            fg="red",
            font=("Arial", 10),
            command=btn_command if btn_command else lambda: messagebox.showwarning("warning","only admin can access this button")
        )
        btn.pack(side=tk.LEFT, padx=10)

    trending_banner = tk.Label(user_win,
                               text="TRENDING, THRILLING AND TOTALLY UNSTOPPABLE READS",
                               font=("Arial", 16, "bold"),
                               bg="#fceabb", fg="black", pady=10)
    trending_banner.pack(fill=tk.X, pady=5)

    manga_frame = tk.Frame(user_win, bg="#424242", padx=20, pady=20)
    manga_frame.pack(fill=tk.X)

    manga_title = tk.Label(manga_frame, text="MANGA & COMICS", font=("Arial", 20, "bold"), fg="white", bg="#424242")
    manga_title.pack(anchor='w')

    #book_frame = tk.Frame(manga_frame, bg="#424242")
    #book_frame.pack(pady=10)

    scroll_canvas = tk.Canvas(manga_frame, bg="#424242", height=200, highlightthickness=0)
    scroll_canvas.pack(fill=tk.X, side=tk.TOP, expand=True)

    h_scrollbar = tk.Scrollbar(manga_frame, orient=tk.HORIZONTAL, command=scroll_canvas.xview)
    h_scrollbar.pack(fill=tk.X, side=tk.TOP)

    scroll_canvas.configure(xscrollcommand=h_scrollbar.set)

    book_frame = tk.Frame(scroll_canvas, bg="#424242")
    scroll_canvas.create_window((0, 0), window=book_frame, anchor='nw')

    def update_scrollregion(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    book_frame.bind("<Configure>", update_scrollregion)


    book_images = [
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b2.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b3.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b4.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b6.jpeg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b5.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b5.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b8.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b9.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b10.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b11.jpg",
        "E:\\SEMISTER IV\\Python\\python gui\\project2\\e-books\\b12.jpg"
    ]

    book_labels = []
    for img_file in book_images:
        try:
            img = Image.open(img_file).resize((120, 180))
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(book_frame, image=photo, bg="#424242")
            lbl.image = photo  # Reference to avoid garbage collection
            lbl.pack(side=tk.LEFT, padx=15)
            book_labels.append(lbl)
        except Exception as e:
            print(f"Error loading {img_file}: {e}")




def admin_management():
    w.withdraw()
    man_win = tk.Toplevel()
    man_win.title("Admin Panel - Bookshop Management")
    man_win.geometry("500x500")

    #image_path="F:\\SEMISTER IV\\Python\\python gui\\project2\\bg_Images\\janko-ferlic-sfL_QOnmy00-unsplash.jpg"
    image_path = "E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_Images\\janko-ferlic-sfL_QOnmy00-unsplash.jpg"
    image1 = Image.open(image_path).resize((1000, 650))
    tk_image1 = ImageTk.PhotoImage(image1)
    man_win.image_ref = tk_image1
    canvas = tk.Canvas(man_win, width=950, height=600, bd=5, relief="solid", highlightbackground="blue", highlightthickness=3)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    canvas.create_image(500, 325, anchor=tk.CENTER, image=tk_image1)

    add_btn = tk.Button(man_win, text="ADD BOOK", bg="blue", bd=5, relief="solid", font=("Arial", 14, "bold"), command=add_book)
    update_btn = tk.Button(man_win, text="UPDATE BOOK", bg="blue", bd=5, relief="solid", font=("Arial", 14, "bold"), command=update_book)
    delete_btn = tk.Button(man_win, text="DELETE BOOK", bg="blue", bd=5, relief="solid", font=("Arial", 14, "bold"), command=delete_book)
    search_btn = tk.Button(man_win, text="SEARCH BOOK", bg="blue", bd=5, relief="solid", font=("Arial", 14, "bold"), command=search_book)
    view_btn = tk.Button(man_win, text="VIEW BOOK", bg="blue", bd=5, relief="solid", font=("Arial", 14, "bold"), command=view_book)
    exit_btn = tk.Button(man_win, text="EXIT", bg="Red", bd=5, relief="solid", font=("Arial", 16, "bold"), command=exit_Store)

    canvas.create_window(180, 180, window=add_btn, width=200, height=40)
    canvas.create_window(180, 260, window=update_btn, width=200, height=40)
    canvas.create_window(180, 340, window=delete_btn, width=200, height=40)
    canvas.create_window(180, 420, window=search_btn, width=200, height=40)
    canvas.create_window(180, 500, window=view_btn, width=200, height=40)
    canvas.create_window(850, 550, window=exit_btn, width=200, height=50)

def user_management():
    w.withdraw()
    user_win = tk.Toplevel()
    user_win.title("User Panel - Bookshop Management")
    user_win.geometry("500x500")

    tk.Label(user_win, text="Welcome, User!", font=("Arial", 16, "bold")).pack(pady=10)

    view_btn = tk.Button(user_win, text="VIEW BOOKS", bg="blue", bd=5, relief="solid", font=("Arial", 14, "bold"), command=view_book)
    search_btn = tk.Button(user_win, text="SEARCH BOOKS", bg="blue", bd=5, relief="solid", font=("Arial", 14, "bold"), command=search_book)
    exit_btn = tk.Button(user_win, text="EXIT", bg="Red", bd=5, relief="solid", font=("Arial", 14, "bold"), command=exit_Store)

    view_btn.pack(pady=10)
    search_btn.pack(pady=10)
    exit_btn.pack(pady=10)

'''def login_error():
    w.withdraw()
    error_win = Toplevel()
    error_win.title("Login Unsuccessful")
    error_win.geometry("200x200")
    Label(error_win, text="Login Unsuccessful", font=("Arial", 14, "italic"), bg="Red").grid(row=0, column=0, pady=10)
    bt2 = Button(error_win, text="Retry", bg="Green", command=Retry_pass)
    bt2.grid(row=1, column=0, pady=10)

def Retry_pass():
    w.deiconify()'''

'''def toggle_pass():
    if txt1.get("show")=='*':
        txt1.config(show="")
        toggle_btn.config(image=hide_img)
    else:
        txt1.config(show="*")
        toggle_btn.config(image=show_img)'''        
def time():
    now=datetime.now()
    current_time=now.strftime("%Y-%m-%d \n %H:%M:%S")
    time_label.config(text=current_time)
    w.after(1000,time)

time_label = tk.Label(w, font=("Arial", 12,"bold"), fg="white", bg="black",highlightthickness=2,highlightbackground="yellow")
time_label.place(x=1, y=1)
time()    


def add_book():

    print("Add book clicked")
    add_win = Toplevel()
    add_win.title("ADD BOOKS")
    add_win.geometry("500x500")
    window_width=1400
    window_height=800

    #image_path="F:\\SEMISTER IV\\Python\\python gui\\project2\\bg_Images\\kimberly-farmer-lUaaKCUANVI-unsplash.jpg"
    image_path="E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_Images\\kimberly-farmer-lUaaKCUANVI-unsplash.jpg"
    image=Image.open(image_path)
    image=image.resize((window_width,window_height))
    bg_image=ImageTk.PhotoImage(image)
    add_win.bg_image=bg_image
    bg_label=tk.Label(add_win,image=add_win.bg_image)
    bg_label.place(x=0,y=0,relwidth=1,relheight=1)

    '''image_path_add="E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_Images\\nareeta-martin-pEWtWnDgGLs-unsplash.jpg"
    image_add=Image.open(image_path_add).resize((50,50))
    #add_win.image=image
    add_win.tk_image_add=ImageTk.PhotoImage(image_add)'''

    canvas = tk.Canvas(add_win, width=480, height=500, highlightbackground="blue", highlightthickness=3)
    canvas.place(relx=0.7, rely=0.5, anchor=CENTER)
    canvas.create_image(400, 500, anchor=tk.CENTER)

    add_book_label=Label(add_win,text="📚 ADD_BOOK 📚",font=("Arial",18,"bold"),fg="#2980B9")
    canvas.create_window(250,50,window=add_book_label)

    lb3=Label(add_win,text="   Title📖:",bg="#ECF0F1",font=("Arial",12,"bold"))
    canvas.create_window(150,100,window=lb3)

    book_title=tk.Entry(add_win,bg="#ECF0F1",highlightbackground="cyan",highlightthickness=3, font=("Arial",12,"bold"),bd=2)
    canvas.create_window(350,100,window=book_title)

    lb4=Label(add_win,text="  Author✍️:",bg="#ECF0F1",font=("Arial",12,"bold"))
    canvas.create_window(150,150,window=lb4)

    book_author=tk.Entry(add_win,bg="#ECF0F1",highlightbackground="cyan",highlightthickness="3",font=("Arial",12,"bold"),bd=2)
    canvas.create_window(350,150,window=book_author)

    isbn_label=Label(add_win,text="    ISBN🔖:",bg="#ECF0F1",font=("Arial",12,"bold"))
    canvas.create_window(150,200,window=isbn_label)

    book_isbn=tk.Entry(add_win,bg="#ECF0F1",highlightbackground="cyan",highlightthickness=3,font=("Arial",12,"bold"),bd=2)
    canvas.create_window(350,200,window=book_isbn)

    qty_label=Label(add_win,text="Quantity📦:",bg="#ECF0F1",font=("Arial",12,"bold"))
    canvas.create_window(150,250,window=qty_label)

    book_qty=tk.Entry(add_win,bg="#ECF0F1",highlightbackground="cyan",highlightthickness=3,font=("Arial",12,"bold"),bd=2)
    canvas.create_window(350,250,window=book_qty)

    price_label=Label(add_win,text="   Price💰:",bg="#ECF0F1",font=("Arial",12,"bold"))
    canvas.create_window(150,300,window=price_label)

    book_price=tk.Entry(add_win,bg="#ECF0F1",highlightbackground="cyan",highlightthickness=3,font=("Arial",12,"bold"),bd=2)
    canvas.create_window(350,300,window=book_price)

    '''lb = Label(w, text="Username:", bg="lightgray", font=("Arial", 12, "bold"))
    canvas.create_window(150, 100, window=lb)

    entry_password = Entry(w, bg="#ECF0F1", show="*", highlightbackground="cyan", highlightthickness=3,font=("Arial",12),bd=2)
    canvas.create_window(150, 250, window=entry_password)'''


    '''Label(add_win, text="Title:").pack()
    book_title = Entry(add_win)
    book_title.pack()

    Label(add_win, text="Author:").pack()
    book_author = Entry(add_win)
    book_author.pack()

    Label(add_win, text="ISBN:").pack()
    book_isbn = Entry(add_win)
    book_isbn.pack()

    Label(add_win, text="Quantity:").pack()
    book_qty = Entry(add_win)
    book_qty.pack()

    Label(add_win, text="Price:").pack()
    book_price = Entry(add_win)
    book_price.pack()'''

    if book_title=="" or book_author=="" or book_isbn=="" or book_qty=="" or book_price=="":
        messagebox.showerror("Error","Please fill all fields before inserting.")
        return

    def insertBook():
        title=book_title.get()
        author=book_author.get()
        isbn=book_isbn.get()
        qty=book_qty.get()
        price=book_price.get()

        if title=="" or author=="" or isbn=="" or qty=="" or price=="":
            messagebox.showerror("Error","Please fill all fields before inserting.")
            return

        try:
            insert_query="INSERT INTO book_inventory(title,author,isbn,qty,price) VALUES(%s,%s,%s,%s,%s)"
            values=(title,author,isbn,qty,price)
            mycursor.execute(insert_query,values)
            mydb.commit()
            messagebox.showinfo("Success","Record Inserted successfully!")
            add_win.destroy()    
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error",f"Error:{err}")    


    #Button(add_win, text="Save",command=insertBook).pack(pady=10)
    save_btn=Button(add_win,text="ADD BOOK",bg="Green",bd=5,font=("Arial",12,"bold"),fg="cyan",width=18,height=1,command=insertBook)
    #save_btn.bind("<Button-1>",insertBook)
    canvas.create_window(350,400,window=save_btn)

    clear_btn= Button(add_win, text="Clear Data", bg="Red", bd=5, font=("Arial",12,"bold"), width=18, height=1,command=lambda: [book_title.delete(0, END), book_author.delete(0, END),book_isbn.delete(0,END),book_qty.delete(0,END),book_price.delete(0,END)])
    canvas.create_window(150, 400, window=clear_btn)

def view_book():
    print("View book clicked")
    view_win = tk.Toplevel()
    view_win.title("VIEW BOOKS")
    view_win.geometry("500x500")

    tree=ttk.Treeview(view_win,columns=("ID","Title","Author","ISBN","Qty","Price"))
    tree.heading("ID",text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Qty", text="Quantity")
    tree.heading("Price", text="Price")

    tree.column("ID",width=50)
    tree.column("Title", width=150)
    tree.column("Author", width=120)
    tree.column("ISBN", width=100)
    tree.column("Qty", width=80)
    tree.column("Price", width=80)
    tree.pack(expand=True,fill="both")

    scrollbar=ttk.Scrollbar(view_win,orient="vertical",command=ttk.Treeview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right",fill="y")

    try:
        retrive="SELECT * FROM book_inventory"
        mycursor.execute(retrive)
        rows=mycursor.fetchall()
        for row in rows:
            tree.insert("","end",values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error",f"Error:{err}")        
def search_book():
    print("Search book clicked")
    search_win = Toplevel()
    search_win.title("SEARCH BOOKS")
    search_content="Search by Title, Author Or ISBN"

    header_frame=tk.Label(search_win,bg="white",pady=10)
    header_frame.pack(fill=tk.X)
    search_frame=tk.Frame(header_frame,bg="white",bd=2,relief=tk.SOLID)
    search_frame.pack(side=tk.LEFT,padx=10)
    search_entry=tk.Entry(search_frame,font=("Arial",12),width=60,bd=0)
    search_entry.insert(0,search_content)
    search_entry.bind("<FocusIn>",lambda e:[search_entry.delete(0,END)])
    search_entry.bind("<FocusOut>",lambda e:[search_entry.insert(0,search_content)])
    search_entry.pack(side=LEFT,padx=5,pady=5)
    
    def search_action():
        query=search_entry.get()
        if query=="":
            messagebox.showerror("Error","Insert Content In SearchBox")    
        else:
            try:
                #mycursor.mydb.cursor()
                mycursor.execute("SELECT id,title,author,isbn,qty,price FROM book_inventory WHERE id=%s,title=%s,author=%s",(query,))
                result=mycursor.fetchone()
                mycursor.close()
                if result:
                    id,title,author,isbn,qty,price=result
                    msg=(
                        f"Book Detais:\n\n"
                        f"ID:{id}\n"
                        f"TITLE:{title}\n"
                        f"AUTHOR:{author}\n"
                        f"ISBN:{isbn}\n"
                        f"Stock:₹{qty}\n"
                        f"PRICE:{price} available\n"
                        )
                    messagebox.showinfo("search result",msg)
                else:
                    messagebox.showinfo("Not Found","NO Book Found")
            except Exception as e:
                traceback.print_exc()
                messagebox.showerror("Error","Failed to search book.")
                        

    search_icon=tk.Button(search_frame,text="🔍",bg="red",fg="white",command=search_action)
    search_icon.pack(side=tk.LEFT,padx=5,pady=5)        

def delete_book():
    print("Delete book clicked")
    delete_win = Toplevel()
    delete_win.title("DELETE BOOKS")
    delete_win.geometry("900x600")

 
    search_by_var = tk.StringVar(value="id")
    id_var = tk.StringVar()
    title_var = tk.StringVar()
    author_var = tk.StringVar()
    isbn_var = tk.StringVar()
    price_var = tk.StringVar()
    qty_var = tk.StringVar()

    def fetch_book():
        key = search_by_var.get()
        value = search_entry.get().strip()

        mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="my-Bookshop"
    )
        mycursor = mydb.cursor(dictionary=True)

        try:
            query = f"SELECT * FROM book_inventory WHERE {key} = %s"
            mycursor.execute(query, (value,))
            result = mycursor.fetchone()

            if result:
                id_var.set(result['id'])
                title_var.set(result['title'])
                author_var.set(result['author'])
                isbn_var.set(result['isbn'])
                price_var.set(result['price'])
                qty_var.set(result['qty'])
            else:
                messagebox.showerror("Not Found", f"No book found with {key} = {value}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL error: {err}")
        finally:
            mydb.close()    
    def delete_fun():
        nonlocal id_var, title_var, author_var, isbn_var, price_var, qty_var
        id=id_var.get().strip()
        title=title_var.get().strip()
        author=author_var.get().strip()
        isbn=isbn_var.get().strip()
        key = search_by_var.get()
        value = search_entry.get().strip()

        mycursor = mydb.cursor()
        if not value:
            messagebox.showwarning("Missing Info","Please search and select a book first. ")
            return

        confirm=messagebox.askyesno("Confirm Delete",f"Are you sure you want to delete '{title}' book ")
        if not confirm:
            return    
        try:
            mycursor = mydb.cursor()

            query = f"DELETE FROM book_inventory WHERE {key} = %s"
            mycursor.execute(query,(value,))
            mydb.commit()

            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", f"'{title}'Book deleted successfully!")
                id_var=set("")
                title_var=set("")
                author_var=set("")
                isbn_var=set("")
                price_var=set("")
                qty_var=set("")
                delete_win.destroy()
            else:
                messagebox.showerror("Error", f"failed. Check Book {key} again.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL error: {err}")
        #finally:
            #mydb.close()

    top_banner = tk.Label(delete_win, text="Grab Bestselling Books upto 50% Off!", bg="#d32f2f", fg="white",
                          font=("Arial", 12, "bold"), padx=10, pady=5)
    top_banner.pack(fill="x")

    search_frame = tk.Frame(delete_win, bg="white")
    search_frame.pack(pady=10)

    logo = tk.Label(search_frame, text="BOOKSWAGON", font=("Arial", 18, "bold"), fg="#d32f2f", bg="white")
    logo.grid(row=0, column=0, padx=10)

    search_entry = tk.Entry(search_frame, font=("Arial", 12))
    search_entry.grid(row=0, column=1, ipadx=100, ipady=5, padx=10)

    search_button = tk.Button(search_frame, text="Search", command=fetch_book, bg="#f44336", fg="white",
                              font=("Arial", 10, "bold"))
    search_button.grid(row=0, column=2, padx=5)

    search_by_dropdown = tk.OptionMenu(search_frame, search_by_var, "id", "title", "author", "isbn")
    search_by_dropdown.config(bg="white")
    search_by_dropdown.grid(row=0, column=3)

    nav_frame = tk.Frame(delete_win, bg="#f5f5f5", pady=10)
    nav_frame.pack(fill="x")

    for label ,command in [("Book_list",view_book)]:
        tk.Button(nav_frame, text=label, command=command, bg="#f5f5f5", relief="flat", font=("Arial", 10)).pack(side="left", padx=10)

    form_frame = tk.Frame(delete_win, bg="white", pady=20)
    form_frame.pack()

    labels = ["ID", "Title", "Author", "ISBN", "Price", "Quantity"]
    variables = [id_var, title_var, author_var, isbn_var, price_var, qty_var]

    for i, (label, var) in enumerate(zip(labels, variables)):
        tk.Label(form_frame, text=label, font=("Arial", 12), bg="white").grid(row=i, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(form_frame, textvariable=var, font=("Arial", 12), width=40).grid(row=i, column=1, pady=5, padx=5)

    tk.Button(delete_win, text="Delete Book", command=delete_fun, bg="#388e3c", fg="white",
              font=("Arial", 12, "bold")).pack(pady=10)

def update_book():
    print("Update book clicked")
    update_win = tk.Toplevel()
    update_win.title("Update BOOKS")
    update_win.geometry("900x600")

 
    search_by_var = tk.StringVar(value="id")
    id_var = tk.StringVar()
    title_var = tk.StringVar()
    author_var = tk.StringVar()
    isbn_var = tk.StringVar()
    price_var = tk.StringVar()
    qty_var = tk.StringVar()

    def fetch_book():
        key = search_by_var.get()
        value = search_entry.get().strip()

        mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="my-Bookshop"
    )
        #mydb = update_book()
        mycursor = mydb.cursor(dictionary=True)

        try:
            query = f"SELECT * FROM book_inventory WHERE {key} = %s"
            mycursor.execute(query, (value,))
            result = mycursor.fetchone()

            if result:
                id_var.set(result['id'])
                title_var.set(result['title'])
                author_var.set(result['author'])
                isbn_var.set(result['isbn'])
                price_var.set(result['price'])
                qty_var.set(result['qty'])
            else:
                messagebox.showerror("Not Found", f"No book found with {key} = {value}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL error: {err}")
        #finally:
            #mydb.close()

    def update_inventory():
        #mydb = update_book()
        mycursor = mydb.cursor()

        try:
            query = """UPDATE book_inventory SET title=%s, author=%s, isbn=%s, price=%s, qty=%s WHERE id=%s"""
            mycursor.execute(query, (
                title_var.get(),
                author_var.get(),
                isbn_var.get(),
                price_var.get(),
                qty_var.get(),
                id_var.get()
            ))
            mydb.commit()

            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", "Book updated successfully!")
                update_win.destroy()
            else:
                messagebox.showerror("Error", "Update failed. Check Book ID again.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL error: {err}")
        #finally:
            #mydb.close()

    top_banner = tk.Label(update_win, text="Grab Bestselling Books upto 50% Off!", bg="#d32f2f", fg="white",
                          font=("Arial", 12, "bold"), padx=10, pady=5)
    top_banner.pack(fill="x")

    search_frame = tk.Frame(update_win, bg="white")
    search_frame.pack(pady=10)

    logo = tk.Label(search_frame, text="BOOKSWAGON", font=("Arial", 18, "bold"), fg="#d32f2f", bg="white")
    logo.grid(row=0, column=0, padx=10)

    search_entry = tk.Entry(search_frame, font=("Arial", 12))
    search_entry.grid(row=0, column=1, ipadx=100, ipady=5, padx=10)

    search_button = tk.Button(search_frame, text="Search", command=fetch_book, bg="#f44336", fg="white",
                              font=("Arial", 10, "bold"))
    search_button.grid(row=0, column=2, padx=5)

    search_by_dropdown = tk.OptionMenu(search_frame, search_by_var, "id", "title", "author", "isbn")
    search_by_dropdown.config(bg="white")
    search_by_dropdown.grid(row=0, column=3)

    nav_frame = tk.Frame(update_win, bg="#f5f5f5", pady=10)
    nav_frame.pack(fill="x")

    for label ,command in [("Book_list",view_book)]:
        tk.Button(nav_frame, text=label, command=command, bg="#f5f5f5", relief="flat", font=("Arial", 10)).pack(side="left", padx=10)

    form_frame = tk.Frame(update_win, bg="white", pady=20)
    form_frame.pack()

    labels = ["ID", "Title", "Author", "ISBN", "Price", "Quantity"]
    variables = [id_var, title_var, author_var, isbn_var, price_var, qty_var]

    for i, (label, var) in enumerate(zip(labels, variables)):
        tk.Label(form_frame, text=label, font=("Arial", 12), bg="white").grid(row=i, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(form_frame, textvariable=var, font=("Arial", 12), width=40).grid(row=i, column=1, pady=5, padx=5)

    tk.Button(update_win, text="Update Book", command=update_inventory, bg="#388e3c", fg="white",
              font=("Arial", 12, "bold")).pack(pady=10)


def send_verification_email():
    email_win = Toplevel()
    email_win.title("Request A Book with Email Verification")
    email_win.geometry("600x600")
    email_win.configure(bg="black")

    global is_verified
    is_verified = False
    verification_code = ""

    def verify_code():
        nonlocal verification_code
        user_code = code_entry.get().strip()
        if user_code == verification_code:
            global is_verified
            is_verified = True
            messagebox.showinfo("Verified", "Email verified successfully!")
        else:
            messagebox.showerror("Failed", "Incorrect verification code.")

    def connect_to_db():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="my-Bookshop"
            )
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{e}")
            return None

    def clear_form():
        entry_isbn.delete(0, tk.END)
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        code_entry.delete(0, tk.END)
        global is_verified
        is_verified = False

    def submit_form():
        if not is_verified:
            messagebox.showerror("Verification Required", "Please verify your email before submitting.")
            return

        isbn = entry_isbn.get().strip()
        title = entry_title.get().strip()
        author = entry_author.get().strip()
        quantity = entry_qty.get().strip()
        price = entry_price.get().strip()
        email = entry_email.get().strip()
        phone = entry_phone.get().strip()

        if isbn == "" or title == "" or email == "":
            messagebox.showerror("Missing Fields", "ISBN13, Book Title, and Email are required.")
            return

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        try:
            qty = int(quantity)
            price_val = float(price)
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be an integer and Price must be a number.")
            return

        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO book_requests (isbn, title, author, quantity, price, email, phone)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (isbn, title, author, qty, price_val, email, phone))
                conn.commit()
                messagebox.showinfo("Success", "Book request submitted successfully.")
                clear_form()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error inserting data:\n{err}")

    tk.Label(email_win, text="Request A Book", font=("Helvetica", 16, "bold"), bg="black", fg="white").pack(pady=10)

    frame = tk.Frame(email_win)
    frame.pack(pady=10)

    tk.Label(frame, text="ISBN13:*").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_isbn = tk.Entry(frame, width=40)
    entry_isbn.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Book Title:*").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_title = tk.Entry(frame, width=40)
    entry_title.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Author:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_author = tk.Entry(frame, width=40)
    entry_author.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame, text="Quantity:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_qty = tk.Entry(frame, width=40)
    entry_qty.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame, text="Price:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_price = tk.Entry(frame, width=40)
    entry_price.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(frame, text="Email ID:*").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_email = tk.Entry(frame, width=40)
    entry_email.grid(row=5, column=1, padx=5, pady=5)

    def send_email():
        nonlocal verification_code
        email = entry_email.get().strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        verification_code = str(random.randint(100000, 999999))
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                subject = "Book Request Email Verification"
                body = (
                    f"Dear User,\n\n"
                    f"Thank you for requesting a book from our Bookshop.\n\n"
                    f"Your One-Time Verification Code is: {verification_code}\n\n"
                    f"Please enter this code in the application to verify your email address.\n"
                    f"This code is valid for 5 minutes.\n\n"
                    f"Regards,\n"
                    f"Bookshop Team"
                )

                message = f"From: Bookshop <{SENDER_EMAIL}>\n"
                message += f"To: {email}\n"
                message += f"Subject: {subject}\n\n{body}"
                
                server.sendmail(SENDER_EMAIL, email, message)
            messagebox.showinfo("Sent", f"A verification code has been sent to {email}.")
            code_frame.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email:\n{e}")

    tk.Button(frame, text="Send Verification Email", command=send_email, bg="#2980B9", fg="white").grid(row=6, column=1, sticky="w", pady=10)

    tk.Label(frame, text="Phone/Mobile:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    entry_phone = tk.Entry(frame, width=40)
    entry_phone.grid(row=7, column=1, padx=5, pady=5)

    code_frame = tk.Frame(email_win)
    tk.Label(code_frame, text="Enter Code:", font=("Arial", 12)).pack(side=tk.LEFT)
    code_entry = tk.Entry(code_frame, width=10, font=("Arial", 12))
    code_entry.pack(side=tk.LEFT, padx=5)
    tk.Button(code_frame, text="Verify", command=verify_code, bg="#27AE60", fg="white").pack(side=tk.LEFT)

    tk.Button(email_win, text="Submit", bg="#C0392B", fg="white", width=15, command=submit_form).pack(pady=15)




def generate_pdf_receipt(book_id, title, author, price, qty, total):
    now = datetime.now()
    filename = f"Receipt_{book_id}_{now.strftime('%Y%m%d%H%M%S')}.pdf"
    c = pdf_canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    logo_path = "E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_logos\\logo2.png"
    if os.path.exists(logo_path):
        logo_width = 120
        logo_height = 60
        c.drawImage(logo_path, (width - logo_width) / 2, height - 100, width=logo_width, height=logo_height, preserveAspectRatio=True)
        y = height - 120
    else:
        y = height - 80

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "Readers' Haven Bookstore")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y, "123 Book Street, Mumbai City, India - 400001")
    y -= 15
    c.drawCentredString(width / 2, y, "Phone: +91-0000000000 | Email: SK-bookshop12@gmail.com") #add your own details 
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y, "Purchase Receipt")
    y -= 10
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y, f"Receipt No: R-{book_id}-{now.strftime('%Y%m%d%H%M%S')}")
    y -= 30

    c.setFont("Helvetica", 11)
    spacing = 20
    items = [
        ("Date", now.strftime("%d-%m-%Y  %I:%M %p")),
        ("Book ID", book_id),
        ("Title", title),
        ("Author", author),
        ("Price ", f"{price:.2f}"),
        ("Quantity", qty),
        ("Total Amount ", f"{total:.2f}"),
        ("Payment Mode", "Online (UPI/Card)"),
    ]
    for label, value in items:
        c.drawString(60, y, f"{label}:")
        c.drawString(180, y, str(value))
        y -= spacing

    y -= 20
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(60, y, "Thank you for shopping with us at Readers' Haven!")
    y -= 15
    c.drawString(60, y, "We hope to see you again soon. Happy Reading!")
    y -=30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, y, 'Thank YOU FROM')
    y -=10
    c.drawString(60, y, 'SK_bookshop')
    c.save()
    return filename




def send_email_receipt(to_email, book_id, title, qty, total, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = 'Book Purchase Confirmation'
    msg['From'] = 'yourbookshop@gmail.com'
    msg['To'] = to_email
    body = f"""
Thank you for your purchase!

Book ID: {book_id}
Title: {title}
Quantity: {qty}
Total Paid: ₹{total:.2f}

Regards,
Bookshop Team
"""
    msg.set_content(body)

    try:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('your_email', 'your_API')  # add email and api key
            smtp.send_message(msg)
            messagebox.showinfo("Email Sent", f"Receipt sent to {to_email}")
            return True
    except Exception as e:
        messagebox.showerror("Email Error", str(e))
        return False

def buy_book_gui():
    def fetch_details():
        book_id = id_var.get().strip()
        if not book_id:
            messagebox.showwarning("Input Error", "Please enter a valid Book ID.")
            return

        try:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT title, author, price, qty FROM book_inventory WHERE id=%s", (book_id,))
            result = mycursor.fetchone()
            if result:
                title, author, price, stock = result
                detail_text.set(f"📘 Title: {title}\n✍️ Author: {author}\n💰 Price: ₹{price:.2f}\n📦 Stock: {stock}")
            else:
                detail_text.set("❌ Book not found.")
            mycursor.close()
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", "Failed to fetch book details.")

    def buy_book():
        book_id = id_var.get().strip()
        qty_str = qty_var.get().strip()

        if not book_id or not qty_str.isdigit() or int(qty_str) <= 0:
            messagebox.showwarning("Input Error", "Enter valid Book ID and positive quantity.")
            return

        qty_to_buy = int(qty_str)

        try:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT title, author, price, qty FROM book_inventory WHERE id=%s", (book_id,))
            result = mycursor.fetchone()

            if result:
                title, author, price, available_qty = result
                if qty_to_buy > available_qty:
                    messagebox.showerror("Stock Error", f"Only {available_qty} book(s) available.")
                    return

                total = qty_to_buy * price
                new_qty = available_qty - qty_to_buy
                mycursor.execute("UPDATE book_inventory SET qty=%s WHERE id=%s", (new_qty, book_id))
                mydb.commit()

                messagebox.showinfo("Success", f"✅ Purchased {qty_to_buy} book(s) of '{title}' for ₹{total:.2f}")

                pdf_file = generate_pdf_receipt(book_id, title, author, price, qty_to_buy, total)
                to_email = simpledialog.askstring("Email", "Enter email to receive receipt (optional):")
                if to_email:
                    send_email_receipt(to_email, book_id, title, qty_to_buy, total, pdf_file)
                else:
                    to_email = None

                now = datetime.now()
                mycursor.execute("""
                    INSERT INTO sales (book_id, title, author, price, quantity, total, email, purchase_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (book_id, title, author, price, qty_to_buy, total, to_email, now))
                mydb.commit()
                mycursor.close()

                id_var.delete(0, tk.END)
                qty_var.delete(0, tk.END)
                detail_text.set("")

            else:
                messagebox.showerror("Not Found", "Book ID not found.")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", "Error processing purchase.")

    win = tk.Toplevel()
    win.title("📚 Buy Book")
    win.geometry("450x400")
    win.configure(bg="#f0f8ff")

    header = tk.Label(win, text="Buy Book", font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#003366")
    header.pack(pady=10)

    frame = tk.Frame(win, bg="white", bd=2, relief="ridge", padx=10, pady=10)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    tk.Label(frame, text="Enter Book ID:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", pady=5)
    id_var = tk.Entry(frame, font=("Arial", 12))
    id_var.grid(row=0, column=1, pady=5)

    show_btn = tk.Button(frame, text="🔍 Show Details", font=("Arial", 10), command=fetch_details, bg="#add8e6")
    show_btn.grid(row=1, column=0, columnspan=2, pady=10)

    detail_text = tk.StringVar()
    detail_label = tk.Label(frame, textvariable=detail_text, justify="left", font=("Arial", 11), bg="white", fg="green", wraplength=350)
    detail_label.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="Enter Quantity:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w", pady=5)
    qty_var = tk.Entry(frame, font=("Arial", 12))
    qty_var.grid(row=3, column=1, pady=5)

    buy_btn = tk.Button(frame, text="🛒 Buy Book", command=buy_book, bg="green", fg="white", font=("Arial", 12, "bold"))
    buy_btn.grid(row=4, column=0, columnspan=2, pady=20)


def exit_Store():
    response=messagebox.askquestion("Confirmation","Are you Really want to Exit")
    res=response
    if res=="yes":
        w.destroy()
    else:
        messagebox.showinfo("Info","Good Choice")    
    print("***********************************************************************************")
    print("*****************************SUCCESSFULLY EXITED:**********************************")
    print("***********************************************************************************")

    print("                         *****  *      *  *****  *****                             ")
    print("                         *        *  *      *      *                               ")
    print("                         ***       *        *      *                               ")
    print("                         *        *  *      *      *                               ")
    print("                         *****  *      *  *****    *                               ")

    print("***********************************************************************************")
    print("*****************************SUCCESSFULLY EXITED:**********************************")
    print("***********************************************************************************")
'''image_path1="C:\\Users\\User\\Downloads\\bg_logo.jpg"
image1=Image.open(image_path1).resize((800,800))
tk_image1=ImageTk.PhotoImage(image1)'''

#image_path = "E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_Images\\alex-lvrs-2zDw14yCYqk-unsplash.jpg"
#image_path="F:\\SEMISTER IV\\Python\\python gui\\project2\\bg_logos\\logo.png"
#image_path="E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_Images\\pawel-czerwinski-4B3m1zRofV8-unsplash.jpg"
image_path="E:\\SEMISTER IV\\Python\\python gui\\project2\\bg_logos\\logo.png"
image = Image.open(image_path).resize((50, 50))
tk_image = ImageTk.PhotoImage(image)

canvas =tk.Canvas(w,width=50,height=50)
#canvas.grid(row=1,column=1,padx=10,pady=10)
canvas.place(relx=0.9,rely=0.9,anchor=CENTER,)
canvas.create_image(25,25,anchor=tk.CENTER,image=tk_image)

canvas = tk.Canvas(w, width=300, height=600, highlightbackground="blue", highlightthickness=3)
canvas.place(relx=0.7, rely=0.5, anchor=CENTER)
canvas.create_image(250, 250, anchor=tk.CENTER,)

label=Label(w,text="🔐Login Page🔐",font=("Arial",20,"bold"),fg="#2980B9")
canvas.create_window(150,50,window=label)

lb = Label(w, text="Username:", bg="lightgray", font=("Arial", 12, "bold"))
canvas.create_window(150, 100, window=lb)

entry_username = tk.Entry(w, bg="#ECF0F1",highlightbackground="cyan", highlightthickness=3,font=("Arial",12),bd=2)
canvas.create_window(150, 150, window=entry_username)

lb1 = Label(w, text="Password:", bg="lightgray", font=("Arial", 12, "bold"))
canvas.create_window(150, 200, window=lb1)

entry_password = Entry(w, bg="#ECF0F1", show="*", highlightbackground="cyan", highlightthickness=3,font=("Arial",12),bd=2)
canvas.create_window(150, 250, window=entry_password)

admin_radio = Radiobutton(w, text="👑Admin", variable=role, value="Admin", font=("Arial", 10, "bold"))
user_radio = Radiobutton(w, text="👤User", variable=role, value="User", font=("Arial", 10, "bold"))
canvas.create_window(100, 300, window=admin_radio)
canvas.create_window(200, 300, window=user_radio)

sp_label=Label(w,text="Admin Key",font=("Arial",14))
canvas.create_window(150,500,window=sp_label)
entry_sp=tk.Entry(w,show="$",font=("Arial",14))
canvas.create_window(150,550,window=entry_sp)

bt = Button(w, text="Login", bg="Green", bd=5, font=("Arial",12,"bold"),fg="white", width=18, height=1)
bt.bind("<Button-1>", getting_text)
canvas.create_window(150, 350, window=bt)

register_btn= Button(w, text="Register", bg="blue", bd=5 , font=("Arial",12,"bold"), width=18, height=1)
register_btn.bind("<Button-1>", register)
canvas.create_window(150, 400, window=register_btn)

bt1 = Button(w, text="Clear", bg="Red", bd=5, font=("Arial",12,"bold"), width=18, height=1,command=lambda: [entry_username.delete(0, END), entry_password.delete(0, END)])
canvas.create_window(150, 450, window=bt1)

'''def toggle_SP():
    if role.get()=="Admin":
        sp_label.place(x=300,y=150)
        entry_sp.place(x=500,y=150)
    else:
        sp_label.place_forget()
        entry_sp.place_forget()'''    

'''time_label = tk.Label(w, font=("Arial", 12), fg="white", bg="black")
time_label.place(x=1, y=1)
time()'''

#time_label=tk.Label(w,font=("Helvetica",16))
#canvas.create_window(50,50,window=time_label)

'''show_img=PhotoImage(file="E:\\SEMISTER IV\\Python\\python gui\\project2\\view.png")
hide_img=PhotoImage(file="E:\\SEMISTER IV\\Python\\python gui\\project2\\hidden.png")

toggle_btn=Button(w,image=show_img,command=toggle_pass,bd=0)
canvas.create_window(320,100,window=toggle_btn)'''

'''canvas = tk.Canvas(add_win, width=300, height=500, highlightbackground="blue", highlightthickness=3)
canvas.place(relx=0.7, rely=0.5, anchor=CENTER)
canvas.create_image(250, 250, anchor=tk.CENTER,)

lb3=Label(add_win,text="Title")
canvas.create_window(150,50,window=lb3)'''

'''w.bind("<Left>", lambda event: go_back())   
w.bind("<Right>", lambda event: go_forward())'''  


w.mainloop()
