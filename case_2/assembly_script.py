#

import subprocess
import tempfile
import json
import zipfile
from datetime import datetime as dt
import os.path
from os import getcwd, walk

from shutil import move
class Case2:

    repository: str
    relative_path: str
    version: str
    local_path: str
    file_version: str

    def __init__(self, repository, relative_path, version) -> None:
        self.repository = repository
        self.relative_path = ("" if relative_path[0]== "/" else "/") + relative_path
        self.version = version
        self.local_path = getcwd() + "/temp"
        self.file_version = "/version.json"
        self.extention = {".py": -3, ".js": -3, ".sh": -3}
        pass

    def __call__(self):
        self.selection_repository()
        self.create_file_version()
        self.dir_to_zip()
        pass

    #
    def selection_repository(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(["git", "clone", self.repository, temp_dir])
            move((temp_dir + self.relative_path), (self.local_path + self.relative_path))
    
    #
    def create_file_version(self):
        result = {}

        result["name"] = "hello world"
        result["version"] = f"{self.version}"
        result["files"] = self.filter_file_extention()

        with open(self.local_path + self.relative_path + self.file_version, "w") as file:
            file.write(json.dumps(result))
    
    #
    def filter_file_extention(self):
        temp = []
        
        for _, _, files in walk(self.local_path + self.relative_path):
            for file in files:
                for key in self.extention.keys():
                    if key == file[self.extention[key]:]:
                        temp.append(file)
        return temp
    
    #
    def dir_to_zip(self):
        name_zip = self.relative_path[(self.relative_path.rfind("/") + 1):] + dt.now().strftime("%d%m%Y") + ".zip"
        with zipfile.ZipFile(name_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in walk(self.local_path):
                for file in files:
                    fp = os.path.join(root, file)

                    zf.write(fp, arcname=os.path.relpath(fp, start=self.local_path))


if __name__ == "__main__":
    a = "https://github.com/paulbouwer/hello-kubernetes.git"
    b = "src/app"
    c = "3.4.5"
    test = Case2(a,b,c)
    test()
