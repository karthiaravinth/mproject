from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from PdfGenerator import PDFGenerator

class HomeScreen(Screen):
    dt_staff = ObjectProperty(None)
    def filter_method(self, text="", search=False):
        if text == "":
            self.on_pre_enter()
            return
        if self.ids.filter_opt_id.text == "All":
            qry = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode where staffDetails.firstname like \"%'+text+'%\" or staffDetails.lastname like \"%'+text+'%\" or staffDetails.dob like \"%'+text+'%\" or staffDetails.gender like \"%'+text+'%\" or engineering_colleges.clgName like \"%'+text+'%\" or staffDetails.role like \"%'+text+'%\" Order By dob'
        elif self.ids.filter_opt_id.text == "First Name":
            qry  = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode where staffDetails.firstname like \"%'+text+'%\" Order By dob'
        elif self.ids.filter_opt_id.text == " Last Name":
            qry  = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode where staffDetails.lastname like \"%'+text+'%\" Order By dob'
        elif self.ids.filter_opt_id.text == "DOB":
            qry  = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode where staffDetails.dob like \"%'+text+'%\" Order By dob'
        elif self.ids.filter_opt_id.text == "Sex":
            qry  = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode where staffDetails.gender like \"%'+text+'%\" Order By dob'           
        elif self.ids.filter_opt_id.text == "Role":
            qry  = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode where staffDetails.role like \"%'+text+'%\" Order By dob' 
        elif self.ids.filter_opt_id.text == "College Name":
            qry  = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode where engineering_colleges.clgName like \"%'+text+'%\" Order By dob' 
        elif self.ids.filter_opt_id.text == "Retire Date":
            self.extstafflist = []
            i =1
            for val in self.stafflist:
                if text in val[-1]:
                    self.extstafflist.append((str(i),)+val[1:])
                    i+=1
            self.dt_staff.row_data = self.extstafflist
            if self.dt_staff is None :
                self.ids.rv.add_widget(self.dt_staff)
            else:
                self.ids.rv.remove_widget(self.dt_staff)
                self.ids.rv.add_widget(self.dt_staff) 
            return
        else:
            qry = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode where staffDetails.firstname like \"%'+text+'%\" or staffDetails.lastname like \"%'+text+'%\" or staffDetails.dob like \"%'+text+'%\" or staffDetails.gender like \"%'+text+'%\" or engineering_colleges.clgName like \"%'+text+'%\" or staffDetails.role like \"%'+text+'%\" Order By dob' # This also All

        cursor.execute(qry)
        self.extstafflist = []
        i = 1
        for dt in cursor.fetchall():
            rt =retire_cal(str(dt[2]))
            val = (str(i),str(dt[0]),str(dt[1]),str(dt[2]),str(dt[3]),str(dt[4]),str(dt[5]),rt)
            self.extstafflist.append(val)
            i+=1
        self.dt_staff.row_data = self.extstafflist
        if self.dt_staff is None :
            self.ids.rv.add_widget(self.dt_staff)
        else:
            self.ids.rv.remove_widget(self.dt_staff)
            self.ids.rv.add_widget(self.dt_staff) 

    def callback(self,button):
        self.menu.caller = button
        self.menu.open()
    def menu_callback(self, text_item):
        self.manager.current = 'loginWin'    #based on text_item
        self.menu.dismiss()
    def filter_opt_open(self):
        self.filter_option.open()
    def filter_opt_fun(self,text):
        self.ids.search_field.hint_text ="Filter" if text=="All" else "Filter by "+text
        self.ids.filter_opt_id.text = text
        self.filter_option.dismiss()
    def on_pre_enter(self):
        self.pdfobj = PDFGenerator()  #pdf class
        self.menu = MDDropdownMenu( width_mult=4,
                                    items = [  {
                                        "viewclass": "OneLineListItem",
                                        "text": f"{i}",
                                        "height": dp(56),
                                        "on_release": lambda x=i: self.menu_callback(x),
                                        } for i in ["Institute Login","Governemnt Login"]
                                    ],
                                )
        self.filter_option = MDDropdownMenu( width_mult=4,
                                    items = [  {
                                        "viewclass": "OneLineListItem",
                                        "text": f"{i}",
                                        "height": dp(46),
                                        "on_release": lambda x=i: self.filter_opt_fun(x),
                                        } for i in ["All","First Name","Last Name","DOB","Sex","College Name","Role","Retire Date"]
                                    ],
                                    caller = self.ids.filter_opt_id,
                                )
        if self.dt_staff is None:
            self.dt_staff = MDDataTable( 
                    #column_data = [ ("No.", dp(10)) , ("First Name", dp(30)),("Last Name", dp(30)),("DOB", dp(17)),("Gen",dp(10)),("Staff Id", dp(19)),("College Code",dp(20)),("College Name",dp(60)),("Joint Date", dp(17)),("Role", dp(25)),("Trans applyed", dp(18)) ],
                    column_data = [ ("No.", dp(10)) , ("First Name", dp(30)),("Last Name", dp(30)),("DOB", dp(20)),("Gen",dp(11)),("College Name",dp(70)),("Role", dp(25)),("Retire Date", dp(30)) ],
                    use_pagination = True,
                    pagination_menu_pos = "center",
                    rows_num = 10                   )
        #qry = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,staffDetails.id,staffDetails.collegecode,engineering_colleges.clgName,staffDetails.joinDate,staffDetails.role,staffDetails.istransfer from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode Order By dob'
        qry = 'select staffDetails.firstname,staffDetails.lastname,staffDetails.dob,staffDetails.gender,engineering_colleges.clgName,staffDetails.role from staffDetails Inner Join engineering_colleges on staffDetails.collegecode = engineering_colleges.clgCode Order By dob'
        cursor.execute(qry)
        self.stafflist = []
        self.d = [("No","First Name","Last Name","DOB","Sex","College Name","Role","Retire Date")]
        i = 1
        for dt in cursor.fetchall():
            #tr =  "NO" if dt[9]==0 else "YES"
            #val = (i,dt[0],dt[1],str(dt[2]),dt[3],dt[4],dt[5],dt[6],str(dt[7]),dt[8],tr) 
            rt =retire_cal(str(dt[2]))
            val = (str(i),str(dt[0]),str(dt[1]),str(dt[2]),str(dt[3]),str(dt[4]),str(dt[5]),rt)
            self.stafflist.append(val)
            i+=1
        self.dt_staff.row_data = self.stafflist
        if self.dt_staff is None :
            self.ids.rv.add_widget(self.dt_staff)
        else:
            self.ids.rv.remove_widget(self.dt_staff)
            self.ids.rv.add_widget(self.dt_staff)        
