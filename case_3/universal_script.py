#

from random import randint
import json

class Case3:

    version: str
    filename: str
    collection: dict
    data: list

    def __init__(self, version: str, filename: str) -> None:
        """Инициализация класса с версией и именем файла."""
        self.version = version
        self.filename = filename
        self.data = []

    def __call__(self) -> None:
        """Основной метод для чтения данных из файла и обработки коллекции."""
        with open(self.filename, "r") as file:
            self.collection = json.load(file)
        
        for value in self.collection.values():
            self.data.append(self.generation_set(value))
            self.data.append(self.generation_set(value))
    
        self.data = sorted(self.data)
        print("Отсортированный список:")
        print(self.data)

        self.data = [i for i in self.data if i < self.version]
        print(f"Список меньше {self.version}:")
        print(self.data)
    
    @staticmethod
    def rni() -> int:
        """Генерирует случайное число от 0 до 9."""
        return randint(0,9)

    def generation_set(self, value: str) -> str:
        """Генерация "версии" по маске, добавляя случайные цифры."""
        temp = value.split("*")
        result = temp[0]

        for part in temp[1:]:
            result += str(self.rni())
            result += part
        
        return result

if __name__ == "__main__":
    a = "3.4.5"
    b = "./conf.txt"
    test = Case3(a,b)
    test()
