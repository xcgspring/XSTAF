
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
        
        #staf monitor name
        self.monitor_name = "DUTSTATUS"

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
        
    def _staf_handle_submit(self, location, service, request):
        assert(not self.staf_handle is None, "Need create staf handle first")
        result = self.staf_handle.submit(location, service, request)
        if (result.rc != 0):
            print("Error submitting request, RC: %d, Result: %s" % (result.rc, result.result))
            print("Location: %s, Service: %s, Request: %s" % (location, service, request))
            return False
        
        return result.result
        
    ########################################
    #
    # Queue Service
    #     We use STAF Queue to manage all tasks to be executed on clients
    #
    ########################################

    def add_message(self, ID, message, priority):
        '''
        Add message to handle message queue
        '''
        location = 'local'
        service = 'Queue'
        request = 'QUEUE MESSAGE %s HANDLE %s NAME %s' % (message, self.staf_handle_id, priority, ID) 
        
        return self._staf_handle_submit(location, service, request)
            
    def get_message(self):
        '''
        retrieve and removes oldest message form handle message queue
        '''
        location = 'local'
        service = 'Queue'
        request = 'GET FIRST 1'
        
        return self._staf_handle_submit(location, service, request)
        
    def peek_message(self):
        '''
        retrieve oldest message form handle message queue
        '''
        location = 'local'
        service = 'Queue'
        request = 'PEEK FIRST 1'
        
        return self._staf_handle_submit(location, service, request)
        
    def delete_message(self, ID):
        '''
        delete message form handle message queue
        '''
        location = 'local'
        service = 'Queue'
        request = 'DELETE NAME %s' % ID
        
        return self._staf_handle_submit(location, service, request)
        
    def list_message(self):
        '''
        retrieve the entire contents from handle message queue
        '''
        location = 'local'
        service = 'Queue'
        request = 'LIST'
        
        return self._staf_handle_submit(location, service, request))
        
    ########################################
    #
    # Process Service
    #     Used to execute tasks on clients
    #
    ########################################
        
    def start_process(self, DUT, command):
        '''
        start a process
        '''
        location = '%s' % DUT
        service = 'Process'
        request = 'START COMMAND %s ' % command
        
        return self._staf_handle_submit(location, service, request)
        
    def stop_process(self, DUT, process):
        '''
        stop a process
        '''
        location = '%s' % DUT
        service = 'Process'
        request = 'STOP ALL'
        
        return self._staf_handle_submit(location, service, request)
        
    ########################################
    #
    # monitor and trust service
    #     Used to record client status, 
    #     and simulate a lock function to prevent client controlled by others
    #
    ########################################
    
    def set_DUT_status(self, DUT, status):
        '''
        '''
        location = '%s' % DUT
        service = 'MONITOR'
        request = 'LOG MESSAGE %s NAME %s' % (status, self.monitor_name)
        
        return self._staf_handle_submit(location, service, request)
        
    def get_DUT_status(self, DUT):
        '''
        '''
        location = '%s' % DUT
        service = 'MONITOR'
        request = 'QUERY MACHINE %s NAME %s' % (, self.monitor_name)
        
        return self._staf_handle_submit(location, service, request)
        
    def lock_DUT(self, DUT):
        '''
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET DEFAULT 3'
        
        return self._staf_handle_submit(location, service, request)
        
    def release_DUT(self, DUT):
        '''
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET DEFAULT 5'
        
        return self._staf_handle_submit(location, service, request)
    