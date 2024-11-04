#

from datetime import datetime, timedelta, timezone
import requests

class Case1:

    id_geo: int
    data: object

    def __init__(self, id_geo) -> None:
        self.id_geo = id_geo
        self.url = f"https://yandex.com/time/sync.json?geo={id_geo}"
        pass

    # Запрос
    def request_to_url(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.json()
            return True
        else:
            self.data = f"Ошибка при запросе: {response.status_code}"
            return False
    
    # Расчет интервала
    def calc_interval(self):
        interval = datetime.now().timestamp()
        if self.request_to_url():
            interval = self.data["time"]/1000 - interval
        else:
            interval = -1
        return interval

    # Печать в консоль данных, полученные в запросе
    def print_to_console(self):
        if self.request_to_url():
            print("Вывод в сыром виде:")
            print(self.data)
            # print("Форматированный вид:")
            # print(json.dumps(self.data, indent=2))
        else:
            print(self.data)
    
    # Вывод в консоль времени и временной зоны из запроса
    def print_time(self):
        if self.request_to_url():
            tz_geo = self.data["clocks"][f"{self.id_geo}"]["offsetString"][3:-3]
            tz_geo = timezone(timedelta(hours=int(tz_geo)))
            dt = datetime.fromtimestamp(timestamp=self.data["time"]/1000, tz=tz_geo)

            print("Время:", end="\t\t")
            print(dt.strftime("%H:%M:%S"))
            print("Временная зона:", end="\t")
            print(self.data["clocks"][f"{self.id_geo}"]["offsetString"])
        else:
            print(self.data)
    
    # Интервал
    def print_interval(self, iter=1):
        if iter < 1:
            print("Недопустимо")
        
        summa = 0
        for i in range(iter):
            temp = self.calc_interval()
            if temp == -1:
                return self.data
            else:
                summa  += temp
        
        tz_geo = timezone(timedelta(hours=0))
        dt = datetime.fromtimestamp(timestamp=summa/iter, tz=tz_geo)
        print(f"Дельта времени для серии из {iter} запроса(ов):", end="\t")

        print(dt.strftime("%H:%M:%S.%f"))


if __name__ == "__main__":
    test = Case1(123)

    # Случай A
    test.print_to_console()
    print()
    # Случай B
    test.print_time()
    print()
    # Случай C
    test.print_interval()
    print()
    # Случай D
    test.print_interval(5)


