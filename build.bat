@echo off

pyinstaller --onefile --name VoiceGPT --noconsole --add-data "logo.png;." --add-data "beep.wav;." VoiceGPT.py

type NUL > temp.txt
echo import sys; sys.setrecursionlimit(sys.getrecursionlimit() * 5) >> temp.txt
type VoiceGPT.spec >> temp.txt
copy /Y temp.txt VoiceGPT.spec

pyinstaller VoiceGPT.spec

xcopy /Y "logo.png" "dist\"
xcopy /Y "beep.wav" "dist\"
del VoiceGPT.zip

powershell Compress-Archive dist VoiceGPT.zip

rd /S /Q dist
del /Q VoiceGPT.spec
rd /S /Q build
del temp.txt

pause
