
import os
import sys
import socket
import subprocess
import logger

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
            logger.LOGGER.error("STAF starter not exist: %s" % abs_staf_starter)
            return False
            
        #by default we only have one staf process
        subprocess.Popen(abs_staf_starter, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
        
    def get_handle(self, handle_name):
        '''
        create and get STAF handle to control STAF service
        '''
        return STAFHandle(handle_name, self.staf_dir)
        
class STAFHandle(object):
    '''
    staf handle, every DUT thread will get a handle instance
    '''
    def __init__(self, handle_name, staf_dir):
        self.staf_handle_name = handle_name
        #staf id, 0 is an invalid id
        self.staf_handle_id = 0
        self.staf_handle = None
        
        self.staf_dir = staf_dir
        
    def register(self):
        ''' 
        create a staf handle and register to staf process
        '''
        #import python lib
        python_staf_lib_path = os.path.join(self.staf_dir, "bin")
        sys.path.append(python_staf_lib_path)
        try:
            import PySTAF
        except ImportError:
            logger.LOGGER.error("Cannot import PySTAF")
            return False
            
        try:
            self.staf_handle = PySTAF.STAFHandle(self.staf_handle_name)
        except PySTAF.STAFException, e:
            if e.rc == 21:
                #error value 21 indicate STAF not running
                logger.LOGGER.error("Error code 21, STAF not running, please start it and try again")
            else:
                logger.LOGGER.error("Error registering with STAF, RC: %d" % e.rc)
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
            logger.LOGGER.error("Error submitting request, RC: %d, Result: %s" % (result.rc, result.result))
            logger.LOGGER.error("Location: %s, Service: %s, Request: %s" % (location, service, request))
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
        request = 'Ping machine %s' % DUT
        
        return self._staf_handle_submit(location, service, request)
        
    ########################################
    #
    # File System (FS) Service
    #     We use FS service to copy log files to server
    #
    ########################################

    def copy_log(self, DUT, remote_file, local_location):
        #before copy file to local, need give DUT trust level 4
        location = 'local'
        service = 'TRUST'
        request = 'SET MACHINE %s LEVEL 4' % DUT
        assert(self._staf_handle_submit(location, service, request))
        
        location = '%s' % DUT
        service = 'FS'
        request = 'COPY FILE %s TODIRECTORY  %s TOMACHINE %s' % (remote_file, local_location, ServerName)
        return self._staf_handle_submit(location, service, request)
        
        
    ########################################
    #
    # Process Service
    #     Used to execute tasks on clients
    #
    ########################################
        
    def start_process(self, DUT, command, log_file):
        '''
        start a process, stdout and stderr store to a tmp location
        '''
        location = '%s' % DUT
        service = 'Process'
        request = 'START COMMAND %s wait stdout %s stderr %s' % (command, log_file, log_file)
        
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
    def check_if_DUT_locked (self, DUT):
        '''
        check if DUT locked
        if trust level for server is less than 5, server cannot change DUT trust level 
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'GET MACHINE %s' % ServerName
        
        result = self._staf_handle_submit(location, service, request)
        if result:
            logger.LOGGER.debug("Trust level for machine: %s is %s" % (ServerName, result))
            if int(result) < 5:
                logger.LOGGER.debug("DUT is locked")
                return True
            else:
                logger.LOGGER.debug("DUT is unlocked")
                return False
        else:
            #Cannot get trust level, could be trust level is less than 2
            #So DUT is locked
            return True
        
    def lock_DUT(self, DUT):
        '''
        set DUT trust level for server to 5
        then set DUT default trust level to 3
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET MACHINE %s LEVEL 5' % ServerName
        
        result = self._staf_handle_submit(location, service, request)
        if not result:
            logger.LOGGER.debug("Lock fail")
            return False
            
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET DEFAULT LEVEL 3'
        
        result = self._staf_handle_submit(location, service, request)
        if not result:
            logger.LOGGER.debug("Lock fail")
            return False
            
        return True
        
    def release_DUT(self, DUT):
        '''
        set DUT default trust level to 5
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET DEFAULT LEVEL 5'
        
        return self._staf_handle_submit(location, service, request)
    