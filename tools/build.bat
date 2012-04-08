copy setup.py ..\
cd ..\
python setup.py build
tools\upx build\exe.win32-2.7\*
del setup.py
pause