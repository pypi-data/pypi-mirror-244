import sys
import pathlib
from .Logger import logger
from .utilities.Caller import _get_caller_info
from ._version import __version__

_script_name = pathlib.Path(sys.argv[0]).stem # no extension    
_caller_info = _get_caller_info(_script_name)

_info = _script_name + '\n'
_doc = _caller_info['__doc__']
_author = _caller_info['__author__']
_ver = f"Bokger version {__version__}\n"

if _doc: _info += _doc + '\n'
if _author: _info += f"authored by {_author}\n"
_info += _ver

logger.log_code(_info)