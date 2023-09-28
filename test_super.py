from api import PetFriends
import os
import string
import random

valid_email = 'shkolyar1@gmail.com'
valid_password = 'shkolyar1'

#  генерация рандомной стоки в разном регистре с цифрами, param: k= указать длину строки
ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=256))

#  генерация рандомной последовательности чисел param: range(указать кол-во последовательности)
sequence = int(''.join(random.choice('0123456789') for _ in range(1000)))

pf = PetFriends()


def test_get_api_key_for_invalid_user(email: str = 'shkolyar1@gmail.com', password: str = valid_password):
    """Проверяем запрос с невалидным email и с валидным password.
    Проверяем нет ли ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result, 'Ключ отсутствует в ответе'


def test_get_api_key_for_invalid_password(email: str = valid_email, password: str = 'Password12345'):
    """Проверяем запрос с невалидным password и с валидным email.
    Проверяем нет ли ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result, 'Ключ отсутствует в ответе'


def test_update_self_pet_invalid_name_str(name: str = ran, animal_type: str = 'Dog', age: int = 17):
    """Проверка с негативным сценарием.
    Поле имя не должно принимать на ввод более 255 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['name']) <= 255, 'Допустимая длина строки 255 символов'

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Моих питомцев нет")


def test_update_self_pet_invalid_name_int(name: int = 4, animal_type: str = 'Dog', age: int = 10):
    """Проверка с негативным сценарием.
    Поле имя не должно принимать цифры в любом виде"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200, имя питомца указано в буквенном значении
        assert status == 200
        assert result['name'].isalpha(), 'Имя животного не может быть цифрой'
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Моих питомцев нет")


def test_update_self_pet_invalid_animal_type(name: str = 'Борис', animal_type: str = ran, age: int = 5):
    """Проверка с негативным сценарием.
     Поле порода не должно принимать на ввод более 255 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['animal_type']) <= 255, 'Допустимая длина строки 255 символов'

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Моих питомцев нет"")


def test_update_self_pet_invalid_age(name: str = 'Борис', animal_type: str = 'обезьяна', age: int = 8):
    """Проверка с негативным сценарием.
    Поле возраст не должно принимать более двух цифр в возрасте питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['age']) < 3, 'Возраст животного не может быть трехзначной цифрой'

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")




def test_update_self_pet_photo_png(pet_photo: str = 'images/owl.png'):
    """Проверка с позитивным сценарием.
    Возможность обновления фото в формате png"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200, 'Формат png не поддерживается'
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Моих питомцев нет"")


def test_update_self_pet_invalid_animal_type_int(name: str = 'Печалька', animal_type: int = 5, age: int = 10):
    """Проверка с негативным сценарием.
      Поле порода не должно принимать цифры в любом виде"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200, вид питомца указано в буквенном значении
        assert status == 200
        assert result['animal_type'].isalpha(), 'Поле порода не должно содержвть цифр'
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Моих питомцев нет"")
