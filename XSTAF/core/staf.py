
import os
import sys
import time
import socket
import subprocess

from XSTAF.core.logger import LOGGER

#server name, server name maybe not correct, we should use ip address get from misc service
#ServerName = socket.getfqdn()

#staf monitor name
MonitorName = "DUTSTATUS"

class STAFError(Exception):
    pass

class STAF(object):
    '''
    STAF class
    '''
    #STAF status
    StatusUnKnown = 0b10000000
    STAFNotDetect = 0b10000001
    CannotImportPySTAF = 0b10000010
    CannotRegisterHandle = 0b10000011
    CannotUnRegisterHandle = 0b10000100
    STAFNotStart = 0b01000001
    STAFOK = 0b00000000
    
    PrettyStatus = {  STAFNotDetect : "Cannot detect STAF",
                    CannotImportPySTAF : "Cannot import PySTAF",
                    CannotRegisterHandle : "Cannot register handle",
                    CannotUnRegisterHandle : "Cannot unregister handle",
                    STAFNotStart : "STAF not start",
                    STAFOK : "STAF OK", }
                    
    #staf settings
    STAFSettings = {"STAFDir" : "",
                    }
    
    def __init__(self):
        self.staf_starter = "startSTAFProc.bat"
        self.handles = {}
        self.status = self.StatusUnKnown
    
    @classmethod
    def config(cls, **kwargs):
        for arg in kwargs.items():
            if arg[0] in cls.STAFSettings:
                cls.STAFSettings[arg[0]] = arg[1]
        
    @property
    def pretty_status(self):
        return self.PrettyStatus[self.status]
        
    def _check_status(self):
        '''
        check if staf exist
        check if staf process started
        '''
        #check if staf exist
        abs_staf_starter = os.path.join(self.STAFSettings["STAFDir"], self.staf_starter)
        if not os.path.isfile(abs_staf_starter):
            LOGGER.error("STAF starter not exist: %s" % abs_staf_starter)
            self.status = self.STAFNotDetect
            return False
            
        self.abs_staf_starter = abs_staf_starter
            
        #check if staf process exist
        #import python lib
        python_staf_lib_path = os.path.join(self.STAFSettings["STAFDir"], "bin")
        sys.path.append(python_staf_lib_path)
        try:
            import PySTAF
        except ImportError:
            LOGGER.error("Cannot import PySTAF")
            self.status = self.CannotImportPySTAF
            return False
            
        #try to register a test handle
        try:
            self.staf_handle = PySTAF.STAFHandle("test")
        except PySTAF.STAFException, e:
            if e.rc == 21:
                #error value 21 indicate STAF not running
                LOGGER.warning("Error code 21, STAF not running")
                self.status = self.STAFNotStart
            else:
                LOGGER.error("Error registering with STAF, RC: %d" % e.rc)
                self.status = self.CannotRegisterHandle
            return False
            
        #unregister test handle
        try:
            self.staf_handle.unregister()
        except PySTAF.STAFException, e:
            LOGGER.error("Error when unregister the test handle, RC: %d" % e.rc)
            self.status = self.CannotUnRegisterHandle
            return False
        
        self.status = self.STAFOK
        return True
        
    def check(self):
        self._check_status()
        LOGGER.debug("STAF current status: %s, pretty status: %s" % (self.status, self.pretty_status))
        
    def start(self):
        '''
        check if staf exist
        and start staf process if exist
        '''
        self.check()
        if self.status & 0b01000000:
            #by default we only have one staf process
            LOGGER.debug("Start staf process")
            p = subprocess.Popen(self.abs_staf_starter, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)
            self.check()
        
    def get_handle(self, handle_name):
        '''
        create and get STAF handle to control STAF service
        '''
        return STAFHandle(handle_name, self.STAFSettings["STAFDir"])
        
class STAFHandle(object):
    '''
    staf handle, every DUT thread will get a handle instance
    '''
    def __init__(self, handle_name, staf_dir):
        self.staf_handle_name = handle_name
        self.staf_dir = staf_dir
        #staf id, 0 is an invalid id
        self.staf_handle_id = 0
        self.staf_handle = None
        #staf process workload name
        self.workload_name = "XSTAF"
        
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
            LOGGER.error("Cannot import PySTAF")
            return False
            
        try:
            self.staf_handle = PySTAF.STAFHandle(self.staf_handle_name)
        except PySTAF.STAFException, e:
            if e.rc == 21:
                #error value 21 indicate STAF not running
                LOGGER.error("Error code 21, STAF not running, please start it and try again")
            else:
                LOGGER.error("Error registering with STAF, RC: %d" % e.rc)
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
        '''
        staf request submit function, most staf command will use this function to send
        '''
        #assert(not (self.staf_handle is None), "Need create staf handle first")
        while True:
            result = self.staf_handle.submit(location, service, request)
            if result.rc == 16:
                #during reboot, STAF may return 16
                #we will keep send the command until timeout
                LOGGER.warning("Submitting request encounter error 16, please check if your DUT still alive")
            elif result.rc != 0:
                LOGGER.error("Error submitting request, RC: %d, Result: %s" % (result.rc, result.result))
                LOGGER.error("Location: %s, Service: %s, Request: %s" % (location, service, request))
                #break the process
                raise STAFError("Error submitting request")
            else:
                #successful
                return result
            
            #sleep 20s if remote is not ready
            time.sleep(20)
        
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
        
        result = self.staf_handle.submit(location, service, request)
        if result.rc == 0 :
            return True
        else:
            LOGGER.warning("Ping DUT %s fail, RC: %d, Result: %s" % (DUT, result.rc, result.result))
            return False

    ########################################
    #
    # Misc Service
    #     used to detect if true server ip
    #
    ########################################
    def get_server_ip(self, DUT):
        location = '%s' % DUT
        service = 'Misc'
        request = 'whoami'
        
        result = self._staf_handle_submit(location, service, request)
        return result.resultContext.getRootObject()["physicalID"]
        
    ########################################
    #
    # File System (FS) Service
    #     We use FS service to copy log files to server
    #
    ########################################

    def create_directory(self, DUT, directory):
        location = '%s' % DUT
        service = 'FS'
        request = 'CREATE DIRECTORY %s FULLPATH' % directory
        self._staf_handle_submit(location, service, request)
    
    def clean_directory(self, DUT, directory):
        location = '%s' % DUT
        service = 'FS'
        request = 'DELETE ENTRY %s CHILDREN RECURSE CONFIRM IGNOREERRORS' % directory
        self._staf_handle_submit(location, service, request)
    
    def copy_log_file(self, DUT, remote_file, local_location):
        #before copy file to local, need give DUT trust level 4
        location = 'local'
        service = 'TRUST'
        request = 'SET MACHINE %s LEVEL 4' % DUT
        self._staf_handle_submit(location, service, request)
        #get server ip
        server_ip = self.get_server_ip(DUT)
        #copy
        location = '%s' % DUT
        service = 'FS'
        request = 'COPY FILE %s TODIRECTORY  %s TOMACHINE %s' % (remote_file, local_location, server_ip)
        self._staf_handle_submit(location, service, request)
        
    def copy_tmp_log_directory(self, DUT, remote_log_directory, local_location):
        #before copy file to local, need give DUT trust level 4
        location = 'local'
        service = 'TRUST'
        request = 'SET MACHINE %s LEVEL 4' % DUT
        self._staf_handle_submit(location, service, request)
        #get server ip
        server_ip = self.get_server_ip(DUT)
        #copy
        location = '%s' % DUT
        service = 'FS'
        request = 'COPY DIRECTORY %s TODIRECTORY  %s TOMACHINE %s RECURSE KEEPEMPTYDIRECTORIES' % (remote_log_directory, local_location, server_ip)
        self._staf_handle_submit(location, service, request)
        #delete remote log
        location = '%s' % DUT
        service = 'FS'
        request = 'DELETE ENTRY %s CHILDREN RECURSE CONFIRM ' % remote_log_directory
        self._staf_handle_submit(location, service, request)
        
    
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
        request = 'START COMMAND %s async workload %s stdout %s stderrTostdout' % (command, self.workload_name, log_file)
        
        result = self._staf_handle_submit(location, service, request)

        handle = result.resultContext
        LOGGER.info("Task started, with staf handle : %s" % handle)

    def query_process_status(self, DUT):
        '''
        query process status
        '''
        location = '%s' % DUT
        service = 'Process'
        request = 'LIST workload %s' % self.workload_name
        
        result = self._staf_handle_submit(location, service, request)
        #check return code, process not end if rc is None
        #every time we start/stop a process, we will free it, to make sure we only have one process info in status
        rc = result.resultContext.getRootObject()[0]["rc"]
        if rc is None:
            #process not end
            return None
        else:
            #check end time
            end_time = result.resultContext.getRootObject()[0]["endTimestamp"]
            return rc, end_time
            
    def free_process_status(self, DUT):
        '''
        free process info, we need to free process info before start new process
        '''
        location = '%s' % DUT
        service = 'Process'
        request = 'free workload %s' % self.workload_name
        
        self._staf_handle_submit(location, service, request)
        
    def stop_process(self, DUT):
        '''
        stop a process
        '''
        location = '%s' % DUT
        service = 'Process'
        request = 'STOP workload %s' % self.workload_name
        
        self._staf_handle_submit(location, service, request)
        
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
        #get server ip
        server_ip = self.get_server_ip(DUT)
        
        location = '%s' % DUT
        service = 'TRUST'
        request = 'GET MACHINE %s' % server_ip
        
        result = self.staf_handle.submit(location, service, request)
        if result:
            LOGGER.debug("Trust level for machine: %s is %s" % (server_ip, result.result))
            if int(result.result) < 5:
                LOGGER.debug("DUT is locked")
                return True
            else:
                LOGGER.debug("DUT is unlocked")
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
        #get server ip
        server_ip = self.get_server_ip(DUT)
        
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET MACHINE %s LEVEL 5' % server_ip
        
        result = self._staf_handle_submit(location, service, request)
        if not result:
            LOGGER.debug("Lock fail, request: %s" % request)
            return False
            
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET DEFAULT LEVEL 3'
        
        result = self._staf_handle_submit(location, service, request)
        if not result:
            LOGGER.debug("Lock fail, request: %s" % request)
            return False
            
        return True
        
    def release_DUT(self, DUT):
        '''
        set DUT default trust level to 5
        '''
        location = '%s' % DUT
        service = 'TRUST'
        request = 'SET DEFAULT LEVEL 5'
        
        self._staf_handle_submit(location, service, request)
    
    
#global staf instance
STAFInstance = STAF()
