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

<a href="https://postimages.org/" target="_blank"><img src="https://i.postimg.cc/J4V5Y9hD/image.png" alt="image"></a><br><br>
<a href="https://postimg.cc/pyCjpczL" target="_blank"><img src="https://i.postimg.cc/vHFt2pmf/image-1.png" alt="image-1"></a><br><br>
<a href="https://postimg.cc/bdgnsVkN" target="_blank"><img src="https://i.postimg.cc/hPW1ZHGx/image-2.png" alt="image-2"></a><br><br>

### Подробная статистика профиля и история тренировок с графиками

<a href="https://postimg.cc/YjRFhDY2" target="_blank"><img src="https://i.postimg.cc/CLTsrWK8/image-3.png" alt="image-3"></a><br><br>
<a href="https://postimg.cc/Cd78zrkK" target="_blank"><img src="https://i.postimg.cc/VLQWZ3NX/image-4.png" alt="image-4"></a><br><br>
<a href="https://postimg.cc/xq5mcpMq" target="_blank"><img src="https://i.postimg.cc/5NdSKZt5/image-5.png" alt="image-5"></a><br><br>

### Темная тема

<a href="https://postimg.cc/vDhnc2fc" target="_blank"><img src="https://i.postimg.cc/Fs5VC2Kg/image-6.png" alt="image-6"></a><br><br>

### Переключение языка и прочие настройки

<a href="https://postimg.cc/1fzq60rP" target="_blank"><img src="https://i.postimg.cc/zXCSs0LL/image-7.png" alt="image-7"></a><br><br>

## _Команды для перевода интерфейса_ 
_Создание .ts файлов с фразами из кода_: \
`pyside6-lupdate main.py ui/main_window.py ui/statistics_widget.py ui/other_widgets.py ui/settings_widget.py ui/starter_window.py ui/typing_widget.py -ts assets/en.ts` \
_Необходимо вручную добавить переводы фраз в .ts файл и затем конвертировать в .qm файл_: \
`pyside6-lrelease assets/en.ts -qm assets/en.qm`
