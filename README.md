# KeyTrainer

### type fast don't waste time

python -m venv new_venv\
source new_venv/bin/activate\
pip install -r requirements.txt\

pyinstaller --windowed --name=KeyTrainer --icon=data/keyIc.ico -F --add-data "styles/dark.qss:styles"--add-data "styles/light.qss:styles" --add-data "data/keyIc.ico:resources" --add-data "styles/style.qss:styles" main.py