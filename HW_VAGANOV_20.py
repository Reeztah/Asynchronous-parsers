class CardDeck:
    """
    Класс CardDeck представляет собой итератор колоды карт (52 штуки).

    Private Аттрибуты:
        card_suits (list): Список мастей карт.
        card_list (list): Список значений карт.

    Методы:
        __init__(): Инициализирует объект класса CardDeck.
        __next__(): Возвращает следующую карту из колоды.

    Пример использования:
        deck = CardDeck()
        print(next(deck))  # Выведет первую карту из колоды
    """

    __card_suits = ['Пики', 'Бубны', 'Червы', 'Трефы']
    __card_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']

    def __init__(self):
        self.card_iterator = [f'{card} {suit}' for card in CardDeck.__card_list for suit in CardDeck.__card_suits]
        self.iterator_index = 0

    def __next__(self):
        if self.iterator_index >= len(self.card_iterator):
            raise StopIteration('Карт в колоде больше нет')

        current_index = self.card_iterator[self.iterator_index]
        self.iterator_index += 1
        return current_index


example_carddeck = CardDeck()
print(next(example_carddeck))
print(next(example_carddeck))
print(next(example_carddeck))
print(next(example_carddeck))
print(next(example_carddeck))
#test