'''
Created on 26 de maig 2018

@author: oriol
'''
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import sqlite3
import sys
#from diskdb.py import dbMan
#import diskdb.diskdb
#d0bMan=g
#from diskdb import DiskDBManager.FirstInstance as dbm

#from diskdb import GetDBMan 
import diskdb

#dbm=GetDBMan()

class ddbMainWindow(QMainWindow):
    '''
    classdocs
    '''
    progress_value=0
#    sqliteconn=dbm.lconnection
#    UIWnd=dbm.Wnd
        #Noneprepdiskdb_ui.Ui_MainWindow(object)
    app=None
    def eventFilter(self, obj, event):
        return QMainWindow.eventFilter(self, obj, event)
    def __init__(self):
        '''
        Constructor
        '''
 #       QMainWindow.__init__()
        super(QMainWindow,self).__init__()
#       

    def SetProgresspc(self,value):
        self.UIWnd.progressBar.setValue(value)
        
    def tableNameChanged(self):
        ctext=self.UIWnd.comboBox_files.currentText()
        sel='PRAGMA table_info('+ctext+');'
        #"SELECT sql FROM sqlite_master WHERE name = '"+ctext+"';")
        try:
            c=self.sqliteconn.execute(sel)
            fields=c.fetchall()
            print("PRAGME table_info returns:\n",fields)
            if (fields==None or len(fields)==0):
                return
            self.UIWnd.comboBox_fields.clear()
            self.UIWnd.comboBox_fields_order.clear()
            for field in fields:
                field=field[1]
                self.UIWnd.comboBox_fields.addItem(field)
                self.UIWnd.comboBox_fields_order.addItem(field)
        except Exception as e:
            print(str(e))
        return
    def closeEvent(self, event: QCloseEvent):
        print('Close event called, bye')
#        dbMan.FirstInstance.WriteObject()
    def progressHandler(self):
   # if(QMWnd.progressbar!=None):
        #tx=QMWnd.statuslabel.text()
        #print("progressHnadler called")
        try:
            self.SetProgresspc(((self.progress_value*100)%100000))
        # implementing a custom closeEvent doesn't help me)/1000)
            self.progress_value+=1
 #       
            self.app.processEvents()
        except Exception as ex:
            print(sys.exc_info())
            print('interrupting progress_handler')
            return -1
        return 0

 #   def SetStatus(text):
     #   if(self.statuslabel!=None):
            
            
            