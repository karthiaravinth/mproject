from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty,BooleanProperty
from PdfGenerator import PDFGenerator
from collections import defaultdict
def show_dialog_box(msg):
    dialog = MDDialog(text = msg) 
    dialog.open()

class FacultyView(Screen):
    typeforedit = BooleanProperty(False)
    row = ObjectProperty(None)
    def on_pre_enter(self):
        self.menu = MDDropdownMenu( width_mult=4,
                            items = [  {
                                "viewclass": "OneLineListItem",
                                "text": f"{i}",
                                "height": dp(56),
                                "on_release": lambda x=i: self.menu_callback(x),
                                } for i in ["Home","Back"]
                            ],
                        )
        try:
            self.clgdictName = defaultdict(lambda : "--select--")
            self.clgdictCode = defaultdict(lambda : "--select--")
            qry = "select clgName,clgCode from engineering_colleges"
            cursor.execute(qry) 
            for x in cursor.fetchall():
                self.clgdictName[x[0]] = x[1]
                self.clgdictCode[x[1]] = x[0]
        except:
            print("Error")
            self.ids.fac_transclg_id.text = '--select--'
            self.ids.fac_transcode_id.text = '--select--'
             
        self.dropMenuForTransClgName = MDDropdownMenu(caller = self.ids.fac_transclg_id,   position="center", width_mult=20,
                        items =      [    {
                            "viewclass": "OneLineListItem",
                            "text": i,
                            "height": dp(56),
                            "on_release": lambda x=i: self.set_item_for_clgName(x),
                            } for i in ['--select--']+list(self.clgdictName.keys())    
                        ]    )
        self.dropMenuForTransClgName.bind()

        self.dropMenuForTransClgCode = MDDropdownMenu(caller = self.ids.fac_transcode_id,  position="center", width_mult=20,
                        items =     [    {
                            "viewclass": "OneLineListItem", 
                            "text": i,  
                            "height": dp  (36),
                            "on_release":  lambda x=i: self.set_item_for_clgCode(x),
                                } for i in ['--select--']+list(self.clgdictCode.keys())      
                            ]     ) 
        self.dropMenuForTransClgCode.bind()

        self.ids.fac_istrans_id.text = 'NO'
        self.ids.fac_transclg_id.disabled = True
        self.ids.fac_transcode_id.disabled = True
        self.menuForGender = MDDropdownMenu(
            caller = self.ids.fac_gender_id,
            items = [    {
                        "viewclass": "OneLineListItem",
                        "text": i,
                        "height": dp(56),
                        "on_release": lambda x=i: self.set_item_gender(x),
                        } for i in ['Male','Female','Other']             
                    ],
            position="center",
            width_mult=2,
            )
        self.menuForGender.bind()
        self.menuForTransfer = MDDropdownMenu(
            caller = self.ids.fac_istrans_id,
            items = [    {
                        "viewclass": "OneLineListItem",
                        "text": i,
                        "height": dp(56),
                        "on_release": lambda x=i: self.set_item(x),
                        } for i in ['NO','YES']             
                    ],
            position="center",
            width_mult=2,
            )
        self.menuForTransfer.bind()

    def OnClickIsTransfer(self):
        self.menuForTransfer.open()
    def set_item(self, text_item):
        self.ids.fac_istrans_id.text = text_item
        if text_item.strip().upper() == "YES":
            self.ids.fac_transclg_id.disabled = False
            self.ids.fac_transcode_id.disabled = False
            self.ids.fac_transclg_id.line_color_normal = (57/255,165/255,220/255,1)
            self.ids.fac_transcode_id.line_color_normal = (57/255,165/255,220/255,1)
        else:
            self.ids.fac_transclg_id.disabled = True
            self.ids.fac_transcode_id.disabled = True
            self.ids.fac_transclg_id.text = ""
            self.ids.fac_transcode_id.text = ""
        self.menuForTransfer.dismiss()
    def OnClickGender(self):
        self.menuForGender.open()        
    def set_item_gender(self, text_item):
        self.ids.fac_gender_id.text = text_item
        self.menuForGender.dismiss() 

    # on_focus Work 2 times so adjustmant
    hlcl = BooleanProperty(True)
    hlcd = BooleanProperty(True)
    def getCollegeCode(self):
        if self.hlcd:
            self.dropMenuForTransClgCode.open()
            self.hlcd =False
        else:
            self.hlcd =True
    def set_item_for_clgCode(self, text_item):
        self.ids.fac_transcode_id.text = text_item
        self.dropMenuForTransClgCode.dismiss()    
        self.ids.fac_transclg_id.text = self.clgdictCode[text_item]

    def getCollegeName(self):
        if self.hlcl : 
            self.dropMenuForTransClgName.open()
            self.hlcl = False
        else:
            self.hlcl = True
    def set_item_for_clgName(self, text_item):
        self.ids.fac_transclg_id.text = text_item
        self.dropMenuForTransClgName.dismiss()    
        self.ids.fac_transcode_id.text = self.clgdictName[text_item]
    def collectDetails(self):
        for scr in self.manager.screens:
            if scr.name == 'loginWin':
                scrobj = scr
                break
        collegecode = scrobj.collegecode
        firstname = self.ids.fac_firstName_id.text.strip()
        lastname = self.ids.fac_lastName_id.text.strip()
        dob  = self.convertDateSql(self.ids.fac_dob_id.text.strip())
        gender = self.ids.fac_gender_id.text[0]
        empId = self.ids.fac_staff_id.text.strip().upper()
        joinDate = self.convertDateSql(self.ids.fac_joinDate_id.text.strip())
        role = self.ids.fac_role_id.text.strip()
        other = self.ids.fac_other_id.text.strip()
        istransfer = 1 if self.ids.fac_istrans_id.text.strip() == 'YES' else 0
        transclgcode = self.ids.fac_transcode_id.text.strip()
        if all([firstname,lastname,dob,gender,empId,joinDate]):
            if istransfer == 1 :
                qry = 'insert into staffDetails (id,firstname,lastname,dob,gender,joinDate,collegeCode,role,istransfer,other,transclgCode) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                values = (empId,firstname,lastname,dob,gender,joinDate,collegecode,role,istransfer,other,transclgcode)
            else:
                qry = 'insert into staffDetails (id,firstname,lastname,dob,gender,joinDate,collegeCode,role,istransfer,other) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                values = (empId,firstname,lastname,dob,gender,joinDate,collegecode,role,istransfer,other)
            try:
                if self.typeforedit:
                    print(self.row)
                    firstname,lastname,dob,gender,staffid,joinDate = self.row[1],self.row[2],self.row[3],self.row[4],self.row[5],self.row[6]
                    qryfordelete = 'delete from staffDetails WHERE collegecode = \"'+collegecode+'\" and firstname= \"'+firstname+'\" and lastname=\"'+lastname+'\" and dob=\"'+dob+'\" and gender=\"'+gender+'\" and id=\"'+staffid+'\" and joinDate=\"'+joinDate+'\"'
                    print(qryfordelete)
                    cursor.execute(qryfordelete)
                print(qry,values)
                cursor.execute(qry,values)
                connection.commit()
                if self.typeforedit:
                    Snackbar(text = "Memeber Edited").open()
                else:
                    show_dialog_box("Member Added Successfully")
                self.row = ['' for i in range(8)]
                self.typeforedit = False
                self.manager.current = "clgWin"
            except Exception as e:
                print(e)
                show_dialog_box("Check the values")
        else:
            show_dialog_box("Fill nessesary details")
        #print(cursor.fetchone())

    def convertDateSql(self,date):
        dd,mm,yy = date.split('/')
        return yy.strip()+'-'+mm.strip()+'-'+dd.strip()
    def callback(self,button):
        self.menu.caller = button
        self.menu.open()
    def menu_callback(self, text_item):
        if text_item == "Home":
            self.manager.current = 'homeWin'    #based on text_item
        elif text_item == "Back":
            self.manager.current = 'clgWin'
        self.menu.dismiss()
