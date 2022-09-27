import json
import keyword
from typing import Union


class JSONToObject:
    """
    JSONToObject осуществляет разбор JSON-объекта (словаря) в Python-объект,
    динамически создавая атрибуты.
    При совпадении имени поля объявления с ключевыми словами Python к первому
    добавляется single trailing underscore: "class" -> "class_"
    """

    def __init__(self, description: dict) -> None:
        for field, value in description.items():
            if keyword.iskeyword(field):
                field = f'{field}_'
            self.__setattr__(field, self._field_handler(value))

    def _field_handler(self, value: Union[dict, list, int, float]):
        if isinstance(value, dict):
            return JSONToObject(value)
        elif isinstance(value, list):
            return [self._field_handler(elem) for elem in value]
        else:
            return value


class ColorizeMixin:
    repr_color_code = 33

    def __str__(self):
        return f'\033[1;{self.repr_color_code};40m{self.__repr__()}\033[0m'


class Advert(ColorizeMixin, JSONToObject):
    """
    Advert - класс, преобразующий объявление в формате JSON в объект Python,
    позволяющий получать доступ к полям через '.'.
    Поле title - обязательное для всех объявлений.
    """
    def __init__(self, description: dict) -> None:
        super().__init__(description)
        if not hasattr(self, 'price'):
            self._price = 0

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: Union[int, float]):
        if value >= 0:
            self._price = value
        else:
            raise ValueError('must be >= 0')


if __name__ == '__main__':
    lesson_str = """{
        'title': 'python', 'price': 10,
        'location': {
        'address: 'город Москва, Лесная, 7',
        'metro_stations': ['Белорусская']
        }
    }"""
    lesson = json.loads(lesson_str)

    advert = Advert(lesson)

    advert.price = 30
    print(advert)

    corgi_dict = {
        'title': 'Вельш-корги',
        'price': 1000,
        'class': 'dogs',
        'location': {
            'address': 'сельское поселение Ельдигинское, поселок санатория Тишково, 25'
        }
    }

    corgi_advert = Advert(corgi_dict)

    print(corgi_advert.price)
    print('something')
