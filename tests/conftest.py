import json
import pytest
import requests
from api import PetFriend

from settings import email, passwd
import os

pf = PetFriend()


"""Фикстура получает ключ авторизации с валидными данными"""
@pytest.fixture(scope='class', autouse=True)
def get_auth_key():
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в auth_key
    status, auth_key = pf.get_api_key(email=email, password=passwd)

    """Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key"""
    assert status == 200, 'Запрос на получение ключа выполнен успешно'
    assert 'key' in auth_key, 'Ключ авторизации получен'

    return auth_key


"""Фикстура удаляет тестовые данные (созданных в процессе тестирования питомцев)  после прохождения тестов"""
@pytest.fixture(autouse=True)
def delete_test_pets(get_auth_key):
    yield
    while True:
        _, my_pets = pf.get_list_of_pets(get_auth_key, 'my_pets')
        if len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, _ = pf.delete_pet(get_auth_key, pet_id)
        else:
            break
