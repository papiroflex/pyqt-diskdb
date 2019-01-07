'''
Created on 25 de maig 2018

@author: oriol
'''
import PyQt5.uic
dir_arrel='/home/oriol'

if __name__ == '__main__':
#   PyQt5.uic.uiparser.
#   pass
    PyQt5.uic.compileUi('diskdb.ui', open('diskdb_ui.py','w'), execute=False,from_imports=True)
    PyQt5.uic.compileUi('createdbdlg.ui',open('createdbdlg_ui.py','w'),execute=False,from_imports=True)
        