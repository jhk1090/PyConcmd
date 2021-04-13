import os
import inspect

header = {
    "By": "Jhk_",
    "Identifier": "ConCmd",
    "Version": 1.0,
    "BackCompatible": [
        True, 1.0
    ],  # 하휘호환 범위 (지정 ~ 이 버전), 하휘호환 가능
    "Langauge": "Ko-KR"
}

self.version: float = self.package["version"]
self.status: bool = None
if type(self.version) != str:
    if header["BackCompatible"][0] and header["BackCompatible"][1] <= self.version <= header["Version"]:
        self.status = True
    else:
        self.status = False
        clear()
        print("오류) 호환 오류 :: 이 버전 \"{}\"이 다른 버전과 호환되지 않거나, 이 버전과 \"{}\" 버전이 호환되지 않습니다.".format(header["Version"], self.version))
        pause()
else:
    self.status = False
    clear()
    print("오류) 호환 오류 :: 시험 버전은 호환되지 않습니다.")
    pause()
    
# Test #2
