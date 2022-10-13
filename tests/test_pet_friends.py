from api import PetFriend
from settings import email, passwd
import os

pf = PetFriend()


def test_get_api_key_for_valid_user(email=email, password=passwd):
    """Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем API ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступные значения параметра filter = 'my_pets' или ''. """

    _, auth_key = pf.get_api_key(email, passwd)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) > 0


def test_get_pets_with_valid_key_related_to_the_current_user(filter='my_pets'):
    """Проверяем, что запрос питомцев текущего пользователя проходит со статусом 200 и возвращает список
    его питомцев или пустой список.
    Для этого сначала получаем API ключ и сохраняем в переменную auth_key.
    Доступные значения параметра filter = 'my_pets' или ''. """

    _, auth_key = pf.get_api_key(email, passwd)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) >= 0


def test_create_pet_simple_with_valid_data(name='Потапыч', animal_type='медведь', age=46):
    """Проверяем, что можно добавить питомца с корректными данными без фотографии"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(email, passwd)

    # Добавляем питомца без фотографии
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_add_photo_of_pet(pet_photo='images/gena.jpeg'):
    """Проверяем, что можно добавить фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(email, passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового без фото и опять запрашиваем
    # список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, 'Суперкот', 'кот', 3)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    # assert result['pet_photo'] == 'image/jpeg'


def test_add_new_pet_with_valid_data(name='Котейка', animal_type='кошка',
                                     age=15, pet_photo='images/cat.jpeg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(email, passwd)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Смешарик', animal_type='песик', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(email, passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('There is no my pets')


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(email, passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список
    # своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, 'Суперкот', 'кот', 3)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_get_api_key_for_incorrect_email(email='dlsjgghs@gmail.com', password=passwd):
    """Проверяем, что запрос API ключа возвращает статус 403 и в результате отсутствует слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_dont_get_api_key_for_incorrect_password(email=email, password='slghaathg'):
    """Проверяем, что запрос API ключа возвращает статус 403 и в результате отсутствует слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_dont_get_list_of_pets_with_incorrect_filter(filter='not_my_pets'):
    """Метод проверяет, что в параметр фильтр нельзя ввести неподдерживаемое значение, запрос к серверу
    выдает внутреннюю ошибку на стороне сервера"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(email, passwd)
    status, _ = pf.get_list_of_pets(auth_key, filter)

    assert status == 500


def test_dont_create_pet_simple_with_negative_age(name='Потапыч', animal_type='медведь', age=-1):
    """Проверяем, что нельзя добавить питомца (без фотографии) с отрицательным возрастом,
    полагаю, что должна быть ошибка со стороны клиента - типа 400 - некорректный запрос, но точно не 200
     !!! тест провален - запрос на сервер успешный, питомец добавляется - баг"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(email, passwd)

    # Добавляем питомца без фотографии
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'name' not in result


def test_dont_add_new_pet_negative_age(name='Котейка', animal_type='кошка',
                                       age=-15, pet_photo='images/cat.jpeg'):
    """Проверяем, что нельзя добавить нового питомца с отрицательным возрастом
    полагаю, что должна быть ошибка со стороны клиента - типа 400 - некорректный запрос, но точно не 200
    !!! тест провален - запрос на сервер успешный, питомец добавляется - баг"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(email, passwd)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'name' not in result


def test_dont_create_pet_simple_with_age_in_str(name='Потапыч', animal_type='медведь', age='четыре'):
    """Проверяем, что нельзя добавить нового питомца с возрастом, заданным текстовой строкой
    !!! тест провален - запрос на сервер успешный, питомец добавляется - баг"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(email, passwd)

    # Добавляем питомца без фотографии
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'name' not in result


def test_dont_create_pet_simple_with_all_empty_data(name='', animal_type='', age=''):
    """Проверяем, что нельзя добавить нового питомца со всеми пустыми данными
    !!! тест провален - запрос на сервер успешный, питомец добавляется - баг"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(email, passwd)

    # Добавляем питомца без фотографии
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'name' not in result


def test_dont_create_pet_simple_with_long_name(name='qwertyuiop[]asdfghjkl;zxccvvbbm,./qwtwyeuritosgdhfkxcvxcnccvzbvzbvzwweerklssljhshjsshjhkshjslsjhzbxnmc,blslhjshjalhjkaiwowyikmhahjs,nm',
                                               animal_type='лиса', age='23'):
    """Проверяем, что нельзя добавить нового питомца, где имя задано очень большим кол-вом символов
    !!! тест провален - запрос на сервер успешный, питомец добавляется - баг"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(email, passwd)

    # Добавляем питомца без фотографии
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert 'name' not in result


def test_dont_update_self_pet_info_with_numbers_in_name(name='Ств531рел;(ка', animal_type='песик', age=5):
    """Проверяем невозможность обновления информации о питомце, где в имени встречаются числа и знаки
    !!! тест провален - запрос на сервер успешный, данные питомца обновляются - баг"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(email, passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 400
        assert 'name' not in result
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('There is no my pets')


def test_dont_update_self_pet_info_with_age_100_and_more(name='Стрелка', animal_type='песик', age=2000):
    """Проверяем невозможность обновления информации о питомце, где значение возраста более 100 лет
    !!! тест провален - запрос на сервер успешный, данные питомца обновляются - баг"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(email, passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 400
        assert 'name' not in result
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('There is no my pets')