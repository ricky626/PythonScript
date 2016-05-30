import platform
import os


if(platform.architecture()[0] == '32bit'):
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"

import my_framework
import start_state
my_framework.run(start_state)