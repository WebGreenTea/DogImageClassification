import os
from tkinter import *
from tkinter import filedialog
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.constants import *
from AI import AI


class Main():

    def __init__(self):
        self.root = Tk()
        self.aiModel = 'dog_AImodel.h5' #ai model 
        self.bg = '#2e2e2e' #background 1
        self.bg2 = '#424242'#background 2
        self.name = "" #program name
        self.ExampleImgPath = "img/" #path of example image

        self.AIlabel = []


        self.root.title("AI Dog")
        self.root.configure(bg=self.bg)
        self.root.geometry("900x1000+100+100")
        self.root.resizable(0, 0)
        #self.root.mainloop()

        

    def start(self):
        #show program name  
        self.f1 = Frame(self.root,bg=self.bg)
        self.f1.pack()
      
        self.mainLabel = Label(self.f1,text=self.name,font=('tahoma',40),fg='white' ,width=10,bg=self.bg)
        self.mainLabel.pack(pady=20,padx=10)

        self.f2 = Frame(self.root,bg=self.bg)
        self.f2.pack()
        
        #show Example Image
        col = 0
        row = 0
        self.ExampleImg = []
        allpic = os.listdir(self.ExampleImgPath)
        for pic in allpic:
            if(col%4 == 0 and col != 0):
                col = 0
                row+=1
            expic = Frame(self.f2,bg=self.bg)
            img = Image.open(self.ExampleImgPath+pic).resize((200,200))
            print(img)
            ph = ImageTk.PhotoImage(img)
            Label(expic,image=ph,bg=self.bg).pack()
            self.ExampleImg.append(ph)
            picname = pic.split(".")[0]
            Label(expic,text=picname,fg='white',font=('tahoma',20),bg=self.bg).pack()
            self.AIlabel.append(picname)
            expic.grid(row=row,column=col)
            col+=1
        print(self.AIlabel)

        #show browse Button
        Frame(self.root,height=25,bg=self.bg).pack()
        self.f3 = Frame(self.root,bg=self.bg2)
        self.f3.pack()
        Label(self.f3,text="เลือก Folder รูปภาพของคุณ" ,fg='white' ,font=('tahoma',16),bg=self.bg2).grid(row=0, column=0)
        Browsebtn = Button(self.f3,text="Browse",command=self.browse_button,font=('tahoma',14)).grid(row=0,column=1,padx=40,pady=10)

        
        #self.label['text'] = "Text updated"  

        #self.fcount = Frame(self.root,bg=self.bg,width=859,height=35)
        #self.fcount.pack()
        self.countxt = Label(self.root,text='Chihuahua 0 | Doberman 0 | Pug 0 | Siberian-Husky 0',font=('tahoma',16))
        self.countxt.pack(pady=10)

        #clear button
        self.fclearbtn = Frame(self.root,bg=self.bg,width=850,height=25)
        self.fclearbtn.pack()
        self.clearBtn = Button(self.fclearbtn,text='Clear X',anchor="e",command=self.clear).place(x=800,y=0)

        #show result image
        self.fileName = []
        self.imgFilePath = []
        self.result = []
        self.images = []
        
        self.f4 = Frame(self.root)
        self.f4.pack()
        # --- create canvas with scrollbar ---
        self.canvas = Canvas(self.f4,width=850,height=515,bg=self.bg2)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        scrollbar = tk.Scrollbar(self.f4, command=self.canvas.yview,bg='gray')
        scrollbar.pack(side=tk.LEFT, fill='y')

        self.canvas.configure(yscrollcommand = scrollbar.set)

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.bind('<Configure>', self.on_configure)

        # --- put frame in canvas ---

        self.frame = Frame(self.canvas,bg=self.bg2)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        self.root.mainloop()

        

    def on_configure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _on_mousewheel(self,event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def browse_button(self):
        filepath = filedialog.askdirectory()
        self.pathImg = filepath
        print(filepath)
        
        if(filepath != ''):
            self.clear()
            for Fname in os.listdir(filepath):
                self.fileName.append(Fname)
            for path in Path(filepath).iterdir():
                self.imgFilePath.append(path)
            self.AI()
    
    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
            self.fileName = []
            self.imgFilePath = []
            self.result = []
            self.images = []
        self.countxt.configure(text='Chihuahua 0 | Doberman 0 | Pug 0 | Siberian-Husky 0')
        
        

        
    def AI(self):
        Predic = AI()
        self.result = Predic.getResultList(self.imgFilePath,self.AIlabel,self.aiModel,raw=0)

        coutstr = ''
        for i in self.AIlabel:
            coutstr+= f'{i} {self.result.count(i)}'
            if(i != self.AIlabel[len(self.AIlabel)-1] ):
                coutstr += ' | '

        self.countxt.configure(text=coutstr)


        row = 1
        col = 0
        for i in range(0,len(self.fileName)):
            #print(i)
            print
            if(i%5 == 0 and i != 0):
                row+=1
                col = 0

            img = Image.open(self.imgFilePath[i]).resize((166,166),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.images.append(img)

            pltResult = plotResult(self.frame)
            pltResult.bg = self.bg
            pltResult.getResultFrame(self.fileName[i],img,self.result[i]).grid(row=row,column=col,pady=5)
            col+=1
        self.frame.bind('<Configure>', self.on_configure)


class plotResult():
    def __init__(self,root):
        self.root = root
        self.bg ='gray' #defult bg color is gray 
        
    def getResultFrame(self,filename,img,result):
        frame = Frame(self.root,bg=self.bg)
        Label(frame,text=filename,fg='white',bg=self.bg,width=20).pack()
        Label(frame,image=img,bg=self.bg).pack()
        Label(frame,text=result,bg=self.bg,fg='white',font=('tahoma',12)).pack()
        return frame


app = Main()
app.name = "Dog Classify"
app.aiModel = "dog_AImodel83.h5"
app.start()
