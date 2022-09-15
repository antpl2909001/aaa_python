import string
from collections import defaultdict


class CountVectorizer:
    """
    CountVectorizer - формирует терм-документную матрицу для корпуса из текстов
    """

    def __init__(self):
        self._feature_names = []
        self._feature_counts = []

    def get_feature_names(self):
        return self._feature_names.copy()

    @staticmethod
    def _word_handler(s):
        return s.strip(string.punctuation).lower()

    def fit_transform(self, corpus):
        # словарь корпуса документов
        corpus_words_counter = defaultdict(int)
        # список словарей документов
        doc_words_counter_list = []

        for doc in corpus:
            # создаем словарь документа
            doc_words_counter_list.append(defaultdict(int))
            # обновляем счетчики слов в словаре корпуса и документа
            for word in map(self._word_handler, doc.split()):
                corpus_words_counter[word] += 1
                doc_words_counter_list[-1][word] += 1

        self._feature_names = list(corpus_words_counter.keys())

        # формируем терм-документную матрицу для корпуса
        for i, doc in enumerate(corpus):
            self._feature_counts.append([0] * len(self._feature_names))
            for j, word in enumerate(self._feature_names):
                self._feature_counts[-1][j] = doc_words_counter_list[i][word]

        return self._feature_counts.copy()


if __name__ == '__main__':
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)

    print(vectorizer.get_feature_names())
    # Out: ['crock', 'pot', 'pasta', 'never', 'boil', 'again', 'pomodoro',
    #       'fresh', 'ingredients', 'parmesan', 'to', 'taste']

    print(count_matrix)
    # Out: [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    #       [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
