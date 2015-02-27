
import os
import sys
import socket
import subprocess
#import custom logger

#server name
ServerName = socket.getfqdn()
#staf monitor name
MonitorName = "DUTSTATUS"

class STAF(object):
    '''
    STAF class
    '''
    def __init__(self, staf_dir):
        self.staf_dir = staf_dir
        self.staf_starter = "startSTAFProc.bat"

        self.handles = {}

    def check_and_start_staf(self):
        '''
        check if staf exist
        and start staf process if exist
        '''
        abs_staf_starter = os.path.join(self.staf_dir, self.staf_starter)
        if not os.path.isfile(abs_staf_starter):
            print("STAF starter not exist: %s" % abs_staf_starter)
            return False
            
        #by default we only have one staf process
        subprocess.Popen(abs_staf_starter, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
        
    def get_handle(self, handle_name):
        '''
        create and get STAF handle to control STAF service
        '''
        return STAFHandle(handle_name)
        
class STAFHandle(object):
    '''
    staf handle, every DUT thread will get a handle instance
    '''
    def __init__(self, handle_name):
        self.staf_handle_name = handle_name
        #staf id, 0 is an invalid id
        self.staf_handle_id = 0
        self.staf_handle = None
        
    def register(self):
        ''' 
        create a staf handle and register to staf process
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
        
    def configure(self):
        '''
        add custom configurations here
        '''
        #add more configures here
        
        return True
        
    def _staf_handle_submit(self, location, service, request):
        assert(not (self.staf_handle is None), "Need create staf handle first")
        result = self.staf_handle.submit(location, service, request)
        if (result.rc != 0):
            print("Error submitting request, RC: %d, Result: %s" % (result.rc, result.result))
            print("Location: %s, Service: %s, Request: %s" % (location, service, request))
            return False
        
        return result.result
        
    ########################################
    #
    # Ping Service
    #     used to detect if DUT exist
    #
    ########################################
    def ping(self, DUT):
        location = 'local'
        service = 'Ping'
        request = 'Ping %s' % DUT
        
        return self._staf_handle_submit(location, service, request)
        
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
        
        return self._staf_handle_submit(location, service, request)
        
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
    # monitor service
    #     Used to record client status
    #
    ########################################
    
    def set_monitor_message(self, DUT, message):
        '''
        '''
        location = '%s' % DUT
        service = 'MONITOR'
        request = 'LOG MESSAGE %s NAME %s' % (message, MonitorName)
        
        return self._staf_handle_submit(location, service, request)
        
    def get_monitor_machine_name(self, DUT):
        '''
        '''
        location = '%s' % DUT
        service = 'MONITOR'
        request = 'LIST MACHINES'
        
        return self._staf_handle_submit(location, service, request)
        
    def get_monitor_message(self, DUT):
        '''
        '''
        machine_name = self.get_monitor_machine_name(DUT)
        location = '%s' % DUT
        service = 'MONITOR'
        request = 'QUERY MACHINE %s NAME %s' % (machine_name, MonitorName)
        
        return self._staf_handle_submit(location, service, request)
        
    def delete_all_monitor_message(self, DUT):
        '''
        '''
        location = '%s' % DUT
        service = 'MONITOR'
        request = 'DELETE CONFIRM'
        
        return self._staf_handle_submit(location, service, request)
        
    ########################################
    #
    # trust service
    #     Used to simulate lock function, prevent DUT used by others
    #
    ########################################
    def check_if_DUT_locked(self, DUT):
        '''
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'GET MACHINE %s' % ServerName
        
        return self._staf_handle_submit(location, service, request)
        
    def lock_DUT(self, DUT):
        '''
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET DEFAULT LEVEL 3'
        
        self._staf_handle_submit(location, service, request)
        
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET MACHINE %s LEVEL 5' % ServerName
        
        self._staf_handle_submit(location, service, request)
        
    def release_DUT(self, DUT):
        '''
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET DEFAULT LEVEL 5'
        
        return self._staf_handle_submit(location, service, request)
    