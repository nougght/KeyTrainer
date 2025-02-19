# KeyTrainer

### type fast don't waste time

python -m venv new_venv\
source new_venv/bin/activate\
pip install -r requirements.txt\

pyinstaller --windowed --name=KeyTrainer --icon=resources/keyIc.ico -F --add-data "dark.qss:." --add-data "theme.txt:." --add-data "light.qss:." --add-data "resources/keyIc.ico:resources" --add-data "style.qss:." main.py