from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QTextEdit,QAction,QMenu,QFileDialog,QWidget,QLabel,QMessageBox,QErrorMessage
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QRect,QSize,pyqtSignal,Qt,QThread
from PyQt5 import uic
import sys
import time
from PyQt5.QtGui import QIcon



class MyThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(int)
    def run(self):
        cnt = 0
        while cnt in range(100):
            cnt+=1
            time.sleep(0.01)
            self.change_value.emit(cnt)

class Draw(QDialog):
    def __init__(self,li):
        super(Draw, self).__init__()
        self.lis=li

        self.title = "Syntax Tree"
        self.top = 250
        self.left = 300
        self.width = 1200
        self.height = 600

        self.InitDraw(self.lis)

    def InitDraw(self,li):
    	self.setWindowIcon(QIcon("parse2.png"))
    	self.setWindowTitle(self.title)
    	self.setGeometry(self.left, self.top, self.width, self.height)
    	self.setFixedSize(self.geometry().width(),self.geometry().height())

    	self.CreateButton()
    	#self.GenerateSyntaxTree(li)
    	#self.label1=QLabel(self.lis[0],self)
    	#self.label1.setText(li[0])
    	#self.label1.move(50,50)

    def paintEvent(self,event=None):
    	x=50
    	y=50
    	self.Rectangle("read",x,y,"x")
    	self.connect("read",True,x,y)
    	x=x+150
    	self.Rectangle("if",x,y)
    	self.connect("if",False,x,y)
    	x=x-200
    	y=y+150
    	self.Elipse("op","<",x,y)
    	x=x+200
    	self.Rectangle("assign",x,y,"fact")


    def CreateButton(self):
    	CloseBtn=QPushButton("Close",self)
    	CloseBtn.setGeometry(QRect(1080,560,100,28))
    	CloseBtn.clicked.connect(self.close)
    	
    def Rectangle(self,kind,x,y,tag=None):
    	painter = QPainter(self)
    	painter.setPen(QPen(Qt.black,  3, Qt.SolidLine))
    	painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
    	painter.drawRect(x, y, 100 , 50)
    	if kind == "read":
    		painter.drawText(x+25,y+20,kind)
    		painter.drawText(x+30,y+30,"("+tag+")")
    	elif kind == "assign":
        	painter.drawText(x+25,y+20,kind)
        	painter.drawText(x+30,y+30,"("+tag+")")
    	elif kind == "write":
    		painter.drawText(x+25,y+20,kind)
    	elif kind == "repeat":
        	painter.drawText(x+25,y+20,kind)
    	elif kind == "if":
        	painter.drawText(x+25,y+20,kind)

    def Elipse(self,kind,tag,x,y):
    	painter = QPainter(self)
    	painter.setPen(QPen(Qt.black, 3,Qt.SolidLine))
    	painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
    	painter.drawEllipse(x, y, 100, 50)
    	if kind == "op":
    		painter.drawText(x+25,y+20,kind)
    		painter.drawText(x+30,y+30,"("+tag+")")
    	if kind == "const":
    		painter.drawText(x+25,y+20,kind)
    		painter.drawText(x+30,y+30,"("+tag+")")
    	if kind == "id":
    		painter.drawText(x+25,y+20,kind)
    		painter.drawText(x+30,y+30,"("+tag+")")
    def connect(self,kind,sibling,x,y,third=False):
    	painter =QPainter(self)
    	painter.setRenderHint(QPainter.Antialiasing)
    	painter.setPen(Qt.red)
    	painter.setBrush(Qt.white)
    	if kind == "read":
    		if sibling == True:
    			painter.drawLine(x+100,y+25,x+150,y+25)
    			#x=x+150
    	elif kind == "if":
    		if sibling == True:
    			painter.drawLine(x+100,y+25,x+150,y+25)
    			#x=x+150
    		painter.drawLine(x+50,y+50,x+50,y+150)
    		painter.drawLine(x+50,y+50,x-150,y+150)
    		if third == True:
    			painter.drawLine(x+50,y+50,x+150,y+150)
    	elif kind == "write":
    		if sibling == True:
    			painter.drawLine(x+100,y+25,x+150,y+25)
    		painter.drawLine(x+50,y+50,x+50,y+150)
    	elif kind == "assign":
    		if sibling == True:
    			painter.drawLine(x+100,y+25,x+150,y+25)
    		painter.drawLine(x+50,y+50,x+50,y+150)
    	elif kind == "repeat":
    		if sibling == True:
    			painter.drawLine(x+100,y+25,x+150,y+25)
    			#x=x+150
    		painter.drawLine(x+50,y+50,x+150,y+150)
    		painter.drawLine(x+50,y+50,x-150,y+150)
    	elif kind == "op":
    		painter.drawLine(x+50,y+50,x+100,y+100)
    		painter.drawLine(x+50,y+50,x-100,y+100)

 








    









 






class UI(QMainWindow):
	def __init__(self):
		super(UI,self).__init__()
		uic.loadUi("test.ui",self)
		self.InitWindow()

		

	def InitWindow(self):

		self.setFixedSize(self.geometry().width(),self.geometry().height())

		self.Filelocation.setText("")
		self.Log.setText("")
		self.progressBar.setMaximum(100)
		self.progressBar.hide()
		
		self.ExecuteBtn=self.findChild(QPushButton, 'Execute')
		self.ExecuteBtn.clicked.connect(self.ExecuteFn)
		
		self.SaveBtn=self.findChild(QPushButton,"Save")
		self.SaveBtn.clicked.connect(self.SaveFn)
		
		self.OpenBtn=self.findChild(QPushButton,"Open")
		self.OpenBtn.clicked.connect(self.OpenFn)
		
		self.ActionExecute=self.findChild(QAction,"actionExecute")
		self.ActionExecute.setShortcut("Ctrl+E")
		self.ActionExecute.triggered.connect(self.ExecuteFn)
		
		self.ActionSave=self.findChild(QAction,"actionSave")
		self.ActionSave.setShortcut("Ctrl+S")
		self.ActionSave.triggered.connect(self.SaveFn)
		
		self.ActionOpen=self.findChild(QAction,"actionOpen")
		self.ActionOpen.setShortcut("Ctrl+O")
		self.ActionOpen.triggered.connect(self.OpenFn)

		self.ActionAbout=self.findChild(QAction,"actionAbout")
		self.ActionAbout.triggered.connect(self.AboutmessageBox)
		
		self.token_index=0
		self.dum=False
		self.dum2=False
		self.dum3=False
		self.show()


	def OpenFn(self):
		self.Openfname = QFileDialog.getOpenFileName(self, 'Open file','E:/Study/College/cse2020/compilers/Parsser', "Text files (*.txt )")

		if self.Openfname[0]:
			self.Filelocation.setStyleSheet('color:red')
			self.Filelocation.setText(self.Openfname[0])
			self.Filelocation.adjustSize()
			self.file_open=open(self.Openfname[0],"r")
			self.dum=True
			self.dum2=True

	def ExecuteFn(self):
		if self.dum:	
			if self.file_open.mode == 'r':
				self.f1=self.file_open.readlines()
				if self.f1:
					self.StartParse()
				else:
					text="No Text in File!"
					self.dum=False
					self.ErrorMessage(text)
		elif self.textInput.toPlainText():
			inputText=self.textInput.toPlainText()
			self.inputLines=str(inputText).split('\n')
			self.StartParse()
		else:
			text="No Opened File or Typed Text!"
			self.ErrorMessage(text)
		#print("hello")

	def SaveFn(self):
		self.Savefname = QFileDialog.getSaveFileName(self, 'Open file','E:/Study/College/cse2020/compilers/Parsser', "Text files (*.txt )")
		self.file_name = (self.Savefname[0].split('/'))[-1]
		if self.textInput.toPlainText():
			self.file_save = open(self.Savefname[0],"w")
			self.file_save.write(self.textInput.toPlainText())
			self.file_save.close()
		else:
			text="Can't Save!"
			self.ErrorMessage(text)


	def AboutmessageBox(self):
		QMessageBox.about(self, "About Parser", "This is a simple Parser Application \nUsed to take list of Tokens and generate Syntax Tree. \n\nCreated by Omar And Kareem\n©2019")

	def StartParse(self):
		self.Filelocation.setStyleSheet('color:grey')
		if self.dum2==True:
			self.tokens=[]
			for x in self.f1:
				y="".join(x.split())
				y=str(y).split(",")
				self.tokens.append((y[0],y[1].upper()))
			self.dum2=False
			print(self.tokens)
			self.token_index = 0
			self.program()
			if self.dum3==False:
				self.thread = MyThread()
				self.thread.change_value.connect(self.setProgressVal)
				self.progressBar.show()
				self.thread.run()
				self.progressBar.hide()
				#self.OpenDrawDialog(self.f1)
		else:
			self.tokens=[]
			for line in self.inputLines:
				y="".join(line.split())
				y=str(y).split(",")
				#print(y[0]+y[1])
				self.tokens.append((y[0],y[1].upper()))
			print(self.tokens)
			self.token_index = 0
			self.program()
			if self.dum3==False:
				self.thread = MyThread()
				self.thread.change_value.connect(self.setProgressVal)
				self.progressBar.show()
				self.thread.run()
				self.progressBar.hide()
				#self.OpenDrawDialog(self.inputLines)


	def ErrorMessage(self,text):
		msg=QMessageBox()
		msg.setWindowTitle("Error")
		msg.setWindowIcon(QIcon("parse2.png"))
		msg.setIcon(QMessageBox.Critical)
		msg.setStandardButtons(QMessageBox.Ok)
		if text =="No Text in File!":
			msg.setText(text+"\nPlease choose a file with Tokens inside!")
			#msg.setInformativeText("Please choose A file with Tokens inside!")
		elif text=="No Opened File or Typed Text!":
			msg.setText(text+"\nPlease Open file or input some text!")
			#msg.setInformativeText("Please Open file first!")
		elif text=="Can't Save!":
			msg.setText(text+"\nNo text input to save! please write something!")
		else :
			msg.setText("Error!!\nCheck Log!")
			self.Log.setStyleSheet('color:orange')
			self.Log.setText(text)
		self.dum3=True
		x = msg.exec_()


	def OpenDrawDialog(self,li):
		self.Draw_Dialog = Draw(li)
		self.Draw_Dialog.setModal(True)
		self.Draw_Dialog.show()

	def setProgressVal(self, val):
		self.progressBar.setValue(val)
		if val==100:
			self.Log.setStyleSheet('color:green')
			self.Log.setText("Compiled Successfully")
			time.sleep(0.5)
	
		
			











	def Error(self,text) :
	    self.ErrorMessage(text)

	def match(self,token):
	    if token == self.tokens[self.token_index][0] or token == self.tokens[self.token_index][1] :
	        self.token_index+=1
	        if self.token_index == len(self.tokens) :
	        	self.token_index=0
	        	#print("Correct Program ^_^ ")
	        	return 

	    else :
	        self.Error("Complier Error\nToken is mis-matched at line "+str(self.token_index+1))

	    return 

	def program (self):
	    self.stmt_sequence()
	    print("Correct Program ^_^ ")
	    #return

	def stmt_sequence(self):
	    self.statement()
	    while self.tokens[self.token_index][0] == ';' :
	        self.match(';')
	        self.statement()
	    return

	def statement(self):
	    if self.tokens[self.token_index][0] == "if" :
	        self.if_stmt()

	    elif self.tokens[self.token_index][0] == "repeat" :
	        self.repeat_stmt()

	    elif self.tokens[self.token_index][1] == "IDENTIFIER" :
	        self.assign_stmt()

	    elif self.tokens[self.token_index][0] == "read" :
	        self.read_stmt()

	    elif self.tokens[self.token_index][0] == "write" :
	        self.write_stmt()

	    else :
	        self.Error("Complier Error\nToken is mis-matched at line "+str(self.token_index+1))

	    return

	def if_stmt(self) :
	    self.match("if")
	    self.exp()
	    self.match("then")
	    self.stmt_sequence()
	    if self.tokens[self.token_index][0] == "end" :
	        self.match("end")
	   
	    elif self.tokens[self.token_index][0] == "else" :
	        self.match("else")
	        self.stmt_sequence()
	        self.match("end")


	    return

	def repeat_stmt(self):
	    self.match("repeat")
	    self.stmt_sequence()
	    self.match("until")
	    self.exp()
	    return

	def assign_stmt(self) :
	    self.match("IDENTIFIER")
	    self.match(":=");
	    self.exp()
	    return

	def read_stmt(self):
	    self.match("read")
	    self.match("IDENTIFIER")
	    return

	def write_stmt(self):
	    self.match("write")
	    self.exp()
	    return

	def exp(self):
	    self.simple_exp()
	    if self.tokens[self.token_index][0] =="<"  or self.tokens[self.token_index][0] == "=" :
	        self.comparison_op()
	        self.simple_exp()

	    return 

	def comparison_op(self) :
	    if self.tokens[self.token_index][0] == "<" :
	        self.match("<")

	    elif self.tokens[self.token_index][0] == "=" :
	        self.match("=")

	    else :
	        self.Error("Complier Error\nToken is mis-matched at line "+str(self.token_index+1))

	    return

	def simple_exp(self) :
	    self.term()
	    while self.tokens[self.token_index][0] == "+"  or self.tokens[self.token_index][0] == "-" :
	        self.addop()
	        self.term()

	    return

	def addop(self) :
	    if self.tokens[self.token_index][0] == "+" :
	        self.match("+")

	    elif self.tokens[self.token_index][0] == "-" :
	        self.match("-")

	    else :
	        self.Error("Complier Error\nToken is mis-matched at line "+str(self.token_index+1))

	    return

	def term(self):
	    self.factor()
	    while self.tokens[self.token_index][0] == "*"  or self.tokens[self.token_index][0] == "/" :
	        self.mulop()
	        self.factor()

	    return

	def mulop(self):
	    if self.tokens[self.token_index][0] == "*" :
	        self.match("*")

	    elif self.tokens[self.token_index][0] == "/" :
	        self.match("/")

	    else :
	        self.Error("Complier Error\nToken is mis-matched at line "+str(self.token_index+1))

	    return

	def factor(self):
	    if self.tokens[self.token_index][0] == "(" :
	        self.match("(")
	        self.exp()
	        self.match(")")

	    elif self.tokens[self.token_index][1] == "NUMBER" :
	        self.match("NUMBER");

	    elif self.tokens[self.token_index][1] == "IDENTIFIER" :
	        self.match("IDENTIFIER")


	    else :
	        self.Error("Complier Error\nToken is mis-matched at line "+str(self.token_index+1))

	    return






if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = UI()
	app.exec_()
