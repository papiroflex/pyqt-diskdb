'''
Created on 1 de juny 2018

@author: oriol
'''
import sqlite3,inspect,sys,traceback
#from numba.typing.builtins import IndexValue
import numpy as np
#from np import ndim

import types
class ObjectSaver(object):
    '''
    classdocs
    '''
    oscon=sqlite3.connect('/home/oriol/objectsave.sqlite3.db')
    dbfile=None
    def __init__(self):
        '''
        Constructor
        '''
        print('initialyzing objectsave')
        #oscon=sqlite3.connect('/home/oriol/objectsave.mysql3.db')
        
        self.oscon.execute('CREATE TABLE IF NOT EXISTS savedvars(module text,type text,object text,varname text,value text);')
        self.oscon.execute('CREATE UNIQUE INDEX IF NOT EXISTS objectsidx ON savedvars (module,object,varname);')
        self.oscon.commit()
        print('ObjectSaver end __init__')
    backslashing="\'\[\]\{\}\(\)\"\,"
    def RemoveCometesiParentesis(self,value):
        ret=value
        
        
        ret=ret.replace('\'','')
        ret=ret.replace('\"','')
        ret=ret.replace('(','')
        ret=ret.replace(')','')
        ret=ret.replace('[','')
        ret=ret.replace(']','')
        return ret
    def RemoveBackslashes(self,value):
        ret=str(value).replace('\\', '')
        print('no backslash',ret)
        return  ret
    def AddBackslashes(self,value):
        ret=str(value)
        for charesc in self.backslashing :
            #idx=ret.index(charesc)
            ret.replace(charesc, '\\'+charesc)
        print('backslashes added'+ret)
        return ret
    def VarTosqlField(self,varvalue,type):
        if(type=='bool'):
            if(varvalue==True):
                ret='True'
            else:
                ret='False'
        elif(type=='list' or type=='tuple' or type=='unknown') :
            ret=self.AddBackslashes(str(varvalue))
        elif(type=='int' or type=='float'):
            ret=str(varvalue)
        else:
            ret=str(varvalue)
            
            
            
                    
        
        
        print('varvalue:'+ret+'type: '+type)
        return ret
            
    def sqlFieldToVar(self,selrow,type):
        
        if(type in ['list','tuple']):
            ret=self.RemoveBackslashes(selrow)
            ret=self.RemoveCometesiParentesis(ret)
            ret=ret.split(',')
        elif (type=='bool'):
            ret=(selrow=='True')
        elif (type=='float'):
            ret=float(selrow)
        elif (type=='int'):
            ret=int(selrow)
        elif (type=='string'):
            ret=selrow
        else:
            ret=str(selrow)
   #     ret=eval(ret)
        print('variable gotten'+str(ret)+"type:"+type)
        return ret    
    def ORead(self,module,type,objname,varnames):
        val=[]
        try:
            for varn in varnames :
                c=self.oscon.execute("SELECT value,type FROM savedvars WHERE module=? AND object=? AND varname=?;"
                                     ,[str(module),str(objname),str(varn)])
                self.oscon.commit()
                ret=c.fetchone()
                
                if(ret!=None):
                    type=ret[1]
                    subl=self.sqlFieldToVar(ret[0],type)
                    val.append(subl)
                else:
                    break;
  #                  val.append('')
                    
        except Exception as ex:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            print('Error!!!!!',ex_type,' ',ex_value,file=sys.stderr)
            print(ex_traceback,file=sys.stderr)
            print(traceback.extract_tb(ex_traceback),file=sys.stderr)
            traceback.print_exception(ex_type, ex_value, ex_traceback,
                              limit=5, file=sys.stderr)
        if(len(val)==0):
            return None   

        return val  
    def islistortuple(self,var):
        return var.ndim>1
    def OWrite(self,module,type,objname,varnames,values):
        i=0
        try :
            for varname in varnames :
                #c=
                self.oscon.execute("DELETE FROM savedvars WHERE module=? AND object=? AND varname=? ;"
                                     ,[module,objname,varname])
                value=values[i]
#                vtype=type(value)
                #vtype='str'
                if (isinstance(value,(tuple))):
                    type='tuple'
                elif(isinstance(value,(list))):
                    type='list'
                elif(isinstance(value,(str)))   :
                    type='string'
                elif(isinstance(value,(int))):
                    type='int'
                elif(isinstance(value,(float))):
                    type='float'
                elif(isinstance(value,(bool))):
                    type='bool'
                else:
                    type='unknown'
                i+=1
                #reg=c.fetchone()
#                value=[value]
               
                
                if(True):
                    c=self.oscon.execute("INSERT INTO savedvars (module,type,object,varname,value) VALUES (?,?,?,?,?); "
                                             ,[module,type,objname,varname,self.VarTosqlField(value,type) ] )
                else:
                    c=self.oscon.execute("UPDATE TABLE savedvars SET value=? WHERE module=? AND object=? AND varname=?;"
                                             ,[self.VarTosqlField(value,type),module,objname,varname])
                c.close()
        except Exception as ex:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            print('Error!!!!!',ex_type,' ',ex_value,file=sys.stderr)
            print(ex_traceback,file=sys.stderr)
            print(traceback.extract_tb(ex_traceback),file=sys.stderr)
            traceback.print_exception(ex_type, ex_value, ex_traceback,
                              limit=5, file=sys.stderr)
            
        self.oscon.commit()
#    def ReadMembers(self,module,classtype,object):
#        for varname in inspect.getmembers(type,inspect.isvariable)
#            c=self.oscon.execute("SELECT varname,value FROM savedvars WHERE module=? AND type=?;",varname,module,type,objname)
#        for vn,vv in c.fetchone()
            
#        return None#str(mval[0])


ObjS=ObjectSaver()