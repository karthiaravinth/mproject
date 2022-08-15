from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from datetime import datetime
def show_dialog_box(msg):
    dialog = MDDialog(text = msg) 
    dialog.open()
from fpdf import FPDF,HTMLMixin
class PDF(FPDF,HTMLMixin):
    pass
class PDFGenerator():
    def __init__(self):
        self.pdf = PDF()
        self.no = 1
    # The division code for pdf
    def strdiv(self,str_arr,divl =22):
        m_str = []
        for s in str_arr:
            a = []
            c=0;
            i = len(s)
            while True:
                try:
                    if len(s[c:c+divl])<divl:
                        a.append(s[c:c+i])
                        break
                    i =s[c:c+divl].rindex(' ')
                    a.append(s[c:c+i])
                    c +=i
                except:
                    break
            m_str.append('<br>'.join(a))
        return m_str
    def createPDF(self,data,where,clg =None):
        self.pdf.add_page()
        self.pdf.set_font("Arial",size =13)
        if where == 'homeView':
            w1 = ("3%","16%","11%","11%","4%","34%","11%","11%")
            bdy = '<tbody><tr>'+'<tr/><div><tr>'.join(['<td>'+'</td><td>'.join(self.strdiv(da))+'</td>' for da in data[1:]])+'</tr></tbody>'
            self.pdf.write_html(f'''
            <head>
                <h2 align="center" style="color:red">Staff Details</h2>
            </head>
            <table border="1">
                <thead><tr>
                    <th width="3%" ><b>{data[0][0]}</b></th>
                    <th width="16%"><b>{data[0][1]}</b></th>
                    <th width="11%"><b>{data[0][2]}</b></th>
                    <th width="11%"><b>{data[0][3]}</b></th>
                    <th width="4%" ><b>{data[0][4]}</b></th>
                    <th width="34%"><b>{data[0][5]}</b></th>
                    <th width="11%"><b>{data[0][6]}</b></th>
                    <th width="11%"><b>{data[0][7]}</b></th>
                </tr></thead>'''+bdy+f''' </table><br>
                <p>  *  The Retirement Age is calculated as 60 from new amendment act <a href = "google.com">(F.No. 18(6)/98-GM)</a><br>       by Governemnt of India April,2018</p>
                <p>  *  This pdf generator based on the given data.</p>
                <p>  *  In this data the error may be possible.</p>
                <p align="right">{datetime.now()}</p>
                <br>'''  )
        else:
            w1 = ("3%","17%","12%","13%","5%","11%","13%","13%","13%")
            bdy = '<tbody><tr>'+'<tr/><div><tr>'.join(['<td>'+'</td><td>'.join(self.strdiv(da[:-1]))+'</td>' for da in data[1:]])+'</tr></tbody>'
            self.pdf.write_html(f'''
            <head>
                <h3 align="center">'''+''.join(self.strdiv([clg],35))+f'''</h3>
            </head>
            <table border="1">
                <thead><tr>
                    <th width="3%" ><b>{data[0][0]}</b></th>
                    <th width="17%"><b>{data[0][1]}</b></th>
                    <th width="12%"><b>{data[0][2]}</b></th>
                    <th width="13%"><b>{data[0][3]}</b></th>
                    <th width="5%" ><b>{data[0][4]}</b></th>
                    <th width="11%"><b>{data[0][5]}</b></th>
                    <th width="13%"><b>{data[0][6]}</b></th>
                    <th width="13%"><b>{data[0][7]}</b></th>
                    <th width="13%"><b>{data[0][8]}</b></th>
                </tr></thead>'''+bdy+f''' </table><br>
                <p>  *  The Retirement Age is calculated as 60 from new amendment act <a href = "google.com">(F.No. 18(6)/98-GM)</a><br>       by Governemnt of India April,2018</p>
                <p>  *  This pdf generator based on the given data.</p>
                <p>  *  In this data the error may be possible.</p>
                <p align="right">{datetime.now()}</p>
                <br>'''    )
        self.pdf.output("doc ("+str(self.no)+").pdf")       #generate pdf default doc.pdf
        print("pdf Downloaded")
        self.no +=1
