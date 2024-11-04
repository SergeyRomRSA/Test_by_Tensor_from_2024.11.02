#

import subprocess
import tempfile
import json
import zipfile
from datetime import datetime as dt
import os.path as osp
from os import getcwd, walk

from shutil import move
class Case2:

    repository: str
    relative_path: str
    version: str
    file_version: str
    temp_dir: object

    def __init__(self, repository, relative_path, version) -> None:
        self.repository = repository
        self.relative_path = relative_path
        self.version = version
        self.file_version = "version.json"
        self.extention = {".py": -3, ".js": -3, ".sh": -3}
        pass

    def __call__(self):
        with tempfile.TemporaryDirectory() as self.temp_dir:
            subprocess.run(["git", "clone", self.repository, self.temp_dir])
            self.create_file_version()
            self.dir_to_zip()
            
    
    # Создание файла кофигурации
    def create_file_version(self):
        result = {}

        result["name"] = "hello world"
        result["version"] = f"{self.version}"
        result["files"] = self.filter_file_extention()

        file_path = osp.join(self.temp_dir, self.relative_path, self.file_version)

        with open(file_path, "w") as file:
            file.write(json.dumps(result))
    
    # Фильтр на расширение файлов
    def filter_file_extention(self):
        array = []
        temp_path = osp.join(self.temp_dir, self.relative_path)
        
        for _, _, files in walk(temp_path):
            for file in files:
                for key in self.extention.keys():
                    if key == file[self.extention[key]:]:
                        array.append(file)
        return array
    
    # Упаковка директории в архив
    def dir_to_zip(self):
        name_zip = self.relative_path[(self.relative_path.rfind("/") + 1):] + dt.now().strftime("%d%m%Y") + ".zip"
        # name_zip = osp.join(getcwd(), name_zip)
        with zipfile.ZipFile(name_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            temp_path = osp.join(self.temp_dir, self.relative_path)
            for root, _, files in walk(temp_path):
                for file in files:
                    fp = osp.join(root, file)
                    zf.write(fp, arcname=osp.relpath(fp, start=self.temp_dir))


if __name__ == "__main__":
    a = "https://github.com/paulbouwer/hello-kubernetes.git"
    b = "src/app"
    c = "3.4.5"
    test = Case2(a,b,c)
    test()
