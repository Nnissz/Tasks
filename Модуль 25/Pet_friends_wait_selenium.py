from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

def col_from_stat(web_driver):
    # количество питомцев из статистики.
    user_stat = WebDriverWait(web_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class=".col-sm-4 left"]'))
    )
    user_stat = user_stat.text.split("\n")
    print(user_stat)
    number_of_pets_from_stat = int(user_stat[1].split(": ")[1])
    return number_of_pets_from_stat


def test_show_all_pets(web_driver, login):
    # список всех обьектов питомца
    all_my_pets = web_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')
    # список своих питомцев не пуст
    assert len(all_my_pets) > 0
    pets_info = []
    for i in range(len(all_my_pets)):
        # получаем информацию о питомце '{{name}} {{type}} {{age}}'
        pet_info = all_my_pets[i].text.split("\n")[0]
        # добавляем в список pets_info информацию рода: имя, тип, возраст по каждому питомцу
        pets_info.append(pet_info)
    number_of_pets_from_stat = col_from_stat(web_driver)
    # на странице присутствуют все питомцы
    assert len(all_my_pets) == number_of_pets_from_stat, 'на странице присутствуют не все питомцы'


def test_check_images_in_cards(web_driver, login):
    # этот список image объектов c изображение питомца
    all_pets_images = web_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/th/img')
    number_of_pets_from_stat = col_from_stat(web_driver)
    # считаем карточки с изображением
    pets_with_photo = 0
    for i in range(len(all_pets_images)):
        if all_pets_images[i].get_attribute('src') != '':
            pets_with_photo += 1
    # проверяем что хотя бы у половины питомцев есть фото
    assert number_of_pets_from_stat / 2 < pets_with_photo, 'больше чем у половины питомцев нет фото'


def test_all_pets_have_name_type_age(web_driver, login):
    def get_card_info_td(i):
        return web_driver.find_elements(By.XPATH, f'//*[@id="all_my_pets"]/table[1]/tbody/tr/td[{i}]')

    # получен список объектов имя
    all_names = get_card_info_td(1)
    # получен список объектов тип
    all_types = get_card_info_td(2)
    # получен список объектов возраст
    all_ages = get_card_info_td(3)
    # проверяем что списоки своих питомцев не пусты и равны
    assert len(all_names) > 0 and len(all_types) > 0 and len(all_ages) > 0
    assert len(all_names) == len(all_types) == len(all_ages)
    for i in range(len(all_names)):
        # если одно из полей пустое , останавливаем тест failed
        assert (all_names[i].text == '' or all_types[i].text == '' or all_ages[i].text == '') == False, \
            'Не у всех питомцев в карточке заведены имя , возраст и порода'


def test_check_unique_pet_name(web_driver, login):
    all_pets_names = web_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[1]')

    def list_of_pet(all_pets_names):
        pets_name = []
        for i in range(len(all_pets_names)):
            # получаем информацию о питомце из списка всех своих питомцев
            pet_name = all_pets_names[i].text
            # избавляемся от лишних символов '\n×'
            pet_name = pet_name.split("\n")[0]
            # добавляем в список pets_name имя по каждому питомцу
            pets_name.append(pet_name)
        return pets_name

    pets_name = list_of_pet(all_pets_names)
    pets_name_uniq = list(set(pets_name))
    # проверяем, что количество уникальных имен соответсвует общему количеству
    assert len(pets_name) == len(pets_name_uniq)
