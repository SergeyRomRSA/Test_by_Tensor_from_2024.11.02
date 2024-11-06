#

import subprocess
import tempfile
import json
import zipfile
import logging
import os.path as osp
from os import walk
from datetime import datetime as dt


class Case2:

    repository: str
    relative_path: str
    version: str
    file_version: str
    extention: list
    temp_dir: str
    file_logs: str
    work_logs: logging.Logger

    def __init__(self, repository: str, relative_path: str, version: str) -> None:
        """Инициализация класса с ссылкой на репозиторий, относительным путем и версией."""
        self.repository = repository
        self.relative_path = relative_path
        self.version = version
        self.file_version = "version.json"
        self.extention = [".py", ".js", ".sh"]
        self.create_logger()

    def __call__(self) -> None:
        """Основной метод для выполнения процесса обработки репозитория."""
        self.work_logs.info("Создание временной файловой области")
        with tempfile.TemporaryDirectory() as self.temp_dir:
            self.work_logs.info(f"Скачивание репозитория {self.repository}")
            try:
                subprocess.run(["git", "clone", self.repository, self.temp_dir])
                self.work_logs.info(f"Репозиторий скачан")
                self.create_file_version()
                self.dir_to_zip()
            except subprocess.CalledProcessError as scp:
                self.work_logs.error(f"Ошибка при скачивании репозитория: {scp}")
        self.work_logs.info("Временная файловая область удалена")

    def create_file_version(self) -> None:
        """Создает файл конфигурации с версией и списком файлов."""
        self.work_logs.info(f"Создание файла конфигурации {self.file_version}")
        result = {
            "name": "hello world",
            "version": f"{self.version}",
            "files": self.filter_file_extention()
        }

        file_path = osp.join(self.temp_dir, self.relative_path, self.file_version)

        with open(file_path, "w") as file:
            # file.write(json.dumps(result))
            json.dump(result, file, ensure_ascii=False, indent=4)

        self.work_logs.info("Файл конфигурации создан")

    def filter_file_extention(self) -> list:
        """Фильтр файлов по заданным расширениям."""
        self.work_logs.info("Фильтрация файлов согласно расширению")
        array = []
        temp_path = osp.join(self.temp_dir, self.relative_path)
        
        for _, _, files in walk(temp_path):
            for file in files:
                for value in self.extention:
                    if file.endswith(value):
                        array.append(file)
        
        self.work_logs.info("Фильтрация завершена")
        return array
    
    def dir_to_zip(self) -> None:
        """Упаковка директории в zip-архив."""
        name_zip = f"{self.relative_path.split('/')[-1]}{dt.now().strftime('%d%m%Y')}.zip"
        self.work_logs.info(f"Создание архива {name_zip}")

        with zipfile.ZipFile(name_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            temp_path = osp.join(self.temp_dir, self.relative_path)
            for root, _, files in walk(temp_path):
                for file in files:
                    fp = osp.join(root, file)
                    zf.write(fp, arcname=osp.relpath(fp, start=self.temp_dir))
        
        self.work_logs.info(f"Архив создан")
    
    def create_logger(self):
        """Настройка логирования."""
        self.work_logs = logging.getLogger("case_2")
        self.work_logs.setLevel(logging.INFO)

        handler = logging.FileHandler(f"case_2.log", mode="w", encoding='utf-8')
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
