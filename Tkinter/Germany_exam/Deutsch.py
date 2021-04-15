import tkinter as tk
import sqlite3
import random
#______________________IMPORT DATA__________________________
con=sqlite3.connect('data_deutsch.sqlite')

c = con.cursor()

with con:
    c.execute(''' select * from beta_test''')

data = c.fetchall()

con.close()

#___________________________CHOOSE FROM DATA_____________________

def shuffle(data,itr,num):
    var=['A)','B)','C)','D)','E)']
    first, *middle,last=data
    random.shuffle(middle)
    first= first.replace(  ('{}'.format(num+1)) , ('{}'.format(itr+1)))
    
    for j,v1 in enumerate(middle):
        
        for i,v in enumerate(var):
            if v in v1:
                middle[j]=(v1.replace(v,var[j]))
    
    out=   [first] + middle +[last]
    
    return tuple(out)

question_num=random.sample(range(0, 303), 25)
test=[]
for i,j in enumerate(question_num):
    
    question=shuffle(data[j],  i, j)
    test.append(question)







class Exam:
    
    variants={'a':0,'b':1,'c':2,'d':3,'e':4}
    std_ans=['']*25
    ques=0
    
    colors={0:[10,10,10,10,10],1:[10,10,10,10,10],2:[10,10,10,10,10],3:[10,10,10,10,10],
            4:[10,10,10,10,10],5:[10,10,10,10,10],6:[10,10,10,10,10],7:[10,10,10,10,10],
            8:[10,10,10,10,10],9:[10,10,10,10,10],10:[10,10,10,10,10],11:[10,10,10,10,10],
            12:[10,10,10,10,10],13:[10,10,10,10,10],14:[10,10,10,10,10],15:[10,10,10,10,10],
            16:[10,10,10,10,10],17:[10,10,10,10,10],18:[10,10,10,10,10],19:[10,10,10,10,10],
            20:[10,10,10,10,10],21:[10,10,10,10,10],22:[10,10,10,10,10],23:[10,10,10,10,10],
            24:[10,10,10,10,10]
            
            }
    
    
    def __init__(self,questions):
        self.root= tk.Tk()
        self.configs()
        self.questions=questions
        
    def configs(self):
        
        self.root.geometry('700x500')
        self.root.resizable(0,0)
        self.root.config(background='#856ff8')
                    
    def comand(self):
         x = self.radiovar.get()
         Exam.std_ans[Exam.ques]=x
         self.radiovar.set(-1)
         
         if Exam.ques < 24:
             self.quest.config(text= self.questions[Exam.ques][0])
             
             self.b1['text'] = self.questions[Exam.ques][1]
             self.b2['text'] = self.questions[Exam.ques][2]
             self.b3['text'] = self.questions[Exam.ques][3]
             self.b4['text'] = self.questions[Exam.ques][4]
             self.b5['text'] = self.questions[Exam.ques][5]
             
             for i in range(5):
                 if i == Exam.variants[x]:
                     Exam.colors[ Exam.ques ][ i ] = 15
                 else:
                     Exam.colors[ Exam.ques ][ i ] = 10
             
             
             
             Exam.ques += 1
             self.destroy_f()
         else:
              Exam.ques = 0
              self.destroy_f()
        
        
    def destroy_f(self):
        
        self.quest.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.b4.destroy()
        self.b5.destroy()
        self.choice()
        
    def next_fun(self):
        if Exam.ques <24:
            Exam.ques+=1
        else:
            Exam.ques=0
        self.quest.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.b4.destroy()
        self.b5.destroy()
        
        self.choice()
    
    
    def prev(self):
        if Exam.ques==0:
            Exam.ques=24
        else:    
            Exam.ques-=1
        self.quest.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.b4.destroy()
        self.b5.destroy()
        self.choice()
        
        
    def submit_f(self):
        self.quest.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.b4.destroy()
        self.b5.destroy()
        self.root.destroy()
        
    def choice(self):
        #_______________QUESTION______________________
        self.quest=tk.Label(text=(self.questions[Exam.ques][0]),
                       font = ("Consolas", 18),
                       width = 600,
                       justify = "center",
                       wraplength = 600,
                       background = "#856ff8",
                       )
        
        self.quest.pack(pady=(30,10))
        
        
        
        self.radiovar = tk.StringVar()
        self.radiovar.set(-1)
        
        #__________________BUTTON 1____________________________
        self.b1= tk.Radiobutton(self.root,text=self.questions[Exam.ques][1],
                           value='a',
                           font = ("Times", Exam.colors[ Exam.ques ][0]    ),
                           
                           background = "#856ff8",
                           variable=self.radiovar,
                           command=self.comand
                      
                            )

        self.b1.place(x=130,y=190)
        #_________________________BUTTON 2_______________________
        self.b2= tk.Radiobutton(self.root,text=self.questions[Exam.ques][2],
                           value='b',
                           font = ("Times", Exam.colors[ Exam.ques ][1]),
                           background = "#856ff8",
                           variable=self.radiovar,
                           command=self.comand
                           )
        self.b2.place(x=130,y=240)
        #_________________________BUTTON 3_______________________

        self.b3= tk.Radiobutton(self.root,text=self.questions[Exam.ques][3],
                           value='c',
                           font = ("Times", Exam.colors[ Exam.ques ][2]),
                           background = "#856ff8",
                           variable=self.radiovar,
                           command=self.comand
                            )
        self.b3.place(x=130,y=300)
        
        #_________________________BUTTON 4_______________________

        self.b4= tk.Radiobutton(self.root,text=self.questions[Exam.ques][4],
                           value='d',
                           font = ("Times", Exam.colors[ Exam.ques ][3]),
                           background = "#856ff8",
                           variable=self.radiovar,
                           command=self.comand
                            )
        self.b4.place(x=130,y=360)
        #_________________________BUTTON 5_______________________

        self.b5= tk.Radiobutton(self.root,text=self.questions[Exam.ques][5],
                           value='e',
                           font = ("Times", Exam.colors[ Exam.ques ][4]  ),
                           background = "#856ff8",
                           variable=self.radiovar,
                           command=self.comand
                            )
        self.b5.place(x=130,y=420)
        
        
        #____________________BUTTON_COMMANDS______________________________
            
            
            
        self.previous= tk.Button(self.root,text='Previous',command=self.prev)
        self.previous.place( x=500,y=450 )
        self.next = tk.Button(self.root,text='Next',command=self.next_fun)
        self.next.place( x=570, y=450   )
        self.submit = tk.Button(self.root , text = 'Submit answers',command=self.submit_f)
        self.submit.place(x=10,y=10)
        
    

class Result:
    num=0
    
    variants_num={0:'a',1:'b',2:'c',3:'d',4:'e'}
    
    variants={'a':1,'b':2,'c':3,'d':4,'e':5}
    
    
    your_selec = Exam.std_ans
    subm= []
    corrects=[]
    
    def __init__(self,questions):
        self.root= tk.Tk()
        self.configs()
        self.questions=questions
        
    def configs(self):
        self.root.geometry('700x500')
        self.root.resizable(0,0)
        self.root.config(background='#856ff8')
    
    def istrue(self,ans_stud , quest , stud):
        first=quest[ans_stud].replace(   ('{})'.format(stud.upper())) , ''  )
        second= quest[-1]
        
        
        return  first==second                     
    
    def check(self):
        self.var=['a','b','c','d','e']
        
        for i,v in enumerate(self.questions):
            
            for k in self.var:
                if self.istrue(  Result.variants[k]   ,v,k   ) :
                    Result.corrects.append(k)
                    break
            else:
                Result.corrects.append('None')
                
                
            try:
                if self.istrue(  Result.variants[ Result.your_selec[i]  ] ,  v , Result.your_selec[i]  ):
                    Result.subm.append('+')
                    #score+=1
                else:
                    Result.subm.append( '-' )
            except KeyError:
                Result.subm.append( '-' )
            
        
    
            
    def total_res(self):
        
        total= tk.Label(text = 'Your score is {}/25'.format( Result.subm.count('+') )  )
        
        total.place(x=300,y=10)
                     
                         
    def prev(self):
        if Result.num==0:
            Result.num=24
        else:    
            Result.num-=1
        self.quest.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.b4.destroy()
        self.b5.destroy()
        self.selected()
        
    def next_fun(self):
        if Result.num <24:
            Result.num+=1
        else:
            Result.num=0
        self.quest.destroy()
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.b4.destroy()
        self.b5.destroy()
        
        self.selected()    
                         
    
    def selected(self):
        
        if Result.subm[Result.num] == '+':
            
            self.answ= tk.Label( text= 'correct var is {}'.format(Result.corrects[Result.num].upper())    , 
                                    background='green'
                                )
            
            self.answ.place(x=10,y=10)
        else:
            self.answ= tk.Label( text= 'correct var is {}'.format(Result.corrects[Result.num].upper())    , 
                                 background='red'
                                )
            
            self.answ.place(x=10,y=10)
            
        
        
        
        
        
        
        
        
        #_______________QUESTION______________________
        self.quest=tk.Label(text=(self.questions[Result.num][0]),
                       font = ("Consolas", 18),
                       width = 600,
                       justify = "center",
                       wraplength = 600,
                       background = "#856ff8",
                       )
        
        self.quest.pack(pady=(30,10))
        
        
        
        self.radiovar = tk.StringVar()
        self.radiovar.set(-1)
        
        #__________________BUTTON 1____________________________
        self.b1= tk.Radiobutton(self.root,text=self.questions[Result.num][1],
                           value='a',
                           font = ("Times", Exam.colors[ Result.num ][0]    ),
                           
                           background = "#856ff8",
                           variable=self.radiovar
                           
                      
                            )

        self.b1.place(x=130,y=190)
        #_________________________BUTTON 2_______________________
        self.b2= tk.Radiobutton(self.root,text=self.questions[Result.num][2],
                           value='b',
                           font = ("Times", Exam.colors[ Result.num ][1]),
                           background = "#856ff8",
                           variable=self.radiovar
                           
                           )
        self.b2.place(x=130,y=240)
        #_________________________BUTTON 3_______________________

        self.b3= tk.Radiobutton(self.root,text=self.questions[Result.num][3],
                           value='c',
                           font = ("Times", Exam.colors[ Result.num ][2]),
                           background = "#856ff8",
                           variable=self.radiovar
                           
                            )
        self.b3.place(x=130,y=300)
        
        #_________________________BUTTON 4_______________________

        self.b4= tk.Radiobutton(self.root,text=self.questions[Result.num][4],
                           value='d',
                           font = ("Times", Exam.colors[ Result.num ][3]),
                           background = "#856ff8",
                           variable=self.radiovar
                           
                            )
        self.b4.place(x=130,y=360)
        #_________________________BUTTON 5_______________________

        self.b5= tk.Radiobutton(self.root,text=self.questions[Result.num][5],
                           value='e',
                           font = ("Times", Exam.colors[ Result.num ][4]  ),
                           background = "#856ff8",
                           variable=self.radiovar
                           
                            )
        self.b5.place(x=130,y=420)
        
        
        #____________________BUTTON_COMMANDS______________________________
            
            
            
        self.previous= tk.Button(self.root,text='Previous',command=self.prev)
        self.previous.place( x=500,y=450 )
        self.next = tk.Button(self.root,text='Next',command=self.next_fun)
        self.next.place( x=570, y=450   )
        
        




obj= Exam(test)
obj.choice()
obj.root.mainloop()




your_res= Result(test)

your_res.check()



your_res.selected()

your_res.total_res()




your_res.root.mainloop()










