# KeyTrainer

### type fast don't waste time

python -m venv new_venv\
source new_venv/bin/activate\
pip install -r requirements.txt\

datas=[('data/eye.svg', 'data'), ("data/data.db", "data"), ('data/reset.png', 'data'), ('data/cross.svg', 'data'),('data/keyIc.ico', 'data'), ('data/checkmark.svg', 'data'), ('data/themes.svg', 'data'), ('data/eye-slash.svg', 'data'),
    ('styles/defaultLight/textStyle.qss', 'styles/defaultLight'), ('styles/defaultDark/widgetStyle.qss', 'styles/defaultDark'), ('styles/baseStyle.qss', 'styles'), ('styles/defaultDark/textStyle.qss', 'styles/defaultDark'), ('styles/defaultLight/widgetStyle.qss', 'styles/defaultLight'), ('styles/defaultLight/textStyle.qss', 'styles/defaultLight'), ('styles/defaultDark/widgetStyle.qss', 'styles/defaultDark'), ('styles/baseStyle.qss', 'styles'), ('styles/defaultDark/textStyle.qss', 'styles/defaultDark'), ('styles/defaultLight/widgetStyle.qss', 'styles/defaultLight')],
    

pyinstaller keytrainer.spec


pyinstaller --windowed --name=KeyTrainer --icon=data/keyIc.ico -F --add-data "styles/defaultDark/widgetStyle.qss:styles/defaultDark" --add-data "styles/defaultDark/textStyle.qss:styles/defaultDark" --add-data "styles/defaultLight/widgetStyle.qss:styles/defaultLight" --add-data "styles/defaultLight/textStyle.qss:styles/defaultLight" --add-data "data/keyIc.ico:resources" --add-data "data/texts.json:data" --add-data "data/words.json:data" --add-data "data/profiles.json:data" --add-data "styles/baseStyle.qss:styles" main.py