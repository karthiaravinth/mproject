from kivymd.uix.datatables import MDDataTable
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from kivy.uix.screenmanager import Screen
from PdfGenerator import PDFGenerator


class CollegeView(Screen):
    dt_staff = ObjectProperty(None)
    def on_pre_enter(self):
        self.pdfobj = PDFGenerator()
        if self.dt_staff is None:
            self.dt_staff = MDDataTable( size_hint = (.9,1),check =True,
                    column_data = [ ("No.", dp(15)) , ("First Name", dp(30)),("Last Name", dp(30)),("DOB", dp(17)),("Gen",dp(10)),("Staff Id", dp(19)),("Joint Date", dp(17)),("Role", dp(25)),("Retire Date",dp(17)),("Trans applyed", dp(18))   ],   #,("Edit",dp(15)),("Delete",dp(15))],
                    sorted_on = "DOB",
                    sorted_order = "DSC",
                    use_pagination = True,
                    rows_num = 9
                )
        self.dt_staff.bind(on_check_press = self.on_check_press)
        a = self.ids.title_text_id.text.partition(":")
        self.clgCode,self.clgName = a[0].strip(),a[2].strip()
        qry = 'select firstname,lastname,dob,gender,id,joinDate,role,istransfer from staffDetails WHERE collegecode = \"'+self.clgCode+'\" Order By dob'
        cursor.execute(qry)
        self.stafflist = []
        i = 1
        for dt in cursor.fetchall():
            tr =  "NO" if dt[7]==0 else "YES"
            val = (str(i),str(dt[0]),str(dt[1]),str(dt[2]),str(dt[3]),str(dt[4]),str(dt[5]),str(dt[6]),retire_cal(str(dt[2])),str(tr)) 
            self.stafflist.append(val)
            i+=1
        self.dt_staff.row_data = self.stafflist
        self.d = [("No","First Name","Last Name","DOB","Gen","Staff Id","Joint Date","Role","Retire Date")]     #pdf heading transte details not given
        # This for column checkbox delete
        self.dt_staff.header.ids.check.size  = (0,0)
        self.dt_staff.header.ids.check.opacity = 0      
        self.dt_staff.header.ids.box.padding[0] = 0
        self.dt_staff.header.ids.box.spacing = 0
        if self.dt_staff is None:
            self.ids.box_datatable_clg_id.add_widget(self.dt_staff)
            print("I am None")
        else:
            self.ids.box_datatable_clg_id.remove_widget(self.dt_staff)
            self.ids.box_datatable_clg_id.add_widget(self.dt_staff)
            print("I am not None")
    def on_check_press(self, instance_table, current_row):
        print("on_check_press = ",instance_table, current_row)  
        self.butAlignFun()
    def butAlignFun(self):
        #print('recycle_data = ',self.dt_staff.recycle_data)
        #print('total_col_headings =',self.dt_staff.total_col_headings)
        lst  = self.dt_staff.get_row_checks()
        print(lst)
        self.ids.editbut_id.disabled  = False
        self.ids.deletebut_id.disabled  = False
        if len(lst) != 1:
            self.ids.editbut_id.disabled  =True
        if len(lst) == 0:
            self.ids.deletebut_id.disabled  = True
        self.ids.deletebut_id.md_bg_color = (1,0,0,.9)
        self.ids.editbut_id.md_bg_color = (0,1,0,.9)
    def deleteRow(self):
        selectedRow = self.dt_staff.get_row_checks()
        for row in selectedRow:
            firstname,lastname,dob,gender,staffid,joinDate = row[1],row[2],row[3],row[4],row[5],row[6]
            qry = 'delete from staffDetails WHERE collegecode = \"'+self.clgCode+'\" and firstname= \"'+firstname+'\" and lastname=\"'+lastname+'\" and dob=\"'+dob+'\" and gender=\"'+gender+'\" and id=\"'+staffid+'\" and joinDate=\"'+joinDate+'\"'
            cursor.execute(qry)
            connection.commit()
        self.on_pre_enter()
        self.sncbar("Memeber Deleted Successfully")
    def editRow(self):
        row = self.dt_staff.get_row_checks()[0]
        for scr in self.manager.screens:
            if scr.name == 'facWin':
                scrobj = scr
                break
        scrobj.ids.fac_firstName_id.text = row[1]
        scrobj.ids.fac_lastName_id.text = row[2]
        scrobj.ids.fac_dob_id.text = self.dateConvert(row[3])
        scrobj.ids.fac_gender_id.text = "Male" if row[4]=='M' else "Female" if row[4]=='F' else 'Other'
        scrobj.ids.fac_staff_id.text = row[5]
        scrobj.ids.fac_joinDate_id.text = self.dateConvert(row[6])
        scrobj.ids.fac_role_id.text = row[7]
        scrobj.ids.fac_other_id.text = ''
        scrobj.ids.fac_istrans_id.text = "YES" if 1 == row[8] else "NO"
        scrobj.row = row
        scrobj.typeforedit = True
        self.manager.current = 'facWin'
    def sncbar(self,msg):
        Snackbar(text = msg).open()
        self.butAlignFun()

    def dateConvert(self,date):
        return '/'.join(reversed(date.split("-")))
    def addMembers(self):
        for scr in self.manager.screens:
            if scr.name == 'facWin':
                scrobj = scr
                break
        scrobj.ids.fac_firstName_id.text = ""
        scrobj.ids.fac_lastName_id.text = ""
        scrobj.ids.fac_dob_id.text = ''
        #scrobj.ids.fac_gender_id.text = "Male" if row[4]=='M' else "Female" if row[4]=='F' else 'Other'
        scrobj.ids.fac_staff_id.text = ''
        scrobj.ids.fac_joinDate_id.text = ''
        scrobj.ids.fac_role_id.text = ''
        scrobj.ids.fac_other_id.text = ''
        scrobj.ids.fac_istrans_id.text = "NO"
        scrobj.ids.fac_transcode_id.text = ''
        scrobj.ids.fac_transclg_id.text = ''
        self.manager.current = 'facWin'
