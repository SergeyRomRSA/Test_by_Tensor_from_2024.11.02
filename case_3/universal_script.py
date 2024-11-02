#

from random import randint
import json

class Case3:

    version: str
    filename: str
    collection: dict
    data: list

    def __init__(self, version, filename) -> None:
        self.version = version
        self.filename = filename
        self.data = []
        self.rni = lambda: randint(0,9)
        pass

    def __call__(self):
        with open(self.filename, "r") as file:
            self.collection = json.load(file)
        
        for i in self.collection.values():
            self.data.append(self.generation_set(i))
            self.data.append(self.generation_set(i))
    
        self.data = sorted(self.data)
        print("Отсортированный список:")
        print(self.data)
        self.data = [i for i in self.data if i < self.version]
        print(f"Список меньше {self.version}:")
        print(self.data)
        pass

    #
    def generation_set(self, value: str):
        temp = value.split("*")
        value = temp[0]

        for i in temp[1:]:
            value += str(self.rni())
            value += i
        
        return value


if __name__ == "__main__":
    a = "3.4.5"
    b = "./conf.txt"
    test = Case3(a,b)
    test()
