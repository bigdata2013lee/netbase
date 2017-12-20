# -*- coding: utf-8 -*-
from django.core.management import execute_manager
import sys, os
try:
    reload(sys)
    sys.path.append(os.getcwd())
    from netWeb import  settings # Assumed to be in the same directory.
except ImportError, e:
    print e
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv)<2:
        sys.argv.append("runserver")
    try:
        execute_manager(settings)
    except Exception, e:
        import traceback;traceback.print_exc();
        sys.exit(2)

