
from kivy.uix.screenmanager import Screen

class LoginPage(Screen):
    def on_pre_enter(self):
        self.ids.email_or_code_id.text = ""
        self.ids.passcheck_id.text = ""
    def checkPassword(self):
        emailorcode = self.ids.email_or_code_id.text.strip()
        password = self.ids.passcheck_id.text.strip()
        pas = None
        if emailorcode =='' or  password=='':
            return
        # now only engineering
        try :
            qry = 'select password,clgName,clgCode from engineering_colleges WHERE email =\"'+emailorcode+'\"'
            cursor.execute(qry)
            pas,self.collegename,self.collegecode = map(str,cursor.fetchone())
        except:
            try:
                qry = 'select password,clgName,clgCode from engineering_colleges WHERE clgCode =\"'+emailorcode+'\"'
                cursor.execute(qry)
                pas,self.collegename,self.collegecode = map(str,cursor.fetchone())
            except:
                print("not valid email & password")

        if pas is not None and pas == password:
            for scr in self.manager.screens:
                if scr.name == 'clgWin':
                    scrobj = scr
                    break
            scrobj.ids.title_text_id.text = self.collegecode+" : " +self.collegename
            self.manager.current = 'clgWin'
