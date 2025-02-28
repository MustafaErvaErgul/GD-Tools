@echo off
REM Package the app with PyInstaller
python -m PyInstaller --onefile --noconsole --icon=assets/icon.ico gdtools.py
if %errorlevel% neq 0 (
    echo Packaging failed!
    pause
    exit /b %errorlevel%
)

REM Copy config.ini into the dist folder
xcopy config.ini dist\ /Y

REM Copy the assets folder into the dist folder
xcopy assets dist\assets\ /E /I /Y

echo Packaging complete.