from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Борис', animal_type='сибирская',
                                     age='3', pet_photo='images/catBoris.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Люся", "бенгальская", "5", "images/catLusia.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='мейн-кун', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

    #--------------------------------

def test_add_new_pet_without_photo_with_valid_data(name='Кузя', animal_type='мейн-кун',
                                         age='3'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type



def test_add_photo_of_pet_with_valid_data(pet_photo='images/catBoris.jpg'):
    """Проверяем что можно добавить фото питомца с корректными данными"""
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создаем нового питомца без фото
    _, new_pet = pf.add_new_pet_without_photo(auth_key, "Люся", "бенгальская", "5")
        # _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id созданного питомца
    pet_id = new_pet['id']

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем фото питомца к созданному ранее питомцу с сохраненным id
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа равен 200
    assert status == 200

def test_get_api_key_for_incorrect_login(email='1234@mail.ru', password=valid_password):
    """ Проверяем что запрос api ключа у незарегистрированного пользователя c верным паролем вернет ошибку"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    # assert 'key' in result

def test_get_api_key_for_incorrect_password(email=valid_email, password='123456789'):
    """ Проверяем что запрос api ключа у зарегистрированного пользователя с неверным паролем вернет ошибку"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    # assert 'key' in result

def test_get_all_pets_with_incorrect_key(filter=''):
    """ Проверяем что запрос не выполнится, т.к. ключ auth_key будет неверный."""

    #Подставляем неверный ключ
    auth_key = {"key":"4832ccc28583501c9d50b9c81fd24ffab118680be8d41b8a331b42a5incorrect"}
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    # assert len(result['pets']) > 0

def test_successful_update_self_pet_info_with_incorrect_id(name='Мурзик', animal_type='мейн-кун', age=5):
    """Проверяем возможность обновления информации о питомце с неправильным id"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.update_pet_info(auth_key, '1000000000000000000', name, animal_type, age)

    # Проверяем что статус ответа = 400
    assert status == 400

def test_add_photo_of_pet_with_incorrect_id(pet_photo='images/catBoris.jpg'):
    """Проверяем что можно добавить фото питомца с неправильным id питомца.
     Примечание: лучше исправить программно, чтобы выводилась ошибка 400, вместо ошибки 500."""
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # создаем нового питомца без фото
    _, new_pet = pf.add_new_pet_without_photo(auth_key, "Люся", "бенгальская", "5")
        # _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём несуществующий id питомца
    pet_id = '1000000000000000000'
    #pet_id = new_pet['id']

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем фото питомца к созданному ранее питомцу с сохраненным id
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Проверяем статус ответа
    assert status == 500

def test_add_new_pet_with_incorrect_key(name='Борис', animal_type='сибирская',
                                     age='3', pet_photo='images/catBoris.jpg'):
    """Проверяем что можно добавить питомца с некорректным ключом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Подставляем неверный ключ
    auth_key = {"key": "4832ccc28583501c9d50b9c81fd24ffab118680be8d41b8a331b42a5incorrect"}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

def test_successful_delete_self_pet_with_incorrect_key():
    """Проверяем возможность удаления питомца с неправильным ключом"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Люся", "бенгальская", "5", "images/catLusia.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Подставляем неверный ключ
    bad_auth_key = {"key": "4832ccc28583501c9d50b9c81fd24ffab118680be8d41b8a331b42a5incorrect"}

    # отправляем запрос на удаление
    status, _ = pf.delete_pet(bad_auth_key, pet_id)

    #Проверяем статус
    assert status == 403

def test_update_self_pet_info_with_incorrect_key(name='Мурзик', animal_type='мейн-кун', age=5):
    """Проверяем возможность обновления информации о питомце с неверным ключом"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
    # Подставляем неверный ключ
        bad_auth_key = {"key": "4832ccc28583501c9d50b9c81fd24ffab118680be8d41b8a331b42a5incorrect"}
        status, result = pf.update_pet_info(bad_auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем статус ответа
        assert status == 403















