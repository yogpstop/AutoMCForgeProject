mkdir ../.api
fsutil hardlink create ../boot.bat boot.bat
fsutil hardlink create ../main.py main.py
xcopy /s .api/python ../.api/python