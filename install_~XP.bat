mkdir ../.api
fsutil hardlink create ../boot.bat boot.bat
xcopy /s .api/python ../.api/python