echo off

call C:\DEV\python3\python --version
call C:\DEV\python3\Scripts\pip --version
call C:\DEV\python3\python -m pip install --upgrade pip
call C:\DEV\python3\Scripts\pip --version

rem set arg1=%1
rem call C:\DEV\python362\Scripts\pip install %arg1% -U
rem call C:\DEV\python3\Scripts\pip install %arg1%

call C:\DEV\python3\Scripts\pip install --upgrade requests
call C:\DEV\python3\Scripts\pip install --upgrade simpleJson
call C:\DEV\python3\Scripts\pip install --upgrade pytz
call C:\DEV\python3\Scripts\pip install --upgrade pyparsing
call C:\DEV\python3\Scripts\pip install --upgrade cmd2
call C:\DEV\python3\Scripts\pip install --upgrade PyMySQL
call C:\DEV\python3\Scripts\pip install --upgrade pymongo
call C:\DEV\python3\Scripts\pip install --upgrade colorama
call C:\DEV\python3\Scripts\pip install --upgrade astroid
call C:\DEV\python3\Scripts\pip install --upgrade pylint
call C:\DEV\python3\Scripts\pip install --upgrade isort
call C:\DEV\python3\Scripts\pip install --upgrade pyperclip
call C:\DEV\python3\Scripts\pip install --upgrade numpy matplotlib

call C:\DEV\python3\Scripts\pip list