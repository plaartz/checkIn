from datetime import datetime
from PIL import ImageTk,Image  
import tkinter as tk
from imutils.video import VideoStream
from pyzbar import pyzbar
from oauth2client.service_account import ServiceAccountCredentials
import argparse,imutils,time,cv2,keyboard,sys,gspread

def rgbtohex(r,g,b):
        return f'#{r:02x}{g:02x}{b:02x}'

workingdir = '/users/realtbnrlrtzy/checkIn/'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(workingdir+'csp-device-check-in-970af875e5f4.json')
gc = gspread.service_account(filename=workingdir+'csp-device-check-in-970af875e5f4.json')

class checkIn:
    def __init__(self):
        self.running = True
        self.choices = {"checkBool":None,'staffBool':None,'ID':None,'Done':False}
        self.defaultFont = 'Helvetica 16 bold'
        self.buttonFont = 'Helvetica 14 bold'
        self.defaultBg = rgbtohex(191, 14, 62)
        
        self.window = tk.Tk()
        self.window.config(cursor='none')
        self.testData = 10
        self.window.geometry('800x480')
        self.keypad = tk.Canvas(self.window,bd=0,width=300,height=480,highlightthickness=0,bg=self.defaultBg)
        self.keypad.grid(column=1,row=0)
        self.prompts = tk.Canvas(self.window,bd=0,width=500,height=480,highlightthickness=0,bg=self.defaultBg)
        self.prompts.grid(column=0,row=0)
        #self.vs = VideoStream(src=0).start()
        #self.vs = VideoStream(usePiCamera=True).start()
        print('Video stream started') 
        

    def terrapin(self):
        logo = Image.open('TPrepLogo.png').resize((300, 300), Image.ANTIALIAS)
        TLogo = ImageTk.PhotoImage(logo)
        TerrapinLogo = tk.Label(self.keypad,image=TLogo)
        TerrapinLogo.image=TLogo
        TerrapinLogo.grid(row=0,column=0)
         

    def checkQs(self):
        self.keypad = tk.Canvas(self.window,bd=0,width=300,height=480,highlightthickness=0,bg=self.defaultBg)
        self.keypad.grid(column=1,row=0)
        self.prompts = tk.Canvas(self.window,bd=0,width=500,height=480,highlightthickness=0,bg=self.defaultBg)
        self.prompts.grid(column=0,row=0)

        self.choices = {"checkBool":None,'staffBool':None,'ID':None,'Done':False}
        TopFrame = tk.LabelFrame(self.prompts,width=500,height=125,bg=self.defaultBg,highlightthickness=0,relief='flat',pady=0)
        TopFrame.grid(column=0,row=0,columnspan=2)
        CancelFrame = tk.LabelFrame(self.prompts,width=500,height=125,bg=self.defaultBg,highlightthickness=0,relief='flat',pady=0)
        CancelFrame.grid(column=0,row=3,columnspan=2)
        Cancel = tk.Button(self.prompts,text="Cancel",width=15,height=3,command=self.cancel)
        Cancel.grid(column=0,row=4)
        
        Q1 = tk.Label(self.prompts,text='Are you checking a device in or out?',bg=self.defaultBg,font=self.defaultFont)
        Q1.grid(column=0,row=1,columnspan=2)
        InQ = tk.Button(self.prompts,text='Checking In',width=25,height=7,command=lambda:[self.setVariable('checkBool',True,'prompts'),self.staffQs()])
        InQ.grid(column=0,row=2,padx=(20,0))
        OutQ = tk.Button(self.prompts,text='Checking Out',width=25,height=7,command=lambda:[self.setVariable('checkBool',False,'prompts'),self.staffQs()])
        OutQ.grid(column=1,row=2,padx=(0,20))
    

    def staffQs(self):
        TopFrame = tk.LabelFrame(self.prompts,width=500,height=125,bg=self.defaultBg,highlightthickness=0,relief='flat',pady=0)
        TopFrame.grid(column=0,row=0,columnspan=2)
        CancelFrame = tk.LabelFrame(self.prompts,width=500,height=125,bg=self.defaultBg,highlightthickness=0,relief='flat',pady=0)
        CancelFrame.grid(column=0,row=3,columnspan=2)
        Cancel = tk.Button(self.prompts,text="Cancel",width=15,height=3,command=self.cancel)
        Cancel.grid(column=0,row=4)

        Q1 = tk.Label(self.prompts,text='Are you a student or a teacher?',bg=self.defaultBg,font=self.defaultFont)
        Q1.grid(column=0,row=1,columnspan=2)
        studQ = tk.Button(self.prompts,text='Student',width=25,height=7,command=lambda:[self.setVariable('staffBool',True,'prompts'),self.createKeypad()])
        studQ.grid(column=0,row=2,padx=(20,0))
        teachQ = tk.Button(self.prompts,text='Teacher',width=25,height=7,command=lambda:[self.setVariable('staffBool',False,'prompts'),self.setVariable('ID','staff','prompts'),self.searchSheet()])
        teachQ.grid(column=1,row=2,padx=(0,20))


    def getTime(self):
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M')
        return self.date


    def keyID(self,value):
        if value == 'clear': self.keypadEnter = ''
        else: self.keypadEnter = self.keypadEnter + value
        print(self.keypadEnter)


    def setVariable(self,name,value,page): #Sets variable based on name and value
        self.choices[name] = value
        if page == 'prompts':
            for i in self.prompts.winfo_children():
                i.destroy()
        else:
            for i in self.keypad.winfo_children():
                i.destroy()
            for i in self.prompts.winfo_children():
                i.destroy()


    def cancel(self):
        self.setVariable('checkBool',None,'prompts')
        self.setVariable('staffBool',None,'prompts')
        self.setVariable('ID',None,'keypad')
        self.checkQs()


    def exitSys(self):
        self.choices['ID'] = 'quit'
        self.choices['Done'] = True
        

    def createKeypad(self):
        self.keypadEnter =''
        keypadLabelFrame = tk.Frame(self.prompts,width=500,bg=self.defaultBg)
        keypadLabelFrame.grid(column=0,row=0,columnspan=2)
        keypadLabel = tk.Label(self.prompts,text='Please enter your Student ID',bg=self.defaultBg,font=self.defaultFont,pady=185)
        keypadLabel.grid(column=0,row=1,columnspan=2)
        #CancelTopFrame = tk.LabelFrame(self.prompts,width=500,height=360,bg=self.defaultBg,highlightthickness=0,relief='flat',pady=0)
        #CancelTopFrame.grid(column=0,row=1,columnspan=2)
        CancelRightFrame = tk.LabelFrame(self.prompts,width=235,bg=self.defaultBg,highlightthickness=0,relief='flat')
        CancelRightFrame.grid(column=1,row=2)
        Cancel = tk.Button(self.prompts,text="Cancel",width=15,height=3,command=self.cancel,)
        Cancel.grid(column=0,row=2,padx=50)

        num1 = tk.Button(self.keypad,text='1',width=8,height=6,command=lambda:self.keyID('1'))
        num1.grid(column=0,row=0)
        num2 = tk.Button(self.keypad,text='2',width=8,height=6,command=lambda:self.keyID('2'))
        num2.grid(column=1,row=0)
        num3 = tk.Button(self.keypad,text='3',width=8,height=6,command=lambda:self.keyID('3'))
        num3.grid(column=2,row=0)
        num4 = tk.Button(self.keypad,text='4',width=8,height=6,command=lambda:self.keyID('4'))
        num4.grid(column=0,row=1)
        num5 = tk.Button(self.keypad,text='5',width=8,height=6,command=lambda:self.keyID('5'))
        num5.grid(column=1,row=1)
        num6 = tk.Button(self.keypad,text='6',width=8,height=6,command=lambda:self.keyID('6'))
        num6.grid(column=2,row=1)
        num7 = tk.Button(self.keypad,text='7',width=8,height=6,command=lambda:self.keyID('7'))
        num7.grid(column=0,row=2)
        num8 = tk.Button(self.keypad,text='8',width=8,height=6,command=lambda:self.keyID('8'))
        num8.grid(column=1,row=2)
        num9 = tk.Button(self.keypad,text='9',width=8,height=6,command=lambda:self.keyID('9'))
        num9.grid(column=2,row=2)
        num0 = tk.Button(self.keypad,text='0',width=8,height=6,command=lambda:self.keyID('0'))
        num0.grid(column=0,row=3)
        numE = tk.Button(self.keypad,text='Enter',width=8,height=6,command=lambda:[self.setVariable('ID',self.keypadEnter,'keypad'),self.searchSheet(),self.keyID('clear')])
        numE.grid(column=1,row=3)
        numC = tk.Button(self.keypad,text='Clear',width=8,height=6,command=lambda:self.keyID('clear'))
        numC.grid(column=2,row=3)   


    def findBarcodes(self):
        keyboard.add_hotkey('q',lambda:self.exitSys())
        print('listening')
        while True:
            
            if self.choices['ID'] == 'quit':
                self.window.destroy()
                break
            self.choices = {"checkBool":None,'staffBool':None,'ID':None,'Done':False}
            print('Searching for QR Codes')
        
            '''while True:
                self.window.update()
                frame = self.vs.read()

                frame = imutils.resize(frame,width=400)
                barcodes = pyzbar.decode(frame)
                if len(barcodes) > 0: 
                    for barcode in barcodes:
                        self.barcodeData = barcode.data.decode('utf-8')
                        print('QR Found')
                    break'''
            #self.terrapin()
            #self.window.overrideredirect(1)
            self.checkQs()
            while True:
                self.window.update()
                if self.choices['Done'] == True:
                    break
        

    def searchSheet(self):
        #   Search if device is already checked out
        #   if checkBool == False and choices['checkBool'] ==  False:
        #       can be checked Out
        #   else if checkBool == True and choices['checkBool'] == True:
        #       can be checked In
        #   else if checkBool == True and choices['checkBool'] == False:
        #       can't be checked in
        #   else if checkBool == False and choices['checkBool'] == True:
        #       cant't be checked Out
        self.wks = gc.open('test').sheet1

        self.barcodeData = 'cl3203-s04'
        

        self.sheetChoices = {'deviceID':None,'checkBool':None,'ID':None,'inDate':None,'outDate':None,'prevID':None,'row':None,'col':None}
        for iteration, row in enumerate(self.wks.get_all_values()):
            print(row)
            if row[0] == self.barcodeData:
                self.sheetChoices['checkBool'] = row[1].lower()
                self.sheetChoices['ID'] = row[2]
                self.sheetChoices['inDate'] = row[3]
                self.sheetChoices['outDate'] = row[4]
                self.sheetChoices['row'] = iteration+1
                if self.choices['checkBool'] == False and self.sheetChoices['checkBool'] == 'no': #  checking Out and is not Out
                    
                    self.checkOut()
                elif self.choices['checkBool'] == True and self.sheetChoices['checkBool'] == 'yes': # checking In and is Out
                    self.checkIn()
                elif self.choices['checkBool'] == False and self.sheetChoices['checkBool'] == 'yes': # checking out and is out
                    self.checkSuccess(False,'Already Out')
                elif self.choices['checkBool'] == True and self.sheetChoices['checkBool'] == 'no': # checking in and is in
                    self.checkSuccess(False,'Already In')


    def checkIn(self):
        if self.sheetChoices['ID'] == self.choices['ID']:
            self.wks.update_cell(self.sheetChoices['row'],2,'No')
            self.wks.update_cell(self.sheetChoices['row'],3,self.choices['ID'])
            self.wks.update_cell(self.sheetChoices['row'],4,self.getTime())
            self.checkSuccess(True,None)
        else: self.checkSuccess(False,'ID Match')


    def checkOut(self):
        self.wks.update_cell(self.sheetChoices['row'],2,'Yes')
        self.wks.update_cell(self.sheetChoices['row'],6,self.sheetChoices['ID'])
        self.wks.update_cell(self.sheetChoices['row'],3,self.choices['ID'])
        self.wks.update_cell(self.sheetChoices['row'],5,self.getTime())
        self.checkSuccess(True,None)


    def checkSuccess(self,success,error):
        
        if self.choices['checkBool'] == True:
            checkStr = 'in'
        elif self.choices['checkBool'] == False:
            checkStr = 'out'
        if success == True:
            successStr = ''
            errorMsg = ''
        elif success == False:
            successStr = ' not'
            if error == 'ID Match':
                errorMsg = 'Student ID does not match!'
            elif error == 'Already In':
                errorMsg = 'Device is not checked out!'
            elif error == 'Already Out':
                errorMsg = 'Device is checked out!'
            else: errorMsg = 'Unknown Error'

        print('Device Check %s was%s successful! %s'%(checkStr,successStr,errorMsg))
        keypadLabelFrame = tk.Frame(self.prompts,width=500,bg=self.defaultBg)
        keypadLabelFrame.grid(column=0,row=0,columnspan=2)
        
        self.setVariable('checkBool',None,'prompts')
        self.setVariable('staffBool',None,'prompts')
        self.setVariable('ID',None,'keypad')
        successText = tk.Label(self.prompts,text='Device Check %s was%s successful! %s'%(checkStr,successStr,errorMsg),bg=self.defaultBg,font=self.defaultFont)
        successText.grid(column=0,row=0,columnspan=2)
        self.window.after(4000,lambda:self.setVariable('Done',True,'done')) 


def main():
    #checkIn().searchSheet()
    checkIn().findBarcodes()
    

if __name__ == "__main__":
    main()

#*   Constant camera 
#*   Looking for barcodes
#*   If len barcodes > 0
#*   read barcode data
#   run through database
#*   is checked out (true/false)
#*   is student or teacher
#*   if student (student ID)
#*   if teacher (sub1,2,3...)
#   write to sheet
#   Rows: Device ID, Is Checked Out, Last Checked Out By, Check Out Date, Check In Date
#   
#    
# 
# TO DO:
#   git
#   
# 
# 
#