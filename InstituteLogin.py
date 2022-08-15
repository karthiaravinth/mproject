from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import Screen
from PdfGenerator import PDFGenerator
from collections import defaultdict
def show_dialog_box(msg):
    dialog = MDDialog(text = msg) 
    dialog.open()

class InstituteLogin(Screen):
    def on_pre_enter(self):
        self.ids.insField_drop_id.text = '--select--'
        #self.fieldlist = ['Engineering','Medical','Management','Law','Arts and Science','Agriculture','Veterinary Science']
        self.fieldlist =['Engineering','Medical','Management','Law','Agriculture','Arts & Science','Veterinary Science','Fisheries Science']
        self.dropMenuForClgField = MDDropdownMenu(caller = self.ids.insField_drop_id,
            items = [ {
                        "viewclass": "OneLineListItem",
                        "text": i,
                        "height": dp(36),
                        "on_release": lambda x=i: self.set_item_for_Field(x),
                        } for i in ['--select--']+self.fieldlist      
                    ],
            position="center",
            width_mult=50,
            )
        self.dropMenuForClgField.bind()  
        self.ids.insName_drop_id.text = '--select--'
        self.ids.insCode_drop_id.text = '--select--'
        self.ids.insType_drop_id.text = '--select--'
         
    def getFieldofInstitute(self):
        self.dropMenuForClgField.open()

    def set_item_for_Field(self, text_item):
        self.ids.insField_drop_id.text = text_item
        self.dropMenuForClgField.dismiss()
        if not text_item == 'Engineering':
            return 
        try:
            qry = "select typeName from types_of_clg"
            cursor.execute(qry) 
            typelist = []
            for x in cursor.fetchall():
                typelist.append(x[0])
        except:
            self.ids.insName_drop_id.text = '--select--'
            self.ids.insCode_drop_id.text = '--select--'
            self.ids.insType_drop_id.text = '--select--'
            return
        finally:          
            self.dropMenuForInsType = MDDropdownMenu(
                caller = self.ids.insType_drop_id,
                items = [    {
                            "viewclass": "OneLineListItem",
                            "text": i,
                            "height": dp(56),
                            "on_release": lambda x=i: self.set_item_for_TypeInstitute(x),
                            } for i in ['--select--']+typelist   
                        ],
                position="center",
                width_mult=20,
                )
            self.dropMenuForInsType.bind()

    def getTypeOfInstitute(self):
        try:
            self.dropMenuForInsType.open()
        except:
            return
    def set_item_for_TypeInstitute(self,text_item):
        self.ids.insName_drop_id.text = '--select--'
        self.ids.insCode_drop_id.text = '--select--'
        self.ids.insType_drop_id.text = '--select--'
        self.ids.insType_drop_id.text = text_item
        self.dropMenuForInsType.dismiss()
        self.clgdictName = defaultdict(lambda :"--select--")
        self.clgdictCode = defaultdict(lambda :"--select--")    
        try:
            qry1 = 'select typeIds from types_of_clg WHERE typeName = \"'+self.ids.insType_drop_id.text.strip()+'\"'
            cursor.execute(qry1)
            tyid = cursor.fetchone()
            qry = "select clgName,clgCode from "+self.ids.insField_drop_id.text.strip()+'_colleges WHERE typeId =\"'+str(tyid[0])+'\" and email is NULL'
            cursor.execute(qry) 
            for x in cursor.fetchall():
                self.clgdictName[x[0]] = x[1]
                self.clgdictCode[x[1]] = x[0]

        except Exception as e:
            self.ids.insType_drop_id.text = '--select--'
            self.ids.insName_drop_id.text = '--select--'
            self.ids.insCode_drop_id.text = '--select--'
            return  
        finally:          
            self.dropMenuForClgName = MDDropdownMenu(
                caller = self.ids.insName_drop_id,
                items = [    {
                            "viewclass": "OneLineListItem",
                            "text": i,
                            "height": dp(56),
                            "on_release": lambda x=i: self.set_item(x),
                            } for i in ['--select--']+list(self.clgdictName.keys())    
                        ],
                position="center",
                width_mult=20,
                )
            self.dropMenuForClgName.bind()
            self.dropMenuForClgCode = MDDropdownMenu(caller = self.ids.insCode_drop_id,
                items = [   {
                            "viewclass": "OneLineListItem",
                            "text": i,
                            "height": dp(36),
                            "on_release": lambda x=i: self.set_item_for_clgCode(x),
                            } for i in ['--select--']+list(self.clgdictCode.keys())      
                        ],
                position="center",
                width_mult=50,
                )
            self.dropMenuForClgCode.bind() 

    def getCollegeCode(self):
        try:
            self.dropMenuForClgCode.open()
        except:
            return
    def set_item_for_clgCode(self, text_item):
        self.ids.insCode_drop_id.text = text_item
        self.dropMenuForClgCode.dismiss()    
        self.ids.insName_drop_id.text = self.clgdictCode[text_item]
    def getCollegeName(self):
        try:
            self.dropMenuForClgName.open()
        except:
            return
    def set_item(self, text_item):
        self.ids.insName_drop_id.text = text_item
        self.dropMenuForClgName.dismiss()
        self.ids.insCode_drop_id.text = self.clgdictName[text_item]
    def mailAndPassChecker(self):
        self.email = self.ids.email_id.text.strip()
        if self.ids.email_id.text.strip()=='' or self.ids.pass_id.text.strip()=='' or self.ids.conPass_id.text.strip() == '':
            show_dialog_box("Fill Nessesary")
            return False
        if self.ids.pass_id.text.strip() == self.ids.conPass_id.text.strip():
            self.password = self.ids.pass_id.text.strip() 
            qry = 'select email from '+self.ids.insField_drop_id.text.strip()+'_colleges WHERE clgName= \"'+self.ids.insName_drop_id.text.strip()+'\" and clgCode= \"'+self.ids.insCode_drop_id.text.strip()+'\"'
            cursor.execute(qry)
            if cursor.fetchone()[0] is not None :
                show_dialog_box("Already have an Account ")
                return False
            qry = 'select email from '+self.ids.insField_drop_id.text.strip()+'_colleges'
            cursor.execute(qry)
            if self.email in [x[0] for x in cursor.fetchall()]:
                show_dialog_box("Mail ID Already Exist")
                return False
            if  self.ids.insName_drop_id.text != '--select--' and self.ids.insCode_drop_id.text != '--select--':
                qry = 'UPDATE '+self.ids.insField_drop_id.text.strip()+'_colleges SET email= \"'+self.email+'\" , password= \"'+self.password+'\" WHERE clgName= \"'+self.ids.insName_drop_id.text.strip()+'\" and clgCode= \"'+self.ids.insCode_drop_id.text.strip()+'\"'
                cursor.execute(qry)  
                connection.commit()                                    
                msg = "Account created Successfully. \nYou can login Now"
                show_dialog_box(msg)
                return True
        show_dialog_box("Error in form ")
        return False
