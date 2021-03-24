"""
OpenNEM Python Client Library

"""
import sys
import warnings
from pathlib import Path

# Check minimum required Python version
if sys.version_info < (3, 8):
    print("OpenNEMPY %s requires Python 3.8 or greater")
    sys.exit(1)


# Ignore noisy twisted deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="twisted")


PATH_OPENNEM = Path(__file__).parent
PATH_CWD = Path.cwd()

from opennem.settings import settings  # noqa

from .client import OpenNEMClient  # noqa

api = OpenNEMClient()
