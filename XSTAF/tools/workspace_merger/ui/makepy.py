
import os
import re

pyuic4 = r"C:\Python27\Lib\site-packages\PyQt4\pyuic4.bat"
pyrcc4 = r"C:\Python27\Lib\site-packages\PyQt4\pyrcc4.exe"

current_dir = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(current_dir):
    for file_name in files:
        if re.match(".*\.ui$", file_name) != None:
            command = "%s -o %s %s" % (pyuic4, "ui_"+file_name.split(".")[0]+".py", file_name)
            print(command)
            os.chdir(root)
            os.system(command)
        if re.match(".*\.qrc", file_name) != None:
            command = "%s -o %s %s" % (pyrcc4, file_name.split(".")[0]+"_rc.py", file_name)
            print(command)
            os.chdir(root)
            os.system(command)