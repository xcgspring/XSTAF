
import sys
import types
import logging

LOGNAME = None

CONFIGS = { "logger_name":"XSTAF", 
            "logging_level_file":logging.DEBUG,
            "logging_level_stream":logging.DEBUG, 
            "logging_stream": None, #need set to UI edit stream
            "logging_file":"XSTAF.log", 
            "file_logging_mode":"w", 
            "formatter":"[ %(levelname)s ][ %(filename)s:%(lineno)d ] %(message)s", }
                 
def level_name(level):
    return logging._levelNames[level]
    
def html_emit(self, record):
    levelno = record.levelno
    if(levelno>=logging.CRITICAL):
        color_str = '<div style="color:red">%s</div>' # red
    elif(levelno>=logging.ERROR):
        color_str = '<div style="color:red">%s</div>' # red
    elif(levelno>=logging.WARN):
        color_str = '<div style="color:yellow">%s</div>' # yellow
    elif(levelno>=logging.INFO):
        color_str = '<div style="color:black">%s</div>' # black
    elif(levelno>=logging.DEBUG):
        color_str = '<div style="color:gray">%s</div>' # gray
    else:
        color_str = '<div style="color:black">%s</div>' # black
    record.msg = color_str % record.msg
    logging.StreamHandler.emit(self, record)
                 
def config():
    '''config logger with settings in configure file
    '''
    logger_name=CONFIGS["logger_name"]
    logging_level_file=CONFIGS["logging_level_file"]
    logging_level_stream=CONFIGS["logging_level_stream"]
    logging_stream=CONFIGS["logging_stream"]
    logging_file=CONFIGS["logging_file"]
    file_logging_mode=CONFIGS["file_logging_mode"]
    formatter_string=CONFIGS["formatter"]

    #config logger according input configs
    logger = logging.getLogger(logger_name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.handlers = []

    if logging_stream:
        stream_handler = logging.StreamHandler(logging_stream)
        stream_handler.setLevel(logging_level_stream)
        formatter = logging.Formatter(formatter_string)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        #replace stream handle emit to html emit, then QT edit can show different color for different log level
        stream_handler.emit = types.MethodType(html_emit, stream_handler)
        
    file_handler = logging.FileHandler(logging_file, mode=file_logging_mode)
    file_handler.setLevel(logging_level_file)
    formatter = logging.Formatter(formatter_string)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    global LOGNAME
    LOGNAME = logger_name

def LOGGER():
    global LOGNAME
    if LOGNAME == None:
        config()
    return logging.getLogger(LOGNAME)