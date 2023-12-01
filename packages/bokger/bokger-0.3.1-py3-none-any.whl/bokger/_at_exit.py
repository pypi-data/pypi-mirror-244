from .Logger import logger
import sys
import atexit
import traceback
import pathlib


def show_html():
    html_path = pathlib.Path(sys.argv[0]).stem # no extension    
    logger.show(html_path)
    
def log_last_exception():    
    try:
        t = getattr(sys,'last_type') # not always defined. #https://docs.python.org/3/library/sys.html#sys.exc_info
        v = getattr(sys,'last_value')
        tb = getattr(sys,'last_traceback')
        formatted_lines = traceback.format_exception(t,v,tb)
        for line in formatted_lines:
            logger.log_code(line)
    except AttributeError: 
        pass

atexit.register(show_html)
atexit.register(log_last_exception)