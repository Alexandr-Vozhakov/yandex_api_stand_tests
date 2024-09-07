# Импортируем модуль sender_stand_request, содержащий функции для отправки HTTP-запросов к API.
import sender_stand_request
#import configuration
# Импортируем модуль data, в котором определены данные, необходимые для HTTP-запросов.
import data
from pythonProject.data import user_body
from pythonProject.sender_stand_request import response


# эта функция меняет значения в параметре firstName
def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body

# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1

# Функция для негативной проверки
def negative_assert(first_name):
# В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
# В переменную user_body_response сохраняется результат запроса на создание пользователя:
    user_body_response = sender_stand_request.post_new_user(user_body)
# Проверка, что код ответа равен 400
    assert user_body_response.status_code == 400
# Проверка, что в теле ответа атрибут "code" равен 400
    assert user_body_response.json()["code"] == 400
# Проверка текста в теле ответа в атрибуте "message"
    assert user_body_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

# Ещё одна функция для негативной проверки
def negative_assert_no_first_name(user_body):
# В переменную response сохрани результат вызова функции:
    response_no_first_name = sender_stand_request.post_new_user(user_body)
# Проверка, что код ответа равен 400
    assert response_no_first_name.status_code == 400
# Проверка, что в теле ответа атрибут "code" равен 400
    assert response_no_first_name.json()["code"] == 400
# Проверка текста в теле ответа в атрибуте "message"
    assert response_no_first_name.json()["message"] == "Не все необходимые параметры были переданы"



# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2. Создание пользователя с именем, длиной в 15 символов

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

# Тест 3. Количество символов меньше допустимого (1)
# Функция для негативной проверки

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert("A")

# Тест 4. Количество символов больше допустимого (16)
# Параметр fisrtName состоит из 16 символов

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert("Aааааааааааааааа")

# Тест 5. Разрешены английские буквы (QWErty)
# Параметр fisrtName состоит из английских букв

def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Тест 6. Разрешены русские символы (Мария)
# Параметр fisrtName состоит из русских букв
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

# Тест 7. Запрещены пробелы (Человек и Ко)
# Параметр fisrtName содержит символ пробел

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert("Человек и Ко")

# Тест 8. Запрещены спецсимволы (№%@)
# Параметр fisrtName содержит спецсимволы

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert("№%@")

# Тест 9. Запрещены цифры (123)
# Параметр fisrtName содержит цифры

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert("123")

# Тест 10. Параметр firstName не передан в запросе
# В запросе нет параметра firstName

def test_create_user_no_first_name_get_error_response():
# Копируется словарь с телом запроса из файла data в переменную user_body
# Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

# Тест 11. Параметр firstName передан в запросе пустым

# В запросе значение параметра firstName в виде пустой строки
def test_create_user_empty_first_name_get_error_response():
# В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
# Проверка полученного ответа
    negative_assert_no_first_name(user_body)

# Тест 12. Параметр firstName передан в запросе другим типом данных

def test_create_user_number_type_first_name_get_error_response():
# В переменную user_body сохраняется значение 12:
    user_body = get_user_body(12)
# Сохранить результат работы в функцию
    response = sender_stand_request.post_new_user(user_body)
# Проверка полученного ответа
    assert response.status_code == 400
