@echo off
if not exist venv\Scripts\activate.bat (
    python -m venv venv & venv\Scripts\activate.bat & pip install -r requirements.txt & deactivate & echo "Done!" & pause
) else (
    echo 'Folder already has an virtual enviroment. Exit instalation' & pause
)