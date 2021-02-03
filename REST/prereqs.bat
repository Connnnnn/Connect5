@echo off


:start
cls

set python_ver=3.9

cd venv/Scripts

call activate.bat
cd ../..
cd resources


python ./get-pip.py

pip install -r requirements.txt

cd ..

python -m app

pause
exit