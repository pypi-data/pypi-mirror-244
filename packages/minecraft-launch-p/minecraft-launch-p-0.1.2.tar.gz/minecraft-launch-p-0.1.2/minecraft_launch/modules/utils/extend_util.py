from hashlib import sha1
from shutil import rmtree
from typing import overload
from json import dump, load
from os import listdir, remove
from os.path import isfile, isdir, join, exists, getsize


class ExtendUtil():
    @staticmethod
    def to_path(raw: str) -> str:
        if(not ' ' in raw):
            return raw
        return f"\"{raw}\"" 

    @staticmethod
    def replace(raw: str, key_value_pairs: dict[str, str]) -> str:
        text: str = raw
        for i in key_value_pairs:
            text = text.replace(i, key_value_pairs[i])        
        return text
    
    @staticmethod
    def del_all_files(path: str) -> None:
        for i in listdir(path):
            if(isfile(join(path, i))):
                remove(join(path, i))
            elif(isdir(join(path, i))):
                rmtree(join(path, i))

    @staticmethod
    def beautifyjson(path: str) -> None:
        with open(path, encoding="utf-8") as f:
            json_to_dict = load(f)
        with open(path, "w", encoding='utf-8') as f:
            dump(json_to_dict,
                f,
                indent=2,
                sort_keys=True,
                ensure_ascii=False)
            
    @overload
    @staticmethod
    def verify(file: str, size: int) -> bool:...

    @overload
    @staticmethod
    def verify(file: str, shal: str) -> bool:... 

    @staticmethod
    def verify(file: str, _s: str|int) -> bool:
        if(isinstance(_s, int)):
            return exists(file) & (getsize(file) == _s)
        elif(isinstance(_s, str)):
            if(not exists(file)):
                return False
            try:
                h = sha1()
                with open(file, 'rb') as f:
                    while True:
                        b = f.read(128000)
                        h.update(b)
                        if not b:
                            break
                return _s.lower() == h.hexdigest().lower()
            except:
                return False

    @staticmethod
    def __statement() -> str: 
        return "此项目为 MinecraftLaunch 的 Python 版,负责人为 JustRainy,技术指导 YangSpring114"