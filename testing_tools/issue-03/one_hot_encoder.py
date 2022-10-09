from typing import List, Tuple
import unittest
from functools import reduce


class TestOneHotEncoding(unittest.TestCase):
    """
    Модуль для тестирования функции fit_transform, осуществляющей one hot encoding
    """

    def test_empty(self):
        with self.assertRaises(TypeError, msg='expected at least 1 arguments, got 0'):
            fit_transform()

    def test_equal_length(self):
        features = '1 2 3 4 1 2 3 1 1 3'.split()
        self.assertEqual(len(features), len(fit_transform(*features)))

    def test_one_category(self):
        features = ['one'] * 10
        res = fit_transform(*features)
        unique_ohe_values = reduce(lambda x, y: x | y, [set(code) for label, code in res])
        self.assertNotIn(0, unique_ohe_values)

    def test_iterable_arg(self):
        features = ['one', 'two', 'three', 'one', 'two', 'four']
        expected_res = [
            ('one', [0, 0, 0, 1]),
            ('two', [0, 0, 1, 0]),
            ('three', [0, 1, 0, 0]),
            ('one', [0, 0, 0, 1]),
            ('two', [0, 0, 1, 0]),
            ('four', [1, 0, 0, 0]),
        ]
        self.assertEqual(expected_res, fit_transform(features))

    def test_seq_of_args(self):
        features = ['one', 'two', 'one', 'one', 'two']
        expected_res = [
            ('one', [0, 1]),
            ('two', [1, 0]),
            ('one', [0, 1]),
            ('one', [0, 1]),
            ('two', [1, 0])
        ]
        self.assertEqual(expected_res, fit_transform(*features))


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


if __name__ == '__main__':
    from pprint import pprint

    cities = ['Moscow', 'New York', 'Moscow', 'London']
    exp_transformed_cities = [
        ('Moscow', [0, 0, 1]),
        ('New York', [0, 1, 0]),
        ('Moscow', [0, 0, 1]),
        ('London', [1, 0, 0]),
    ]
    transformed_cities = fit_transform(cities)
    pprint(transformed_cities)
    assert transformed_cities == exp_transformed_cities
