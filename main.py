from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty,StringProperty,BooleanProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton,MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from datetime import date,datetime,timedelta

from HomeScreen import HomeScreen
from LoginPage import LoginPage
from InstituteLogin import InstituteLogin
from CollegeView import CollegeView
from ForgetView import ForgetView
from FacultyView import FacultyView
Window.size = (1000,650)

import mysql.connector
try:
    import sqlite3
    connection = sqlite3.connect("ha22DB.db")    # Database
    if connection:
        cursor = connection.cursor()
        qry =   ''' create table if not exists staffDetails(
                id varchar(8) not null,             firstname varchar(15),
                lastname varchar(15),               dob date,
                gender char(1),                     joinDate date,                  
                collegeCode varchar(8) not null,    role varchar(20),               
                istransfer bool,                    other text, 
                transclgCode varchar(8) default null,primary key(id),
                FOREIGN KEY (collegeCode) REFERENCES engineering_colleges(clgCode),
                FOREIGN KEY (transclgCode) REFERENCES engineering_colleges(clgCode)
             )  '''
        cursor.execute (qry)  

except Exception as e:
    print(e)
    print("Error While connecting")

def show_dialog_box(msg):
    dialog = MDDialog(text = msg) 
    dialog.open()

def retire_cal(dat):
    t1 = list(map(int,dat.split('-')))
    try:
        if t1[1]<10: 
            return str(date.fromisoformat(str(t1[0]+retire_age)+'-0'+str(t1[1])+'-01') - timedelta(days =1))
        return str(date.fromisoformat(str(t1[0]+retire_age)+'-'+str(t1[1])+'-01') - timedelta(days =1))
    except:
        pass
class main(MDApp):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Builder.load_file()     # To Load Kivy File
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name = 'homeWin'))
        self.sm.add_widget(LoginPage(name = 'loginWin'))
        self.sm.add_widget(InstituteLogin(name = 'instituteWin'))
        self.sm.add_widget(CollegeView(name = 'clgWin'))
        self.sm.add_widget(ForgetView(name = 'forgetWin'))
        self.sm.add_widget(FacultyView(name = 'facWin'))
    def build(self):
        return self.sm
retire_age = 60   # As per new Amendment (58 to 60)       
main().run()

#if connection.is_connected():
if connection:
    cursor.close()
    connection.close()
    print("mysql closed")
