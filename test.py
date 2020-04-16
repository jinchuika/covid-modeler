import os
import sys
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

from modeler.wrapper import Modeler

modeler = Modeler('Guatemala', predict_len=1.5)
modeler.process()