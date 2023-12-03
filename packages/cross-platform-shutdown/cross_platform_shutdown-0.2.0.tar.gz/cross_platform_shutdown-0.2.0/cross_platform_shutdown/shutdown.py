import os
import platform

class OSNotSupported(Exception): pass

def shutdown():
    os_name = platform.system()
    if os_name == "Windows":
        os.system("shutdown /s /f")
    elif os_name == "Linux":
        os.system("shutdown -h now")
    elif os_name == "Darwin":
        os.system("shutdown -h now")
    else:
        raise OSNotSupported()
