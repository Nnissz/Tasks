# project :
    Работа с ресурсом https://petfriends.skillfactory.ru

# Настройка проекта:
    1. Создаем виртуапльное окружение командой:
        python -m venv venv
    2. Активируем виртуальное окружение командой (MacOS/Linux):
        source venv/bin/activate
       для Windows другая команда:
        \env\Scripts\activate.bat
    3. Установка зависимостей:
        pip install -r requirements.txt
    4. Настроить в IDE(Pycharm) текущий интерпритатор, выбрав текущее виртуальное окружение

# Запуск тестов:
    Нажмите на зеленую стрелочку слева от названия теста, если она вдруг не появилась, 
    значит вы не установили библиотеку pytest. Установите командой: pip install pytest.

# Описание пректа:
    conftest.py - файл с фикстурами
    settings.py - файл с логином и паролем
    Pet_friends_wait_selenium.py -  файл с тестами