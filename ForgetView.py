from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextFieldRect
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from PdfGenerator import PDFGenerator
from kivymd.uix.snackbar import Snackbar
def show_dialog_box(msg):
    dialog = MDDialog(text = msg) 
    dialog.open()

class ForgetView(Screen):
    import random
    txt1 = ObjectProperty(None)
    txt2 = ObjectProperty(None)
    def on_pre_enter(self):
        self.mail_obj = MailGenerator()
        self.ids.email_id.text = ""
        self.ids.email_id.disabled = False
        self.ids.otp_id.text =  ""
        self.ids.otp_id.disabled = True
        self.ids.but_id.text = 'Send OTP'  
        self.ids.but_id.md_bg_color = (1,0,0,1)  
        if self.txt1 is not None and self.txt2 is not None:
            self.ids.boxlay1inforget_id.remove_widget(self.txt1)
            self.ids.boxlay1inforget_id.remove_widget(self.txt2)
    def sendOTP(self):
        try:
            if self.ids.email_id.text.strip() == '':
                raise
            qry = "select clgName,clgCode,email,password from engineering_colleges WHERE email =\""+self.ids.email_id.text.strip()+'\"'
            cursor.execute(qry) 
            c = cursor.fetchone()
            clgName,clgCode,email,password = c[0], c[1], c[2], c[3]
            self.otp =self.random.randint(1000,9999)
            print(self.otp)
            to = [email]#['aravintharasai5@gmail.com','vishnukumarnatarajan01@gmail.com']
            body = '''
                Don\'t Share the OTP to anyone...\n
                OTP : '''+str(self.otp)+'''
                \nThis OTP available for 5 mins only.\n\n

                \t\tThank You
            '''
            
            if self.mail_obj.sendEmail(to,body): 
            #if True :
                self.ids.otp_id.disabled = False
                self.ids.but_id.text = 'Submit'  
                self.ids.but_id.md_bg_color = (0,0,1,1)
                self.ids.email_id.disabled = True
        except Exception as e:
            print(e)
            Snackbar(text ="Mail ID not Exist").open()
    threetime = 3
    def checkOtp(self):
        if self.threetime == 0:
            self.ids.otp_id.text = ""
            self.ids.otp_id.disabled = True
            self.ids.but_id.text = 'Resend OTP'  
            self.ids.but_id.md_bg_color = (1,0,0,1)
            self.threetime = 3
            Snackbar(text ="Chance Over.Try to Resend OTP").open()
            return
        try:
            if self.otp == int(self.ids.otp_id.text.strip()):
                print("otp match")
                self.ids.otp_id.disabled = True
                self.ids.but_id.text = 'Save Password'  
                self.ids.but_id.md_bg_color = (0,1,0,1)
                self.txt1 = MDTextFieldRect(multiline =False,padding=5,height=25,hint_text = "New Password",width =175, font_size =20,pos_hint ={"center_x":.5},password =True)
                self.txt2 = MDTextFieldRect(multiline= False,padding=5,height=25,hint_text = "Confirm Password",width =175, font_size =20,pos_hint ={"center_x":.5},password =True)
                self.ids.boxlay1inforget_id.add_widget(self.txt1)
                self.ids.boxlay1inforget_id.add_widget(self.txt2)
                #self.ids.but_id.bind(on_press=lambda x :self.setpassword(txt1.text,txt2.text))  
            else:
                Snackbar(text ="Wrong OTP").open()
            self.threetime -= 1
        except Exception as e:
            print(e)
            Snackbar(text ="Wrong OTP").open()
            self.threetime -= 1
    def setpassword(self):
        password = self.txt1.text.strip()
        con_pass = self.txt2.text.strip()
        if password=='' or con_pass == '':
            show_dialog_box("Should not be Empty")
        elif password== con_pass:
            qry = 'UPDATE engineering_colleges SET password= \"'+password+'\" WHERE email= \"'+self.ids.email_id.text.strip()+'\"'
            cursor.execute(qry)  
            connection.commit()                                    
            msg = "Password Changed Successfully\nYou can login Now"
            show_dialog_box(msg)
            self.manager.current = 'loginWin'
        else:
            show_dialog_box("Password Should be same")
    def forgetMail(self):
        show_dialog_box("Sorry you cant\'t change the Email here..\nYou Should send the mail for that issue to this\nMail ID : "+self.mail_obj.frm)
