
import sys
import types
import logging

from PyQt4 import QtCore, QtGui

def level_name(level):
    return logging._levelNames[level]

class CustomLogger(QtCore.QObject):
    #we want used logger in multiple thread, need emit Qt signals
    #so need to inherit QObject
    
    #signal to update editor
    updateLog = QtCore.SIGNAL("update_editor")
      
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.logger_name = "XSTAF"
        self.logger = logging.getLogger(self.logger_name)
        
        #configs
        self.configs = { "logging_level_file":logging.DEBUG,
                    "logging_level_stream":logging.DEBUG, 
                    "logging_stream": sys.stdout,
                    "logging_file":"XSTAF.log", 
                    "file_logging_mode":"w", 
                    "formatter":"[ %(levelname)s ][ %(filename)s:%(lineno)d ] %(message)s", }
        
    def config(self, **kwargs):
        '''config logger with settings in configure file
        '''
        #update configs
        for arg in kwargs.items():
            key = arg[0]
            value = arg[1]
            if key in self.configs:
                self.configs[key] = value
        
        logging_level_file=self.configs["logging_level_file"]
        logging_level_stream=self.configs["logging_level_stream"]
        logging_stream=self.configs["logging_stream"]
        logging_file=self.configs["logging_file"]
        file_logging_mode=self.configs["file_logging_mode"]
        formatter_string=self.configs["formatter"]

        #config logger according input configs
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []

        if logging_stream:
            stream_handler = logging.StreamHandler(logging_stream)
            stream_handler.setLevel(logging_level_stream)
            formatter = logging.Formatter(formatter_string)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)
            
            #custom emit
            def custom_emit(*args):
                record = args[1]
                #emit Qt signal to update edit view
                self.emit(self.updateLog, record)
                #need for file handle
                logging.StreamHandler.emit(*args)
            
            #replace stream handle emit to custom emit
            stream_handler.emit = types.MethodType(custom_emit, stream_handler)
            
        file_handler = logging.FileHandler(logging_file, mode=file_logging_mode)
        file_handler.setLevel(logging_level_file)
        formatter = logging.Formatter(formatter_string)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def debug(self, msg):
        self.logger.debug(msg)
        
    def info(self, msg):
        self.logger.info(msg)
        
    def warn(self, msg):
        self.logger.warn(msg)
        
    def warning(self, msg):
        self.logger.warn(msg)
        
    def error(self, msg):
        self.logger.error(msg)
        
    def critical(self, msg):
        self.logger.critical(msg)
        
LOGGER = CustomLogger()