# KeyTrainer

### type fast don't waste time

Десктоп приложение для улучшения скорости набора текста на клавиатуре и обучения слепой печати. Написан на PySide6 (официальный Qt для Python) и может быть собран для Windows, Linux и MacOS. \
Данные для приложения хранятся локально в SQLite, необходимые ресурсы(тексты и слова) подгружаются из .sql файлов при первом запуске.

## Функционал

- Режимы тренировки `words` и `text`.
- Тренировочные тексты на Русском и Английском языках (а также с ключевыми словами и выражениями Python и C++).
- Поддержка уровней сложности: `easy`, `normal`, `hard`.
- Выбор языка тренировки и переключение раскладки экранной клавиатуры.
- Отображение статистики в процессе печати (скорость, точность, ошибки, прогресс).
- Сохранение результатов сессий в SQLite и просмотр общей статистики пользователя.
- Экспорт и импорт пользовательских данных (`.sql`).
- Оффлайн-работа без внешних сервисов.
- Английский и русский язык интерфейса.
- Светлая и темная темы.

## Установка зависимостей

``` bash
python -m venv new_venv

# Windows (PowerShell)
.\new_venv\Scripts\Activate.ps1
# Linux/macOS
# source new_venv/bin/activate

pip install -r requirements.txt \

# сборка файла с ресурсами (обязательно)
pyside6-rcc assets.qrc -o res.py
```

Можно запускать из исходников или собрать в исполняемый файл.

## Сборка в исполняемый файл

``` bash
# исполняемый файл (появится dist/KeyTrainer.exe)
pyinstaller KeyTrainer.spec
```

## Скриншоты

<a href="https://postimages.org/" target="_blank"><img src="https://i.postimg.cc/g0LtC33B/image-1.png" alt="image-1"></a><br><br> 

### Переключение языка

<a href="https://postimages.org/" target="_blank"><img src="https://i.postimg.cc/FKkCM003/23AEDC69-A7C1-43E4-9078-318F46077922.png" alt="23AEDC69-A7C1-43E4-9078-318F46077922"></a><br><br>
<a href="https://postimg.cc/SXqG82TC" target="_blank"><img src="https://i.postimg.cc/zfH2sTTt/image-2.png" alt="image-2"></a><br><br>

### Темная тема

<a href="https://postimg.cc/1gPK6nCq" target="_blank"><img src="https://i.postimg.cc/zfH2sTT0/image-3.png" alt="image-3"></a><br><br> 

### Подробная статистика профиля

<a href="https://postimg.cc/8FDbWJKT" target="_blank"><img src="https://i.postimg.cc/0NKXT77K/69CB3A47-A09D-4AF4-AF87-A1B49B30DC4E.png" alt="69CB3A47-A09D-4AF4-AF87-A1B49B30DC4E"></a><br><br>
<a href="https://postimg.cc/nsZ17jRz" target="_blank"><img src="https://i.postimg.cc/BvP7r22x/6C61D8C9-08AC-4F6E-B375-301C4C9CADCC.png" alt="6C61D8C9-08AC-4F6E-B375-301C4C9CADCC"></a><br><br>

### История тренировок с графиками

<a href="https://postimg.cc/LqRVfYCn" target="_blank"><img src="https://i.postimg.cc/3w0fs22C/image-5.png" alt="image-5"></a><br><br>
<a href="https://postimg.cc/SXqG82TR" target="_blank"><img src="https://i.postimg.cc/pd5cwKKf/247296DB-3783-47FA-AD16-F4A633B8B52B.png" alt="247296DB-3783-47FA-AD16-F4A633B8B52B"></a><br><br>

### Настройки

<a href="https://postimg.cc/cKZcYg9J" target="_blank"><img src="https://i.postimg.cc/9fwg6yyy/C0468B96-4EE7-4674-BDAE-2683974DC47F.png" alt="C0468B96-4EE7-4674-BDAE-2683974DC47F"></a><br><br>

## _Команды для перевода интерфейса_ 
_Создание .ts файлов с фразами из кода_: \
`pyside6-lupdate main.py ui/main_window.py ui/statistics_widget.py ui/other_widgets.py ui/settings_widget.py ui/starter_window.py ui/typing_widget.py -ts assets/en.ts` \
_Необходимо вручную добавить переводы фраз в .ts файл и затем конвертировать в .qm файл_: \
`pyside6-lrelease assets/en.ts -qm assets/en.qm`
