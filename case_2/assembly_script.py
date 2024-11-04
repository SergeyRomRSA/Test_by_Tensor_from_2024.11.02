#

import subprocess
import tempfile
import json
import zipfile
from datetime import datetime as dt
import os.path as osp
from os import walk
import logging

class Case2:

    repository: str
    relative_path: str
    version: str
    file_version: str
    file_logs: str
    temp_dir: object
    work_logs: object

    def __init__(self, repository, relative_path, version) -> None:
        self.repository = repository
        self.relative_path = relative_path
        self.version = version
        self.file_version = "version.json"
        self.extention = {".py": -3, ".js": -3, ".sh": -3}
        self.create_logger()
        pass

    def __call__(self):
        self.work_logs.info("Создание временной файловой области")
        with tempfile.TemporaryDirectory() as self.temp_dir:
            self.work_logs.info(f"Скачивание репозитория {self.repository}")
            subprocess.run(["git", "clone", self.repository, self.temp_dir])
            self.work_logs.info(f"Репозиторий скачан")
            self.create_file_version()
            self.dir_to_zip()
        self.work_logs.info("Временная файловая область удалена")
        pass
            
    # Создание файла кофигурации
    def create_file_version(self):
        self.work_logs.info(f"Создание файла конфигурации {self.file_version}")
        result = {}

        result["name"] = "hello world"
        result["version"] = f"{self.version}"
        result["files"] = self.filter_file_extention()

        file_path = osp.join(self.temp_dir, self.relative_path, self.file_version)

        with open(file_path, "w") as file:
            file.write(json.dumps(result))

        self.work_logs.info("Файл конфигурации создан")
        pass
    
    # Фильтр на расширение файлов
    def filter_file_extention(self):
        self.work_logs.info("Фильтрация файлов согласно расширению")
        array = []
        temp_path = osp.join(self.temp_dir, self.relative_path)
        
        for _, _, files in walk(temp_path):
            for file in files:
                for key in self.extention.keys():
                    if key == file[self.extention[key]:]:
                        array.append(file)
        
        self.work_logs.info("Фильтрация окончена")
        return array
    
    # Упаковка директории в архив
    def dir_to_zip(self):
        name_zip = f"{self.relative_path[(self.relative_path.rfind('/') + 1):]}{dt.now().strftime('%d%m%Y')}.zip"
        # name_zip = osp.join(getcwd(), name_zip)
        self.work_logs.info(f"Создание архива {name_zip}")

        with zipfile.ZipFile(name_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            temp_path = osp.join(self.temp_dir, self.relative_path)
            for root, _, files in walk(temp_path):
                for file in files:
                    fp = osp.join(root, file)
                    zf.write(fp, arcname=osp.relpath(fp, start=self.temp_dir))
        
        self.work_logs.info(f"Архив создан")
    
    # Настройка логирования
    def create_logger(self):
        self.work_logs = logging.getLogger("case_2")
        self.work_logs.setLevel(logging.INFO)

        handler = logging.FileHandler(f"case_2_logs.log", mode="w", encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        self.work_logs.addHandler(handler)

        self.work_logs.info("Настроено логирование...")



if __name__ == "__main__":
    a = "https://github.com/paulbouwer/hello-kubernetes.git"
    b = "src/app"
    c = "3.4.5"
    test = Case2(a,b,c)
    test()
