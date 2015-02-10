
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
            
        return True
        
    def configure_staf(self):
        '''
        need to configure staf before run test
        '''
        #set trust level
        #set trust level to 3 for default, so other staf server can queue message to local
        result = self.staf_handle.submit("local", "trust", "set default level 3")
        if (result.rc != 0):
            print("Set trust level fail, RC: %d, Result: %s" % (result.rc, result.result))
            return False
            
        #register self to staf's life cycle service
        #so every time staf process start, client is started
        result = self.staf_handle.submit("local", "lifecycle", 'REGISTER PHASE Startup MACHINE local SERVICE Process REQUEST "START COMMAND %s" DESCRIPTION "Start XSTAF client daemon"' % self.client_daemon)
        if (result.rc != 0):
            print("Register XSTAF client daemon fail, RC: %d, Result: %s" % (result.rc, result.result))
            return False
        
        #add more configures here
        
        return True
        
    def queue_message(self, message):
        '''
        '''
        
        
    def get_message(self, message):
        '''
        '''
        
        
    def peek_message(self, message):
        '''
        '''
        
    def delete_message(self,message):
        '''
        '''
        
    def list_message(self, message):
        '''
        '''