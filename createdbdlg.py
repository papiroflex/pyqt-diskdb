'''
Created on 28 de maig 2018

@author: oriol
'''
from PyQt5.Qt import QDialog, QCheckBox
from prepareui.createdbdlg_ui import Ui_CreateDBDialog
import objectsave as ObjSav
#from diskdb import GetDBMan
#from diskdb import  createDiskdb

class CreatedbDlg(QDialog):
    '''
    classdocs
    '''
    dlg_ui=None #Ui_CreateDBDialog(self)
    accepted=False
    
    dir_arrel='/home/oriol'
    database_path='/home/oriol/diskdb.sqlite3.files'
    Startfrom0=True
    excludedirs=''
    includefiles=''
    
    
    
    varsread=['dir_arrel','database_path','Startfrom0','excludedirs','includefiles']
    def __init__(self):
        '''
        Constructor
        '''
        super(QDialog,self).__init__()
        
        retval=ObjSav.ObjS.ORead('createdbdlg', type(self),'createdbdlg',self.varsread)
        if(retval!=None and len(retval)==5):
            self.dir_arrel,self.database_path,self.Startfrom0,self.excludedirs,self.includefiles=retval #][0]
#       self.dir_arrel=self.dir_arrel[0]
#       self.database_path=self.database_path[0]
#       self.Startfrom0=(self.Startfrom0[0]=='True')
#      self.excludedirs=self.excludedirs[0]
#       self.includefiles=self.includefiles[0]
        
        print('Variables llegides: dir arrel ',self.dir_arrel,"db path",self.database_path,"Start bool:",str(self.Startfrom0))
        print('Exclude dirs:',self.excludedirs)
        print('include files:',self.includefiles)
    
        
        self.dlg_ui=Ui_CreateDBDialog()
        self.dlg_ui.setupUi(self)
        self.dlg_ui.lineEditexcldirs.setText(str(self.excludedirs))#"['*/anaconda3/*',*/chromiumos/*','/tmp/*','/media/oriol/*','*/android-??/*','*/linux-source*/*','*/android-studio/*','*/Android/*','*/android/*','*/eclipse/*','/.local','*/share/*','*/.config/*','/dev/*','*/pid','/sys/*','/proc/*']")
        self.dlg_ui.lineEditincfiles.setText(str(self.includefiles))#[*.xml','*.html','*.jar','*.sh','*.c','*.c??','*.py','*.java','*.tcl','*.ui']")
        self.dlg_ui.lineEditrootdir.setText(self.dir_arrel)
        self.dlg_ui.checkBox.setChecked(self.Startfrom0=='True')
        
   
    
#    def show(self):
#        super.Show()   
    def accept(self, *args, **kwargs):
        self.accepted=True
        self.dir_arrel=self.dlg_ui.lineEditrootdir.text()
#        self.database_path=self.dlg_ui.l
        self.excludedirs=self.dlg_ui.lineEditexcldirs.text()
        self.includefiles=self.dlg_ui.lineEditincfiles.text()
        self.Startfrom0=self.dlg_ui.checkBox.checkState()
        ObjSav.ObjS.OWrite( 'createdbdlg', CreatedbDlg,'createdbdlg', self.varsread, [self.dir_arrel,self.database_path,self.Startfrom0,self.excludedirs,self.includefiles])
        #self.excludedirs=self.excludedirs#.split(",")
        #self.includefiles=self.includefiles#.split(",")
        
        return QDialog.accept(self, *args, **kwargs)
    
    def reject(self, *args, **kwargs):
        return QDialog.reject(self, *args, **kwargs)
    
    
from PyQt5.QtWidgets import QApplication
import sys
#import diskdb.DiskDBManager.createDiskdb
if __name__ == '__main__':
    
    app=QApplication(sys.argv)
    
#    dlg=CreatedbDlg()
 #   dlg.showNormal()
  #  sys.exit(app.exec_())

#    GetDBMan().createDiskdb()
    
    
    print('bye')
    