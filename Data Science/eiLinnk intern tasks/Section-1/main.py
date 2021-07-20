import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilename
from tkinter import *
import seaborn as sns
import numpy as np


class GUI():
    def __init__(self):
        self.root = Tk()
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#ffffff' # X11 color: 'white'
        _ana1color = '#ffffff' # X11 color: 'white'
        _ana2color = '#ffffff' # X11 color: 'white'
        font14 = "-family {Segoe UI} -size 15 -weight bold -slant "  \
                "roman -underline 0 -overstrike 0"
        font16 = "-family {Swis721 BlkCn BT} -size 40 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
                "roman -underline 0 -overstrike 0"

        self.root.geometry("500x500")
        self.root.title("Section 1")
        self.root.configure(background="#d9d9d9")
        self.root.configure(highlightbackground="#d9d9d9")
        self.root.configure(highlightcolor="black")

        self.root.configure(relief=GROOVE)
        self.root.configure(borderwidth="2")
        self.root.configure(relief=GROOVE)
        self.root.configure(background="#d9d9d9")
        self.root.configure(highlightbackground="#d9d9d9")
        self.root.configure(highlightcolor="black")

        self.Frame1 = Frame(self.root)
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.grid(row=0, column=0,)
        

        self.Frame2 = Frame(self.root)
        self.Frame2.configure(background="#d9d9d9")
        self.Frame2.grid(row=1, column=0 )


        figure1 = plt.Figure(figsize=(5,4), dpi=90)
        figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.Frame2)
        self.tk_wid = bar1.get_tk_widget()
        self.tk_wid.grid( column=0 , row=0, padx= 20 )
        

        self.set_UI()

        self.root.mainloop()

    def set_UI(self):
        # ----------- Load button ---------
        self.load_btn = Button( self.Frame1, text = "Load" , command = self.load_file )
        self.load_btn.grid( column = 0, row = 0, padx = 50 , pady= 8)
        
        # ----------- Ptot button ---------
        self.vis_btn = Button( self.Frame1, text = "Visualize" , command = self.plot )
        self.vis_btn.grid( column = 1, row = 0, padx = 50 , pady= 8)
        # ----------- R square button ---------
        self.r_btn = Button( self.Frame1, text = "R Square" , command = self.r_square )
        self.r_btn.grid( column = 2, row = 0, padx = 50 , pady= 8)
        # ----------- R square label ---------
        self.r_lbl = Label( self.Frame2, text = "R squared is : " )
        self.r_lbl.grid( column=0 , row=1, padx= 20, pady= 10 )

    def load_file(self):
        filename = askopenfilename()
        self.df = pd.read_excel( filename,engine='openpyxl' )
        print ( self.df ) 

    def plot(self):
        self.tk_wid.destroy()
        figure1 = plt.Figure(figsize=(5,4), dpi=90)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.Frame2)
        self.tk_wid = bar1.get_tk_widget()
        self.tk_wid.grid( column=0 , row=0, padx= 20 )
        #sns.scatterplot( data = self.df, x = "a", y="b", ax = ax1 )
        self.df.plot(kind='scatter', x= "a", y="b",  ax=ax1)
        ax1.set_title('a vs b')

    def r_square(self):
        
        a = self.df["a"] # actual 
        b = self.df["b"] # predicted

        y_hat = np.sum( a ) / len( a )
        ss_res = np.sum( np.square( a - y_hat ) ) 
        ss_tot = np.sum( np.square( a- b ) )

        res = 1 - (ss_res/ss_tot)

        self.r_lbl["text"] = "R squared is : " + str(res)


if __name__ == "__main__":
    GUI()

