# OctoPrintStatus (Concept)

A python GUI program what shows the status of the 3dprinter in octoprint.

![](https://github.com/AndreRozendaal/OctoPrintStatus/raw/master/images/screencapture1.PNG)
![](https://github.com/AndreRozendaal/OctoPrintStatus/raw/master/images/screencapture2.PNG)

# TODO

- complete pytest, after adding extra method test is broken. must mock two function instead of one
- by reboot the octoprint server, program crash with exception.
- add about screen
- add configuration screen for add and change url and api key
- show video or snapshots
  snapshot_url: http://192.168.2.55/webcam/?action=snapshot
  movie: http://192.168.2.55/webcam/?action=stream
  howto example: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Media_Player_VLC_Based.py
  

# Windows executable
created with: python -m pysimplegui-exemaker.pysimplegui-exemaker
located: dist/OctoPrintStatus.exe

