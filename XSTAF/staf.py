
import os
import sys
#import custom logger

class STAF(object):
    '''
    use this class to configure and control STAF process
    functions "check_staf", "connect_staf", "configure_staf" need run first before use other functions
    '''
    def __init__(self, staf_dir):
        self.staf_dir = staf_dir
        self.staf_starter = "startSTAFProc.bat"
        self.staf_handle_name = "XSTAF_client"
        #staf id, 0 is an invalid id
        self.staf_handle_id = 0
        self.staf_handle = None
        
        self.client_daemon = ""

    def check_staf(self):
        '''
        check if staf exist
        if exist
            return
        if not exist
            prompt a dialog warn user
            return
        '''
        self.abs_staf_starter = os.path.join(self.staf_dir, self.staf_starter)
        if not os.path.isfile(self.abs_staf_starter):
            print("STAF starter not exist: %s" % self.abs_staf_starter)
            return False
            
        return True
        
    def connect_staf(self):
        '''
        check if local staf process start
        if not
            start staf process
            
        create a staf handle to connect to staf process
        '''
        #check if staf process start
        python_staf_lib_path = os.path.join(self.staf_dir, "bin")
        sys.path.append(python_staf_lib_path)
        try:
            import PySTAF
        except ImportError:
            print("Cannot import PySTAF")
            return False
            
        try:
            self.staf_handle = PySTAF.STAFHandle(self.staf_handle_name)
        except PySTAF.STAFException, e:
            if e.rc == 21:
                #error value 21 indicate STAF not running
                print("Error code 21, STAF not running, please start it and try again")
            else:
                print("Error registering with STAF, RC: %d" % e.rc)
            return False
            
        #get handle id here
        self.staf_handle_id = self.staf_handle.handle
        return True
        
    def configure_staf(self):
        '''
        need to configure staf before run test
        '''
        #add more configures here
        
        return True
        
        
    ########################################
    #
    # Queue Service
    #
    ########################################

    def add_message(self, message):
        '''
        Add message to handle message queue
        '''
        
        
    def get_message(self, message):
        '''
        retrieve and removes message form handle message queue
        '''
        
        
    def peek_message(self, message):
        '''
        retrieve message form handle message queue
        '''
        
        
    def delete_message(self, message):
        '''
        delete message form handle message queue
        '''
        
    def list_message(self, message):
        '''
        retrieve the entire contents from handle message queue
        '''
        
    ########################################
    #
    # Process Service
    #
    ########################################
        
    def start_process(self, DUT, process):
        '''
        start a process
        '''
        
    def stop_process(self, DUT, process):
        '''
        stop a process
        '''