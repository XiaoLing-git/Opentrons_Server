dist := $(abspath dist)
build := $(abspath build)
api := $(abspath api)
main := $(abspath main)
build_standalone :=$(abspath build_standalone.py)
python :=$(abspath ../../venv/Scripts/python.exe)
#C:\Users\opentrons\Desktop\Opentrons_Server\venv\Scripts\python.exe

del:
	$(RM)  $(abspath *.spec) $(abspath discovery*)
	$(RM) -r $(abspath dist) $(abspath build)

dist:
#	echo $(python) $(build_standalone)
	$(python) $(build_standalone)

test:
	$(python) $(main)/ssh.py

