''' 

B. YUGENDHRA BABU         (19NA1A0501)
CH. HANISHA               (19NA1A0524)
B. VANI SRI               (19NA1A0504)
S. SOMA SRIKRIAN          (19NA1A0538)
                        
'''





from tkinter import *
import pandas as pd
import tkinter as tk
from playsound import playsound
from PIL import Image, ImageTk
import numpy as np
from tkinter import ttk
import sqlite3
import cv2
import os
import xlsxwriter
from datetime import date
from tkinter import messagebox
import sys
import random


#===========================================================Create Database=====================================================
def createdb():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT , passs TEXT,sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)")
    conn.commit()
    conn.close()
createdb()


#==================================================UpdatingDatabaseStatuscolumeveryday==========================================
def cldata():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE employees set status=' '")
    conn.commit()
    conn.close()







#======================================================Addadminindatabase=======================================================
def saveadmin():
	name_err = name_entry.get()
	pass_err = pass_entry.get()
	if name_err == "":
		messagebox.showinfo("Invalid input","Username can't be Empty")
	elif pass_err == "":
		messagebox.showinfo("Invalid input","Password can't be Empty")
	else:
		conn=sqlite3.connect("database.db")
		c=conn.cursor()
		c.execute("INSERT INTO users(name,passs) VALUES(?,?) ",(name_entry.get(),pass_entry.get()))
		conn.commit()
		messagebox.showinfo("Information","New User has been Added")


#==================================================FetchingAdmindatafromdatabase=================================================
def loggin():
	while True:
		a=name2_entry.get()
		b=pass2_entry.get()
		with sqlite3.connect("database.db") as db:
			cursor=db.cursor()
		find_user= ("SELECT * FROM users WHERE name = ? AND passs = ?")
		cursor.execute(find_user,[(a),(b)])
		results=cursor.fetchall()
		if results:
			for i in results:
				cldata()
				window.destroy()
				
				
				#playvideo()				
#=======================================================Window2+CreateFrame+f1==================================================
				window2=Tk()
				window2.title("SMART ATTENDANCE SYSTEM")

				f1=Frame(window2,bg='black')
				f2=Frame(window2)
				f3=Frame(window2)
				f4=Frame(window2)
				def swap(frame):
					frame.tkraise()
				for frame in(f1,f2,f3,f4):
					frame.place(x=0,y=0,width=1500,height=690)
				window2.geometry("1500x701")
				window2.config(bg='black')


				m9=Label(f1,text="LINGYAS INSTITUTE OF MANAGEMENT AND TECHNOLOGY",bg="lightblue",font=('times',28,'bold'))
				m9.pack(side=TOP,fill=X)


				label3=Label(f1,text="WELCOME",font=("arial",20,"bold"),bg="lightgreen",fg="black",relief=SUNKEN)
				label3.pack(side=TOP,fill=X)
				filename = PhotoImage(file="bg1.png")
				background_label = Label(f1,
                                                         image=filename
                                                         )
				background_label.pack()


				m9=Label(f2,text="LINGYAS INSTITUTE OF MANAGEMENT AND TECHNOLOGY",bg="lightblue",font=('times',28,'bold'))
				m9.pack(side=TOP,fill=X)


				statusbar=Label(f1,text="Project by Yugendra, Hanisha, Vanisri, Sri Kiran, ",font=("arial",13,"bold"),bg="black",fg="white",relief=SUNKEN)
				statusbar.pack(side=BOTTOM,fill=X)

#=================================================================PlayingGif=======================================================
				m7=Label(f3,text="LINGYAS INSTITUTE OF MANAGEMENT AND TECHNOLOGY",bg="lightblue",font=('times',28,'bold'))
				m7.pack(side=TOP,fill=X)

				label4=Label(f3,text="Project by Yugendra, Hanisha, Vanisri, Sri Kiran, ",font=("arial",10,"bold"),bg="grey16",fg="white")
				label4.pack(side=BOTTOM,fill=X)
				
				labelA=Label(f2,text="Project by Yugendra, Hanisha, Vanisri, Sri Kiran, ",font=("arial",10,"bold"),bg="grey16",fg="white")
				labelA.pack(side=BOTTOM,fill=X)

				labelB=Label(f4,text="Project by Yugendra, Hanisha, Vanisri, Sri Kiran, ",font=("arial",10,"bold"),bg="grey16",fg="white")
				labelB.pack(side=BOTTOM,fill=X)



#=======================================================Trian System=============================================================


				def trainsystem():
					recognizer = cv2.face.LBPHFaceRecognizer_create()
					path = 'dataset'
					if not os.path.exists('./recognizer'):
						os.makedirs('./recognizer')
					def getImagesWithID(path):
						imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
						faces = []
						IDs = []
						for imagePath in imagePaths:
							faceImg = Image.open(imagePath).convert('L')
							faceNp = np.array(faceImg,'uint8')
							ID = int(os.path.split(imagePath)[-1].split('.')[1])
							faces.append(faceNp)
							IDs.append(ID)
							cv2.imshow("training",faceNp)
							cv2.waitKey(10)
						cv2.destroyAllWindows()	
						return np.array(IDs), faces
					Ids, faces = getImagesWithID(path)
					recognizer.train(faces,Ids)
					recognizer.save('recognizer/trainingData.yml')
					statusbar['text']='System Trained and model updated'
					cv2.destroyAllWindows()


#==========================================================MarkingAttendence========================================================

				def markattendance():
					if not os.path.exists('./Attendance'):
							os.makedirs('./Attendance')
					statusbar['text']='Attendance Marked....'
					conn = sqlite3.connect('database.db',timeout=10)
					c = conn.cursor()
					fname = "recognizer/trainingData.yml"
					if not os.path.isfile(fname):
					  print("Please train the data first")
					  exit(0)
					face_cascade = cv2.CascadeClassifier('./Resources/haarcascade_frontalface_default.xml')
					cap = cv2.VideoCapture(0)
					recognizer = cv2.face.LBPHFaceRecognizer_create()
					recognizer.read(fname)
					while True:
					  ret, img = cap.read()
					  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
					  for (x,y,w,h) in faces:
					    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
					    ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
					    c.execute("select name from employees where id = (?);", (ids,))
					    result = c.fetchall()
					    name = result[0][0]
					    rname=str(name)
					    if conf < 50:
					      cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX ,1,(0,255,255),1)
					      cv2.putText(img,'Hit Enter if you are '+name,(10,30),cv2.FONT_HERSHEY_COMPLEX,1,(34,34,230),2)
					    else:
					      cv2.putText(img, 'No Match contact supervisor', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
					  cv2.imshow('Face Recognizer',img)
					  k = cv2.waitKey(30) & 0xff
					  if k == 13:
					  	c.execute("UPDATE employees set status='present' WHERE id=(?);",(ids,))
					  	c.execute("SELECT * FROM employees")
					  	employee_result = c.fetchall()
					  	stat=str(employee_result)
					  	time=str(date.today())
					  	df=pd.DataFrame(employee_result, columns=['id', 'Name', 'Department','Roll NO','Status'])
					  	datatoexcel = pd.ExcelWriter("./Attendance/Student Attendance"+time+".xlsx", engine='xlsxwriter')
					  	df.to_excel(datatoexcel, index= False, sheet_name = "Sheet1")
					  	worksheet = datatoexcel.sheets['Sheet1']
					  	worksheet.set_column('A:A', 8)
					  	worksheet.set_column('B:B', 20)
					  	worksheet.set_column('C:C', 25)
					  	worksheet.set_column('D:D', 20)
					  	worksheet.set_column('E:E', 20)
					  	worksheet.set_column('F:F', 20)
					  	datatoexcel.save()
					  	playsound('./Resources/1594026458-text2voice.mp3')
					  	break
					cap.release()
					conn.commit()
					conn.close()
					cv2.destroyAllWindows()


#===============================================================  Frame2(User pannel)===================================================

				label5=Label(f2,text="Student Management (Add Student Details)",font=("arial",20,"bold"),bg="grey16",fg="white")
				label5.pack(side=TOP,fill=X)

				label6=Label(f2,text="Name",font=("arial",12,"bold"))
				label6.place(x=625,y=200)
				
				entry6=StringVar()
				entry6=ttk.Entry(f2,textvariable=entry6)
				entry6.place(x=750,y=200)
				entry6.focus()

				label7=Label(f2,text="Department",font=("arial",12,"bold"))
				label7.place(x=625,y=300)

#================================================================SelectionColumn=====================================================				
				entry7=StringVar()
				combo=ttk.Combobox(f2,textvariable=entry7,width=15,font=("arial",10,"bold"),state='readonly')
				combo['values']=("ECE","CSE","IT","EEE","CIVIL","MECHANICAL","MBA","FACULTY")
				combo.place(x=750,y=300)

				
				label8=Label(f2,text="ROLL NO.",font=("arial",12,"bold"))
				label8.place(x=625,y=400)
				
				entry8=StringVar()
				entry8=ttk.Entry(f2,textvariable=entry8)
				entry8.place(x=750,y=400)

				btn1w2=tk.Button(f1,text="Add Student",bg='lightblue',command=lambda:swap(f2),activebackground = "lightgreen",font=("arial",12,"bold"))
				btn1w2.place(x=1150, y=100,width=200,height=65)

				btn2w2=tk.Button(f1,text="Train System",command=trainsystem,bg='lightblue',activebackground = "lightgreen",font=("arial",12,"bold"))
				btn2w2.place(x=1150, y=225,width=200,height=65)

				btn3w2=tk.Button(f1,text="Mark Attendance",command=markattendance,bg='lightblue',activebackground = "lightgreen",font=("arial",12,"bold"))
				btn3w2.place(x=1150, y=350,width=200,height=65)

#=============================================================CaptureAndSaveintoDatabase==============================================

				def capture_images():
					conn = sqlite3.connect('database.db')
					c = conn.cursor()
					sql = """;
					CREATE TABLE IF NOT EXISTS employees (
								id integer unique primary key autoincrement,
								name text,dept text,contactno text,Status text
					);
					"""
					c.executescript(sql)
					if not os.path.exists('./dataset'):
						os.makedirs('./dataset')
					uname=entry6.get()
					up1=uname.upper()
					dep=entry7.get()
					cont=entry8.get()
					if uname=="":
						messagebox.showerror("Error","Please Enter Student Name")
					elif dep=="":
						messagebox.showerror("Error","Please Select Department")
					elif cont=="":
						messagebox.showerror("Error","Please Enter Roll no")
					else:
						c.execute('INSERT INTO employees (name,dept,contactno) VALUES (?,?,?)', (up1,dep,cont))
						uid = c.lastrowid
						face_classifier=cv2.CascadeClassifier("./Resources/haarcascade_frontalface_default.xml")

						def face_extractor(img):
							gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
							faces=face_classifier.detectMultiScale(gray,1.2,7)
							if faces is():
								return None
							for(x,y,w,h) in faces:
								cropped_face=img[y:y+h,x:x+w]
							return cropped_face
						cap=cv2.VideoCapture(0)
						count=0
						while True:
							ret,frame=cap.read()
							if face_extractor(frame) is not None:
								count+=1
								face=cv2.resize(face_extractor(frame),(400,400))
								face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
								file_name_path="dataset/"+up1+"."+str(uid)+"."+str(count)+".jpg"
								cv2.imwrite(file_name_path,face)
								cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)
								cv2.imshow("Face are being captured",face)
							else:
								print("face not found")
								pass
							if cv2.waitKey(1)==13 or count==70:
								break
						cap.release()						
						conn.commit()
						conn.close()
						cv2.destroyAllWindows
						statusbar['text']='Student has been Added....'
    
						messagebox.showinfo("Information","Images has been collected")


				btn5w2=tk.Button(f2,text="Capture and Save credentials",command=capture_images,bg='lightgray',activebackground = "lightgreen",font=("arial",12,"bold"))
				btn5w2.place(x=600, y=500,width=300,height=50)

				btn4w2=tk.Button(f2,text="Back",bg='red',command=lambda:swap(f1),activebackground = "red",font=("arial",12,"bold"))
				btn4w2.place(x=0, y=85,width=150,height=30)
				def swap2(frame):
					frame.tkraise()

				btn7w2=tk.Button(f3,text="Back",command=lambda:swap(f1),activebackground = "red",font=("arial",12,"bold"),bg='red')
				btn7w2.place(x=0, y=85,width=150,height=30)

				btn6w2=tk.Button(f1,text="View Student's Data",command=lambda:swap2(f3),bg='lightblue',activebackground = "lightgreen",font=("arial",12,"bold"))
				btn6w2.place(x=1150, y=475,width=200,height=65)

#=============================================================Window2Frame1ExitButton===============================================

				def quit():
					window2.destroy()


				btn9w2=tk.Button(f1,text="Exit",command=quit,activebackground = "red",font=("arial",12,"bold"),bg='lightblue')
				btn9w2.place(x=1150, y=600,width=200,height=65)

#============================================================FETCHDATABASEINLISTVIEW================================================	


				def fetch():
					conn = sqlite3.connect("database.db")
					cur = conn.cursor()
					cur.execute("SELECT * FROM employees")
					rows = cur.fetchall()
					for row in rows:
						List_Table.insert("", tk.END, values=row)
					conn.close()

#===============================================================ButtontoViewRecordfromDatabase======================================

				btn8w2=tk.Button(f3,text="View Record",command=fetch,font=("arial",12,"bold"),bg='lightyellow',activebackground = "lightgreen")
				btn8w2.place(x=700, y=600,width=130,height=40)

#================================================================Frame3TableshowingRecords==========================================


				label8=Label(f3,text="Student Records",font=("arial",20,"bold"),bg="grey16",fg="white")
				label8.pack(side=TOP,fill=X)

				Detail_Frame=Frame(f3,bd=4,relief=RIDGE,bg="black")
				Detail_Frame.place(x=30,y=150,width=1200,height=400)
				
				scroll_x=Scrollbar(Detail_Frame,orient=HORIZONTAL)
				scroll_y=Scrollbar(Detail_Frame,orient=VERTICAL)
				
				List_Table=ttk.Treeview(Detail_Frame,columns=("1","2","3","4","5"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
				scroll_x.pack(side=BOTTOM,fill=X)
				scroll_y.pack(side=RIGHT,fill=Y)
				scroll_x.config(command=List_Table.xview)
				scroll_y.config(command=List_Table.yview)
				
				List_Table.heading("1",text="ID")
				List_Table.heading("2",text="Name")
				List_Table.heading("3",text="Department")
				List_Table.heading("4",text="Roll No")
				List_Table.heading("5",text="Status")
				List_Table['show']='headings'
				List_Table.column("1",width=50)
				List_Table.column("2",width=350)
				List_Table.column("3",width=350)
				List_Table.column("4",width=350)
				List_Table.column("5",width=350)
				List_Table.pack(fill=BOTH,expand=1)

				f1.tkraise()
				window2.mainloop()

			break
		else:
			messagebox.showerror("Error","invalid username or password")
			break



#==================================================================MainLoginScreen==================================================




window=Tk()
window.title("Login Panel")
window.configure(bg='lightblue')


nb=ttk.Notebook(window)
m=Message(window,text="    LINGYAS INSTITUTE OF MANAGEMENT AND TECHNOLOGY")
m.config(bg="lightblue",font=('times',28,'bold'),aspect=20000)

m.pack()

                

Label1=Label(window,text="Admin Home (Enter your credentials)",font=("arial",15,"bold"),bg="lightgreen",fg="black")
Label1.pack(side=TOP,fill=X)



Label2=Label(window,text="Project by Yugendra, Hanisha, Vanisri, Sri Kiran, ",font=("arial",10,"bold"),bg="black",fg="white")
Label2.pack(side=BOTTOM,fill=X)

#=================================================================LoginandSignupTabs=============================================
tab1=tk.Frame(nb)
tab1.configure(bg='lightblue')
filename = PhotoImage(file="bg1.png")
background_label = Label(tab1,
                         image=filename
                         )
background_label.pack()
tab2=ttk.Frame(nb)
background_label2 = Label(tab2,
                         image=filename
                         )
background_label2.pack()
nb.add(tab1,text="Login")

nb.add(tab2,text="Sign_up")
nb.pack(expand=True,fill="both")

#==============================================================Logintab==========================================================

name2_label=Label(tab1,text="Name",font=("arial",13,"bold"),bg='black',fg='white')
name2_label.place(x=625,y=200)

name2_entry=StringVar()
name2_entry=ttk.Entry(tab1,textvariable=name2_entry)
name2_entry.place(x=750,y=200)
name2_entry.focus()

pass2_label=Label(tab1,text="Password",font=("arial",13,"bold"),bg='black',fg='white')
pass2_label.place(x=625,y=250)
pass2_entry=StringVar()
pass2_entry=ttk.Entry(tab1,textvariable=pass2_entry,show="*")
pass2_entry.place(x=750,y=250)

#============================================================SignupTab==========================================================
name_label=Label(tab2,text="Name",font=("arial",13,"bold"),bg='black',fg='white')
name_label.place(x=625,y=200)
name_entry=StringVar()
name_entry=ttk.Entry(tab2,textvariable=name_entry)
name_entry.place(x=800,y=200)
name_entry.focus()
pass_label=Label(tab2,text="Create Password",font=("arial",13,"bold"),bg='black',fg='white')
pass_label.place(x=625,y=250)
pass_entry=StringVar()
pass_entry=ttk.Entry(tab2,textvariable=pass_entry,show="*")
pass_entry.place(x=800,y=250)

def clear():
	name_entry.delete(0,END)
	pass_entry.delete(0,END)
#==============================================================SigninButtons====================================================
btn1=tk.Button(tab2,text="Create Account",width=15,command=saveadmin,fg ="white", bg ="green",font=("arial",10,"bold"))
btn1.place(x=550,y=350)

btn2=tk.Button(tab2,text="Clear",width=15,command=clear,fg ="white", bg ="red",font=("arial",10,"bold"))
btn2.place(x=850,y=350)
#=========================================================LoginButtonMainwindow1==================================================
btn3=tk.Button(tab1,text="Login",width=15,command=loggin,activebackground = "green",font=("arial",10,"bold"))
btn3.place(x=550,y=350)

btn4=tk.Button(tab1,text="Clear",width=15,command=clear,fg ="white", bg ="red",font=("arial",10,"bold"))
btn4.place(x=850,y=350)

window.geometry("1500x700")
window.mainloop()
