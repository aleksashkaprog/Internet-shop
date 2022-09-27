

class StrMixin:
    """Класс миксин. Добавляет магический метод __str__ дочернему классу.
    В дочернем классе должен быть задан атрибут name"""

    def __str__(self) -> str:
        return self.name
