# KeyTrainer

### type fast don't waste time

python -m venv new_venv\
source new_venv/bin/activate\
pip install -r requirements.txt\


pyinstaller keytrainer.spec


pyinstaller --windowed --name=KeyTrainer --icon=data/keyIc.ico -F --add-data "styles/defaultDark/widgetStyle.qss:styles/defaultDark" --add-data "styles/defaultDark/textStyle.qss:styles/defaultDark" --add-data "styles/defaultLight/widgetStyle.qss:styles/defaultLight" --add-data "styles/defaultLight/textStyle.qss:styles/defaultLight" --add-data "data/keyIc.ico:resources" --add-data "data/texts.json:data" --add-data "data/words.json:data" --add-data "data/profiles.json:data" --add-data "styles/baseStyle.qss:styles" main.py