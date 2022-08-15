from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
def show_dialog_box(msg):
    dialog = MDDialog(text = msg) 
    dialog.open()
class MailGenerator():
    def __init__(self):
        self.frm = 'xyz@gmail.com'    # source mail id default
    def sendEmail(self,to,body):
        import smtplib
        try:
            self.ser = smtplib.SMTP('smtp.gmail.com',587)
            self.ser.starttls()
            ps = 'password'     #password
            self.ser.login(self.frm,ps)
            desc = '\r\n'.join(['To: %s'%to,'From :%s'%self.frm,'Subject:%s'%'OTP for Forget Password','',body])
            self.ser.sendmail(self.frm,to,desc)
            print("Email Working")
        except Exception as e:
            print(e)
            Snackbar(text ="Error! Need Internet Connection").open()
            return False
        else:
            Snackbar(text ="Otp Sended").open()
            return True
