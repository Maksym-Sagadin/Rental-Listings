
'''
Sergio Chairez
Maksym Sagadin
Front End GUI for rent.py
'''

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
from os import path
import sys
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmb
import rent
import matplotlib
matplotlib.use("TkAgg")



def gui2fg():
    """Brings tkinter GUI to foreground on Mac
       Call gui2fg() after creating main window and before mainloop() start
    """
    if sys.platform == 'darwin':
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))


class MainWindow(tk.Tk):

    def __init__(self, *filenames):
        super().__init__()
        #for filename in filenae
        try:
            self.cityInfoList, self.rentArr, self.unique_cities = rent.read_data(*filenames)
            #print(self.cityInfoList)
            #print(self.rentArr[0])
        except IOError as e:
            self.withdraw()  #removes Master window
            # tkmb.showerror("Error", e)
            if path.exists(filenames[0]) == False and path.exists(filenames[1]) == False:
                tkmb.showerror("Error",f"Can't Open: {filenames}, they were not found")
            elif path.exists(filenames[0]) == False:
                tkmb.showerror("Error",f"Can't Open: {filenames[0]}, it was not found")
            else: #path.exists(filenames[1]) == False:
                tkmb.showerror("Error",f"Can't Open: {filenames[1]}, it was not found")
            
            raise SystemExit(e) #or we can do return?

        # If either of the file open is not successful, a messagebox window will show up to let the user know that there is a file open error, with the specific file name.
        self.meanMonthlyCityRatesArr = rent.mean_rental_price(
            self.cityInfoList, self.rentArr, self.unique_cities)

        self.title('Rental Prices')
        self.geometry("500x200")
        self.container = tk.Frame(self)

        # weight = 0 means their size is fixed
        # weight = 1 means it takes up as much room as it needs to
        # makes changes to the grid rows/cols
        # weights make that col/row more of a priority when expanding the window
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.rowconfigure(0, weight=0)
        self.container.rowconfigure(1, weight=1)
        self.container.rowconfigure(2, weight=0)
        label = tk.Label(background='blue',
                         text="Rent Data for Santa Clara County",
                         fg='white',
                         font=('Helvetica', 28))

        label.grid(
            row=0, column=0,
            sticky='ew',
            padx=10, pady=10
        )
        label2 = tk.Label(
            text="This application gives you info on rental prices for a \n 2-bedroom place in Santa Clara County",
            font=('Helvetica', 16)
        )

        label2.grid(
            row=1, column=0,
            sticky='ew',

        )
        self.rental_price_option_buttons()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        '''
        This function opens a message box asking if the user wants to quit
        Then quits out of the program if the user clicks yes
        '''
        if tkmb.askyesno("Exit", "Do you want to quit the application?"):
            self.quit()

    def rental_price_option_buttons(self):
        '''
        This function creates the buttons for the Main Window
        '''
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(
            row=2, column=0, sticky='nsew', padx=10, pady=10)
        #buttons_frame.config(bg='blue')
        buttons_frame.columnconfigure(0, weight=0)
        buttons_frame.columnconfigure(1, weight=0)
        buttons_frame.columnconfigure(2, weight=0)

        self.rental_trend_button = tk.Button(
            buttons_frame, text='Rental Price Trend',
            command=self._rental_price_trends)
        self.rental_trend_button.grid(
            row=2, column=0, sticky='ew', padx=15, pady=10)

        self.current_rental_prices_button = tk.Button(
            buttons_frame, text='Current Rental Prices', command=self._current_rental_prices)

        self.current_rental_prices_button.grid(
            row=2, column=1, sticky='ew', padx=15, pady=10)

        self.but_about = tk.Button(buttons_frame, text="About",
                                   command=self._about_info)
        self.but_about.grid(
            row=2, column=2, sticky='ew', padx=15, pady=10)

    #button1 logic
    def _rental_price_trends(self):
        dialogWin = DialogWindow(self,
                                 self.meanMonthlyCityRatesArr, self.cityInfoList, 
                                 self.unique_cities,rent.plot_rental_price_trend)
        dialogWin.grab_set()  #do this in DialogWindow() class
        dialogWin.focus_set() #do this in DialogWindow() class

    # button2 logic
    def _current_rental_prices(self):
        PlotWindow(self.rentArr, self.cityInfoList, plotopt="current_rental_prices")

    # button3 logic
    def _about_info(self):
        credits = "Credits:\nSergio Chairez\nMaksym Sagadin"
        tkmb.showinfo("Credits", credits)


class DialogWindow(tk.Toplevel):
    def __init__(self, master, meanMonthlyCityRatesArr, cityInfoList, unique_cities,
                 plot_rental_price_trend):
        super().__init__(master)
        self.meanMonthlyCityRatesArr = meanMonthlyCityRatesArr
        self.cityInfoList = cityInfoList
        self.unique_cities = unique_cities
        self.plot = plot_rental_price_trend
        self.title('Choose a City')
        self.geometry("200x300")
        if 'All' not in unique_cities:
            unique_cities.append('All')

        self.options_frame = tk.Frame(self)
        self.options_frame.grid(
            row=10, column=0, sticky='nsew', padx=30, pady=30)


        self.cityChoice = tk.StringVar()
        #default to SJ
        self.cityChoice.set('San Jose')
        for val in unique_cities:
            tk.Radiobutton(self.options_frame,
                           text=val,
                           padx=20,
                           variable=self.cityChoice,
                           value=val).pack(anchor=tk.W)

        self.saveButton = tk.Button(self, text='SAVE',
                                    command=self.display_rental_price_trend).grid()

        self.grab_set()
        self.focus_set()

    def display_rental_price_trend(self):
        ''' Prints which city was selected and initializes the Plot Window Class '''
        citySelected = self.cityChoice.get()
        print(citySelected)  
        self.destroy()

        PlotWindow(self.meanMonthlyCityRatesArr, self.cityInfoList,self.unique_cities,citySelected, plotopt="plot_rental_price_trend")


class PlotWindow(tk.Toplevel):
    def __init__(self, *args, plotopt=None):
        super().__init__()

        self.fig = plt.figure(figsize=(14, 5), dpi=100)
        if plotopt == "plot_rental_price_trend":
            self._rental_price_plot(*args)
        elif plotopt == "current_rental_prices":
            self._current_price_plot(*args)  

    def _rental_price_plot(self, *args):
        '''This function plots the rental price for the city selected'''
        
        self.focus_set()
        self.title(f"Rental Price Trend for {args[3]}")
        self.plot1 = rent.plot_rental_price_trend
        self.plot1(*args)

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()

    def _current_price_plot(self, *args):
        '''This function plots the current rental prices for all the cities'''
        self.grab_set()
        self.focus_set()
        self.plot2 = rent.bar_graph_zip
        self.plot2(*args)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()


if __name__ == '__main__':

    filenames = ['zipCity.csv', 'rent.csv']
    run = MainWindow(*filenames)
    gui2fg()
    run.mainloop()

