import os
from .base import *
if os.environ.get("CMS") == 'prod':
    from .prod import *
else:
    from .dev import *
