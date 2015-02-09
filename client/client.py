import os
import sys

python_staf_lib_path = r"c:\staf\bin"
if os.path.isdir(python_staf_lib_path):
    raise Exception("STAF path not exist: %s" % python_staf_lib_path)
    
sys.path.append(python_staf_lib_path)
import PySTAF


class Client(object):
    '''
    staf client, used to process staf message
    '''
    #staf hanle name, client will use this handle to interact with staf process
    STAFHandleName = "XSTAFClient"
    
    def __init__(self):

    
    def _get_staf_handle(self):
    
    
    def check_staf(self, staf_path):
        '''
        check if staf exist
        '''
        
    
    def register_self(self):
        '''
        register self to staf lifecycle service, then client will start when staf process start
        '''

    def start_message_process_thread(self):
        '''
        start message process thread, staf message will be processed
        '''
        
    def stop_message_process_thread(self):
        '''
        stop message process thread
        '''