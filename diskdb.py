#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 00:38:19 2018

@author: oriol
"""

#module diskdb.py

import sys,traceback
from PyQt5.Qt import Qt, QTextEdit,QDialog
from PyQt5 import QtGui
#from qutebrowser.utils.log import statusbar
import diskdbMainWindow

import createdbdlg
import datetime,time
import sqlite3
import os,fnmatch,glob,re
import numpy as np
from os.path import join,getsize
import prepareui.diskdb_ui
import types
import objectsave
from pybasicori.BasicObjOri import BasicObjOri
from nltk.corpus import rte
#from debconf import db
#from debconf import db
#from debian.debtags import DB



class DiskDBManager(BasicObjOri):
 
    FirstInstance=None   
    QMWnd=None
    MAX_TEXT=65536
    MAX_COL_LENGTH=65536
    Wnd=prepareui.diskdb_ui.Ui_MainWindow()
    lconnection=None #sqlite3.connect('/home/oriol/diskdb.sqlite3')
    Runningest=False
    SelectHistory=[]
    def __init__(self,name):
        super(BasicObjOri,self).__init__()
        self.setName(name)
        self.lconnection=sqlite3.connect('/home/oriol/diskdb.sqlite3.files')
    
        rt=objectsave.ObjS.ORead('diskdb','DiskDBManager',name,['MAX_TEXT','MAX_COL_LENGTH','SelectHistory'])
        if(rt!=None):
            self.MAX_TEXT,self.MAX_COL_LENGTH,self.SelectHistory=rt
        
         
    def WriteObject(self):
#        self.sself.SelectHistory.copy()
        objectsave.ObjS.OWrite('diskdb', 'DiskDBManager', 'dbMan', ['MAX_TEXT','MAX_COL_LENGTH','SelectHistory'],[self.MAX_TEXT,self.MAX_COL_LENGTH,self.SelectHistory])
    
    def getmount(self,path):    
        return '/'
  #      path = os.path.realpath(os.path.abspath(path))
  #      while path != os.path.sep:
  #          if os.path.ismount(path):
  #              return path
#            path = os.path.abspath(os.path.join(path, os.pardir))
    def IncludeName(self,filename,includefiles):
#        if(len(filename)>self.MAX_TEXT):
#            return False
        inclist=includefiles.split() 
    #    if(type(inclist) is not 'list'):
    #        inclist=inclist.spl
        
        
 #       print(inclist[0])
        
        inclist=inclist[0].split(',')
#        print(inclist)
        
        for ext in inclist :
#            print(ext)
#            print('testing pattern for file fnmatch:',ext)
            wildfiles=fnmatch.fnmatch(filename,ext)
            if(wildfiles):
                print('Included '+ filename + ' ')
                return True
            
        return False
    def ExcludePath(self,dirname,excludedirs,IsDirectory=True):
        exclude=False
# 
        
#        if(len(dirname)>self.MAX_TEXT):
#            return True
        for exdir in excludedirs.split(',') :
#            print('excludepath for dir :'+exdir)
            rege=fnmatch.translate(exdir)
            reo=re.compile(rege)
            if(reo.match(dirname)): #or fnmatch.fnmatch(pathn+'/',exdir)):
 #               print('exclude directory for fnmatch:',dirname,' ',exdir)
                exclude=True
                print('excluded dir ',dirname+' '+exdir)
                break;
        return exclude
    def createDiskdb(self,database_path='/home/oriol/diskdb.sqlite3.files',Startfrom0=True,dir_arrel='/media/oriol',incfiles=['*'],excdirs=[]):
  
#import math
   

        self.Wnd.menuCreate_databasw.setDisabled(True)

        os.chdir(dir_arrel)
        database_path='/home/oriol/diskdb.sqlite3.files'
        if(Startfrom0 and os.path.exists(str(database_path))) :
            if(self.lconnection!=None):
                self.lconnection.close()
            os.remove(database_path)
        print()
        self.lconnection=sqlite3.connect(database_path)
        print('Created db' +database_path)
        self.lconnection.set_progress_handler(self.QMWnd.progressHandler,1000)
        self.lconnection.execute('PRAGMA synchronous = 0;')
        self.lconnection.execute('PRAGMA journal_mode = OFF;')
        self.lconnection.execute('PRAGMA cache_size= 50000;')
        c=self.lconnection.cursor()
 #   c.set_progress_handler(progressHandler)
 
        c.execute('CREATE TABLE IF NOT EXISTS dirs (dirparentid Integer,fsroot text,dirname text,mtime int,atime int,ctime int,uid int,gid int,mode int)')
        c.execute('CREATE TABLE IF NOT EXISTS files (ino int,dirid integer,filename text,type int,size int,mtime int,atime int,ctime int,uid int,gid int,mode int);')
#        c.execute('CREATE UNIQUE INDEX IF NOT EXISTS fullpath ON files (dir,filename);')
        if(excdirs==None):
            excdirs=['/tmp/*','*/android-??/*','*/linux-source*/*','*/android-studio/*','*/Android/*','*/android/*','*/eclipse/*','/.local','*/share/*','*/.config/*','/dev/*','*/pid','/sys/*','/proc/*']
#        else
#            excdirs=split(excdirs[0])
#        else:
#            excludedirs=excdirs
        print('Directories to exclude: ',excdirs)
        if (incfiles==None):
            incfiles=['*.xml','*.html','*.jar','*.sh','*.c','*.c??','*.py','*.java','*.tcl','*.ui']
#        else
#            incfiles=split(incfiles[0])
        errcount=0
        print('Files to include:',incfiles)
        valuebuff=[]
        lastcount=0
        fcount=0
        #c.execute("BEGIN")
        print('Starting to search files')
        c.execute('BEGIN')
        for root, dirs, files in os.walk(dir_arrel):
            if(self.ExcludePath(root,excdirs)):
                dirs.clear()
                print('Excluding root directory:',root)
                continue
            #if(len(str(values))>self.MAX_COL_LENGTH):
                
            dirscp=dirs
            c.execute('SELECT rowid from dirs WHERE dirname=\''+root+'\'');
            parentrowid=c.fetchone();
            if(parentrowid==None):
                print('Parent directory not found for dir '+root)
                parentrowid='0'
            else:
                parentrowid=parentrowid[0]
                
            for curdir in dirscp :
            
                
                if(self.ExcludePath(curdir,excdirs) ):
                    dirs.remove(curdir)
                    print('excluding directory:',join(root,curdir))
                    continue
                try :
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(join(root,curdir))
                    mtimefloat=mtime
                    atimefloat=atime
                    ctimefloat=ctime
                    fsroot=self.getmount(join(root,curdir))
                    values=(parentrowid,fsroot,join(root,curdir),mode,mtimefloat,atimefloat,ctimefloat,uid,gid)
                   
                    
                    c.execute('INSERT INTO dirs VALUES (?,?,?,?,?,?,?,?,?);',values)   
                    
                
                    fcount+=1
                    if((fcount%1000)==0):
                        print('commiting changes')
                        self.lconnection.execute('END')
                        self.lconnection.execute('BEGIN')
                        self.QMWnd.progressHandler()
                        
                        #self.lconnection.commit()
                    if ((fcount-lastcount) >= 10000) :
                        lastcount=fcount
                        print('Reg: ',values)
                        print(str(fcount)+' nodes processed, db size:',str(getsize(database_path)),' directory ',root,' num. errors',errcount)
                except Exception as ex:
                    print(type(ex),':', ex,file=sys.stderr)
                    print(values)
                    errcount+=1
                    
                #print ("!!!!!!!!!Error processing dir!!!!!!!!!! "+root+"/"+curdir)
  #          fcount+=1
            filesmatch=[] 
            for file in files :
                if(self.IncludeName(file,incfiles)):
                    filesmatch.append(file)
                    
            for curfile in filesmatch :

                try:
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(join(root,curfile))
                
                    fsroot=self.getmount(join(root,curfile))
                    #values=(root,curfile,'f',getsize(join(root,curfile)),os.path.getmtime(join(root,curfile)).time())
                    mtimefloat=mtime
                    atimefloat=atime
                    ctimefloat=ctime
                    values=(ino,parentrowid,curfile,mode,size,mtimefloat,atimefloat,ctimefloat,uid,gid,mode)
                    c.execute('INSERT INTO files VALUES (?,?,?,?,?,?,?,?,?,?,?);',values)
                    fcount+=1
                    if((fcount%10000)==0):
                        print('commiting changes')
                        c.execute('END')
                        c.execute('BEGIN')
                        #self.lconnection.commit()
                    if ((fcount-lastcount) >= 10000) :
                        lastcount=fcount
                        print('Reg: ',values)
                        print(str(fcount)+' nodes processed, db size:',str(getsize(database_path)),' directory ',root,' num. errors',errcount)
                except Exception as ex:
    #                if(errcount%100==0):
                    print(type(ex),':', ex,file=sys.stderr)
                    print(values,file=sys.stderr)
                    errcount+=1
                            
          

        self.lconnection.commit()
        c.execute('END')
        if ( Startfrom0 ):
            c.execute('BEGIN')
            c.execute('CREATE INDEX dirpath ON dirs(dirname);')
            c.execute('CREATE INDEX fsinode on files (fsroot,ino);')
            
            c.execute('CREATE INDEX size ON files (size);')
            c.execute('CREATE INDEX modtime ON files(mtime);')
            c.execute('CREATE INDEX ctime ON files(ctime);')
            c.execute('CREATE INDEX filenames ON files(filename);')
            c.execute("END")  
          
        c.close()
        self.Wnd.menuCreate_databasw.setDisabled(False)

        print('Finished creating database')
#   connection.close()

    def qcreateDiskDB(self):
    
        dlg=createdbdlg.CreatedbDlg()
        dlg.showNormal()
        dlg.exec_()
        if(dlg.accepted!=True):
            print("Cancelled operation")
            return
        buttonReply=QMessageBox.question(self.QMWnd, 'This can take several hours', "Do you want to create the disk database?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.createDiskdb(incfiles=dlg.includefiles,excdirs=dlg.excludedirs,Startfrom0=dlg.Startfrom0,dir_arrel=dlg.dir_arrel,database_path=dlg.database_path)
        else:
            print('No clicked.')
     
    def ExecComboStatement(self):
        selst=self.Wnd.comboBox.currentText()
        
        self.Execsqlite(selst)

    def Execsqlite(self,command):
        print('Executing select')
        try:
#            self.lconnection.execute('PRAGMA synchronous = 1;')
            #self.lconnection.set_progress_handler(None,0)
            
            csqlite3=self.lconnection.cursor()
            print('Got sqlite3 cursor')
            csqlite3.execute(command)
                   

            print('executed select')
            
            #self.lconnection.commit()
            selline='empty'
            while(True):
                selline=csqlite3.fetchone()
                if(selline==None):
                    print('no more data available')
                    break;
                print(selline)
                strappend=''
                for field in selline :
                    strappend+=str(field)+' '
                self.Wnd.selectResult.append(strappend)
                endselection=False
     #   while(not endselection):
    #        csqlite3.fetchone
        except Exception as ex:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            
            print(type(ex))
            print(ex.args)
            print(ex)
            traceback.print_exception(ex_type, ex_value, ex_traceback, limit=3)
        
        csqlite3.close()    

    def execSelectStatement(self):
    #    MainWndow.comboBoxSELECT.
        try:
            if(str(self.Wnd.execSelect)=="Stop!"):
                eststop=True
                return
            else:
                eststop=False
        except Exception as ex:
            eststop=False
        qte=QTextEdit()
        qte.toPlainText()
        Runningest=True
        SelectStatement=''
        if(self.Wnd.CheckCreateTable.isChecked()):
            self.Wnd.comboBox_files.addItem(self.Wnd.lineEdit.text())
            SelectStatement="CREATE TABLE "+self.Wnd.lineEdit.text()+" AS ";
        
        SelectStatement+='SELECT '+self.Wnd.comboBox_Distinct.currentText()+" "+str(self.Wnd.comboBox_fields.currentText())+" FROM "+self.Wnd.comboBox_files.currentText()
        if(len(str(self.Wnd.lineEdit_Where.text()))>0):
            SelectStatement+=" WHERE "+str(self.Wnd.lineEdit_Where.text())
        if(len(str(self.Wnd.comboBox_group.currentText()))):
            SelectStatement+=" GROUP BY "+self.Wnd.comboBox_group.currentText()
        if(len(str(self.Wnd.having_condition.text()))>0):
            SelectStatement+=" HAVING "+str(self.Wnd.having_condition.text())
        if(len(str(self.Wnd.comboBox_fields_order.currentText()))):
            SelectStatement+=" ORDER BY "+self.Wnd.comboBox_fields_order.currentText()
        SelectStatement+=';'
        print(SelectStatement)
        
    #    csqlite3=lconnection.cursor()
        self.Wnd.execSelect.setText("Stop!")
        self.Wnd.selectResult.setText('')
        self.SelectHistory.append(SelectStatement)
        self.Wnd.comboBox.addItem(SelectStatement)   

#        lconnection.execute('PRAGMA synchronous = 0;')
        self.Execsqlite(SelectStatement)
    #    csqlite3.close()       
        Runningest=False
        self.Wnd.execSelect.setText("Go!")
    def Analyzedb(self):
        print('calling analyze')
    #    Wnd.statusbar.curr
        #QMWnd.statuslabel.setText('Analyzing...')
        #self.lconnection.set_progress_handler(self.QMWnd.progressHandler,1000)
        csqlite3=self.lconnection.cursor()
    
        csqlite3.execute("ANALYZE;")
        print("Committing changes")
        self.lconnection.commit()
        print("closing cursor")
        csqlite3.close()
    #    self.QMWnd.statuslabel.setText("Ready!")


dbMan=DiskDBManager('dbMan')
DiskDBManager.FirstInstance=dbMan
def GetDBMan():
    return DiskDBManager.FirstInstance

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class ddbMainWindow(QMainWindow):
    '''
    classdocs
    '''
    progress_value=0
#    sqliteconn=dbm.lconnection
    UIWnd=GetDBMan().Wnd
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
        self.UIWnd.comboBox_fields.clear()
        self.UIWnd.comboBox_fields_order.clear()
            
#        ctext=self.UIWnd.comboBox_files.currentText()
        for ctext in ['files','dirs']:
            sel='PRAGMA table_info('+ctext+');'
            #"SELECT sql FROM sqlite_master WHERE name = '"+ctext+"';")
            try:
                c=self.sqliteconn.execute(sel)
                fields=c.fetchall()
                print("PRAGME table_info returns:\n",fields)
                if (fields==None or len(fields)==0):
                    return
                for field in fields:
                    field=field[1]
                    self.UIWnd.comboBox_fields.addItem(field)
                    self.UIWnd.comboBox_fields_order.addItem(field)
            except Exception as e:
                print(str(e))
        return
    def closeEvent(self, event: QCloseEvent):
        print('Close event called, bye')
        GetDBMan().WriteObject()
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
            
            
            


#import createdbdlg.CreatedbDlg
import sys
import PyQt5
import time
#import diskdbMainWindow



from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow  ,QMessageBox,\
    QLabel

if __name__ == '__main__':
  

    app =QApplication(sys.argv)
    print("App creada")
#    if(len(sys.argv)>1 and sys.argv[1]=="createdb"):
 
 #       app.exit(0)
#S        return 
 #   cddlg=CreatedbDlg(QDialog())
    
    print("QMainWindow creada")
    c=dbMan.lconnection.execute("SELECT name FROM sqlite_master WHERE type='table';")
    TableNames=[]
    for tablename in c.fetchall():
        TableNames.append(tablename)
    dbMan.QMWnd=diskdbMainWindow.ddbMainWindow()
    dbMan.Wnd.setupUi(dbMan.QMWnd)
    dbMan.QMWnd.UIWnd=dbMan.Wnd
    dbMan.QMWnd.app=app

    dbMan.QMWnd.sqliteconn=dbMan.lconnection
#
#    dbMan.qcreateDiskDB()
    
#    dbMan.QMWnd.statuslabel=QLabel(dbMan.Wnd.statusbar)
#    Wnd.statusbar.addPermanentWidget(QMWnd.statuslabel)
 #   dbMan.Wnd.comboBox_files.clear()
    for tablename in TableNames :
        tablename=tablename[0]
        dbMan.Wnd.comboBox_files.addItem(str(tablename))
#    dbM
    print('GUI Creat')
    dbMan.lconnection.set_progress_handler(dbMan.QMWnd.progressHandler,1000)
    dbMan.Wnd.comboBox_files.editTextChanged.connect(dbMan.QMWnd.tableNameChanged)
    dbMan.Wnd.comboBox_files.currentIndexChanged.connect(dbMan.QMWnd.tableNameChanged)
    dbMan.Wnd.execSelect.clicked.connect(dbMan.execSelectStatement)
    dbMan.Wnd.actionCreate_database.triggered.connect(dbMan.qcreateDiskDB)
    dbMan.Wnd.execSelect_2.clicked.connect(dbMan.ExecComboStatement)
    dbMan.Wnd.actionUpdate_database.setDisabled(True)
    dbMan.Wnd.actionAnalyze.triggered.connect(dbMan.Analyzedb)
    
    for selectsttmt in dbMan.SelectHistory:
        dbMan.Wnd.comboBox.addItem(selectsttmt)   
        
    
    print('events configurats')
    dbMan.QMWnd.showNormal()
    
    sys.exit(app.exec_())
    print('aplicació finalitzada')
    #createDiskdb()
#    print root, "consumes",
#    print sum(getsize(join(root, name)) for name in files),
#    print "bytes in", len(files), "non-directory files"
 #   if 'CVS' in dirs:
 #       dirs.remove('CVS')  # don't visit CVS directories
