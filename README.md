# KeyTrainer

python -m venv new_venv\
source new_venv/bin/activate\
pip install -r requirements.txt\

pyinstaller --windowed --name=KeyTrainer --icon=resources/keyIc.ico -F --add-data "resources/keyIc.ico:resources" --add-data "style.qss:." main.py