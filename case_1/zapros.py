#

from datetime import datetime, timedelta, timezone
import requests

class Case1:

    id_geo: int
    data: dict

    def __init__(self, id_geo: int) -> None:
        """Инициализация класса."""
        self.id_geo = id_geo
        self.url = f"https://yandex.com/time/sync.json?geo={id_geo}"


    def request_to_url(self) -> bool:
        """GET-запрос и сохранение данных в атрибуте data."""
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.data = response.json()
                return True
            else:
                self.data = f"Ошибка при запросе: {response.status_code}"
                return False
        except requests.exceptions.RequestException as reRE:
            self.data = f"Ошибка запроса: {str(reRE)}"
            return False

    def calc_interval(self) -> float:
        """Расчет интервала времени с момента запроса."""
        current_timestamp = datetime.now().timestamp()
        if self.request_to_url():
            return self.data["time"]/1000 - current_timestamp
        return -1

    def print_to_console(self) -> None:
        """Печать в консоль данных в сыром виде."""
        if self.request_to_url():
            print("Вывод в сыром виде:")
        print(self.data)
    
    def print_time(self) -> None:
        """Вывод в консоль времени и временной зоны из запроса."""
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
    
    def print_interval(self, iterations: int = 1) -> None:
        """Cредний интервал времени для заданного количества запросов."""
        if iterations < 1:
            print("Недопустимо")
            return
        
        total_interval = 0
        for _ in range(iterations):
            interval = self.calc_interval()
            if interval == -1:
                return self.data
            total_interval  += interval
        
        average_interval = total_interval / iterations
        tz_geo = timezone(timedelta(hours=0))
        dt = datetime.fromtimestamp(average_interval, tz=tz_geo)
        print(f"Дельта времени для серии из {iterations} запроса(ов):", end="\t")
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


