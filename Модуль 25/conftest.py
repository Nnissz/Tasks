import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from settings import valid_email, valid_password
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#@pytest.fixture
#def driver():
#    driver = webdriver.Chrome()
#    return driver

@pytest.fixture(autouse=True)
def web_driver():
    driver = webdriver.Chrome()
    # # Переходим на страницу авторизации
    # driver.get('https://petfriends.skillfactory.ru/login')
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def login(web_driver):
    # Переходим на страницу авторизации
    web_driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
    web_driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    web_driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    web_driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Ждем когда окажемся на главной странице пользователя
    # Задаем явное ожидание
    WebDriverWait(web_driver, 11).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'PetFriends')
    )
    # Проверяем, что мы оказались на главной странице пользователя
    # assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Задаем неявное ожидание
    web_driver.implicitly_wait(10)

    web_driver.get('https://petfriends.skillfactory.ru/my_pets')
    # yield login

