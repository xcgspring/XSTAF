import os
import sys

python_staf_lib_path = r"c:\staf\bin"
if os.path.isdir(python_staf_lib_path):
    raise Exception("STAF path not exist: %s" % python_staf_lib_path)
    
sys.path.append(python_staf_lib_path)
import PySTAF
STAFHandleName = "XSTAFClient"

class Client(object):
    '''
    '''
    def __init__(self):
        self.staf_handle = PySTAF.STAFHandle(STAFHandleName)
        
    def startProcessMessage(self):
        '''
        1. Get message from staf handle message queue every 5s
        2. Do action follow the message
        3. Wait action complete
        4. Reply message to server
        '''
        
    def pauseProcessMessage(self):
        '''
        1. Kill running action
        2. pause message processing
        '''
