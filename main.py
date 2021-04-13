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

def pause():
    os.system('pause')

def clear():
    os.system('cls')

class Category:
    def __init__(self, name: str):
        self.name = name

class Command:
    """
    ***\n
    Command(name, desc, trigger, category) -\n
    커맨드를 만듭니다.\n
    ***\n
    name - 커맨드 이름 입력 (str 타입)\n
    desc - 커맨드 설명 입력 (str 타입)\n
    argdetail - 커맨드 매개변수의 설명 입력 (list 타입)\n
    템플릿: [[Short Description, Long Description], [Short...\n
    trigger - 실행할 커맨드의 함수 입력 (function 타입)\n
    category - 커맨드 카테고리 입력 (Category 타입)\n
    stop - 이 커맨드를 입력했을 때 콘솔이 끝나게 되는지 결정 (bool 타입 - 기본 > False)\n
    ***
    """

    def __init__(self, name: str, desc: str, argdetail: list, trigger: object, category: Category = None, pause: bool = True, stop: bool = False):
        self.name = name
        self.desc = desc
        self.trigger = trigger
        self.argspec = inspect.getfullargspec(self.trigger)
        self.args = self.argspec.args
        self.argrequ = []
        self.argdisply = []
        self.argdetail = argdetail
        self.category = category
        self.pause = pause
        self.stop = stop
    
    def call(self, isPrint=True):
        self.argrequ = []
        for index, i in enumerate(self.args + [self.argspec.varargs]):
            isAnnotation = False
            isAstArg = False
            isDefault = False
            # is having type - argument
            if i in self.argspec.annotations.keys():
                isAnnotation = True
            # is having default - argument
            if i in self.args:
                if len(self.args) - len(self.argspec.defaults) > index:
                    pass
                else:
                    isDefault = True
            # is having Asteroid - argument
            if i == self.argspec.varargs:
                isAstArg = True
            # collab
            em1 = "" if isAstArg == False else "*"
            em2 = i.lower()
            em3 = "" if isAnnotation == False else f" : {self.argspec.annotations[i].__name__}"
            em4 = "" if isDefault == False else f" = {list(self.argspec.defaults)[len(self.argspec.defaults) - index]}"
            self.argdisply.append(f"{em1}[{em2}{em3}{em4}]")
            if isPrint:
                print(self.argdisply[index], end=" ")
            if isDefault or isAstArg:
                pass
            else:
                self.argrequ.append(i)

    # prevent to use: kwonlyargument
    def help(self):
        print("=" * 50)
        print(f"카테고리 \"{self.category.name}\"")
        print(self.desc)
        print()
        print(self.name.upper(), end=" ")
        if self.args != []:
            self.call()
            print("\n")
            print("*" * 50)
            print()
            for index, i in enumerate(self.args + [self.argspec.varargs]):
                if self.argdetail[index][0] != None:
                    print(f"{self.argdisply[index]} - {self.argdetail[index][0]}")
                    if self.argdetail[index][1] != None:
                        print(f"{self.argdetail[index][1]}")
                else:
                    continue
                print()
            print("*" * 50)
        else:
            print()
        print("=" * 50)

class Group:
    def __init__(self, *cmd: Command):
        self.cmd = list(cmd)

class Console:
    """
    ***\n
    Console(pack)\n
    실행 가능한 콘솔을 만듭니다.\n
    ***\n
    pack - 딕셔너리로 된 패키지를 만듭니다. \n
    패키지는 pack()으로도 제작할 수 있습니다.\n
    pack(group, version, displayInput, helpCmd, trigStart, trigEnd, trigLoop)\n
    ***\n
    group - 그룹 입력 (Group 타입)\n
    version - 버전 입력 (float 타입 - 기본 > 버전)\n
    displayInput - 입력창 옆에 표시되는 설명바 설정 (str 타입 - 기본 > ">>>")\n
    helpCmd - 도움말 명령어를 추가할 건지 설정 (bool 타입 - 기본 > True)\n
    trigStart - 최초 시작시 실행할 함수 설정 (object 타입 - 기본 > lambda: os.system("cls"))\n
    trigEnd - 종료시 실행할 함수 설정 (object 타입 - 기본 > lambda: print("종료됨"))\n
    trigLoop - 루프시 입력창 표시전 실행할 함수 설정 (object 타입 - 기본 > lambda: os.system("cls"))\n
    ***
    """
    def __init__(self, pack: dict):
        self.package: dict = pack
        self.group: Group = self.package["group"]
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
        self.displayInput: str = self.package["displayInput"]
        self.helpCmd: bool = self.package["helpCmd"]
        self.onStart: object = self.package["trigger"]["start"]
        self.onEnd: object = self.package["trigger"]["end"]
        self.onLoop: object = self.package["trigger"]["loop"]

    def sort(self, cmd, args):
        cmdStrList = []
        for i in self.group.cmd:
            cmdStrList.append(i.name)
        cmdIndex = cmdStrList.index(cmd)
        argConfig = self.group.cmd[cmdIndex]
        argCollab: list = argConfig.args + [argConfig.argspec.varargs]
        argInput = [None for i in range(len(argCollab) - 1)]
        isAssign = False
        argConfig.call(False)

        for index, i in enumerate(args):
            if i[0] != "$" and index < len(argCollab) - 1:
                if isAssign:
                    return [0, f"오류) 연산 오류 :: 대입 연산 후 일반 연산을 할 수 없습니다."]
                else:
                    argInput[index] = i
                    continue
            elif index >= len(argCollab) - 1:
                if i[0] != "$":
                    argInput.append(i)
                else:
                    return [0, f"오류) 연산 오류 :: 가변 인자에 대입 연산을 수행할 수 없습니다."]
            else:
                isAssign = True
                switch = i[1:i.index("=")]
                value = i[i.index("=") + 1:]
                if switch in argCollab:
                    if argInput[argCollab.index(switch)] == None:
                        argInput[argCollab.index(switch)] = value
                        continue
                    else:
                        return [0, f"오류) 중복된 스위치 사용 :: \"{switch}\" 스위치가 중복되어 사용되었습니다."]
                else:
                    return [0, f"오류) 잘못된 스위치 :: \"{switch}\" 스위치가 잘못되었거나 유효하지 않습니다."]
            
        
        if len(argConfig.argrequ) <= len(argCollab) - argInput.count(None) <= len(argCollab) and None not in argInput[:len(argConfig.argrequ)]:
            return [1, argInput]
        elif None in argInput[:len(argConfig.argrequ)]:
            return [0, f"오류) 인수 부족 :: \"{cmd}\" 커맨드는 {len(argConfig.argrequ)}개의 인수({(argConfig.argrequ)})가 필요합니다. ({len(argConfig.argrequ) - 1 - argConfig.argrequ.count(None)}개 입력됨)"]
        elif not (len(argConfig.argrequ) <= len(argCollab) - argInput.count(None) <= len(argCollab)):
            return [0, f"오류) 인수 부족 또는 초과 :: \"{cmd}\" 커맨드는 최소 {len(argConfig.argrequ)}개, 최대 {len(argCollab)}개의 인수가 필요합니다. ({len(argCollab) - argInput.count(None)}개 입력됨)"]

    def typeCast(self, cmd, args):
        cmdStrList = []
        for i in self.group.cmd:
            cmdStrList.append(i.name)
        cmdIndex = cmdStrList.index(cmd)
        argConfig = self.group.cmd[cmdIndex]
        argCollab: list = argConfig.args + [argConfig.argspec.varargs]
        argInput = args
        for index, i in enumerate(args):
            try:
                typeOf = argConfig.argspec.annotations[argCollab[index]]
            except KeyError:
                typeOf = None
            except IndexError:
                try:
                    typeOf = argConfig.argspec.annotations[argCollab[len(argCollab) - 1]]
                except KeyError:
                    typeOf = None
            if typeOf == None:
                argInput[index] == None
            elif typeOf == int:
                try:
                    argInput[index] = int(i)
                except ValueError:
                    return [0, f"오류) 호환되지 않는 형변환 :: 문자열 \"{i}\"는 정수와 변환 될 수 없습니다."]
            elif typeOf == float:
                try:
                    argInput[index] = float(i)
                except ValueError:
                    return [0, f"오류) 호환되지 않는 형변환 :: 문자열 \"{i}\"는 실수와 변환 될 수 없습니다."]
            elif typeOf == bool:
                if i.upper() == "FALSE":
                    argInput[index] == False
                elif i.upper() == "TRUE":
                    argInput[index] == True
                else:
                    return [0, f"오류) 호환되지 않는 형변환 :: 문자열 \"{i}\"는 True 또는 False가 아닙니다."]
        return [1, argInput]

    def input(self):
        self.content = input(f"{self.displayInput}")

    def output(self):
        if self.content != "":
            content = self.content.split()
            cmd = content[0].lower()
            args = content[1:]
            if cmd in [i.name.lower() for i in self.group.cmd] or cmd == "help":
                if cmd == "help":
                    if args != []:
                        if args[0].lower() in [i.name.lower() for i in self.group.cmd] and len(args) == 1:
                            for i in self.group.cmd:
                                if args[0].lower() == i.name.lower():
                                    i.help()
                                    pause()
                                    return True
                        elif len(args) > 1:
                            print(f"오류) 인수 초과 :: help 커맨드는 최대 1개의 인수가 필요합니다. ({len(args)}개 입력됨)")
                            pause()
                            return True
                        else:
                            print(f"오류) 잘못된 명령어 :: \"{args[0].lower()}\" 명령어는 유효하지 않습니다.")
                            pause()
                            return True
                    else:
                        av_cmd = []
                        for i in self.group.cmd:
                            av_cmd.append(i.name)
                        av_cmd.sort()
                        cate_list = {
                            "없음": []
                        }
                        cate_keys = []
                        cate_values = []
                        for i in self.group.cmd:
                            if i.category != None:
                                if i.category.name not in cate_list.keys():
                                    cate_list[i.category.name] = [i]
                                else:
                                    cate_list[i.category.name].append(i)
                            else:
                                cate_list["없음"].append(i)
                        for i in cate_list.keys():
                            cate_keys.append(i)
                        cate_keys.sort()
                        print("=================================================")
                        print("<사용 가능한 커맨드>")
                        for index, i in enumerate(av_cmd):
                            if index != len(self.group.cmd) - 1:
                                print(f"{i},", end=" ")
                            else:
                                print(f"{i}")
                        print('<커맨드 목록>')
                        print(' <커맨드> \t <설명> ')
                        for i in cate_keys:
                            print(f"- 카테고리 {i}")
                            if cate_list[i] != []:
                                for j in cate_list[i]:
                                    cate_values.append(j.name)
                                cate_values.sort()
                                for j in cate_values:
                                    def idxValue() -> int:
                                        for index, k in enumerate(cate_list[i]):
                                            if k.name == j:
                                                return index
                                    path = cate_list[i][idxValue()]
                                    print(f" {path.name} \t {path.desc} ")

                        print("=================================================")
                        print("help [커맨드]로 커맨드별 도움말 불러오기.")
                        print("=================================================")
                        pause()
                        return True
                else:
                    r_sort = self.sort(cmd, args)
                    if r_sort[0] == 0:
                        print(r_sort[1])
                        pause()
                        return True
                    else:
                        args = r_sort[1]
                    r_tcast = self.typeCast(cmd, args)
                    if r_tcast[0] == 0:
                        print(r_tcast[1])
                        pause()
                        return True
                    else:
                        args = r_tcast[1]

                    cmdStrList = []
                    for i in self.group.cmd:
                        cmdStrList.append(i.name)
                    cmdIndex = cmdStrList.index(cmd)
                    argConfig = self.group.cmd[cmdIndex]
                    for index, i in enumerate(args[len(argConfig.argrequ):len(argConfig.args)]):
                        if i == None:
                            args[len(argConfig.argrequ) + index] = argConfig.argspec.defaults[index]
                    argConfig.trigger(*args)

                    if argConfig.pause:
                        pause()

                    if argConfig.stop:
                        return False
                    else:
                        return True
            else:
                print(f"오류) 잘못된 명령어 :: \"{cmd}\" 명령어는 유효하지 않습니다.")
                pause()
                return True
        else:
            return True

    def run(self):
        if self.status:
            self.onStart()
            while self.status:
                self.onLoop()
                self.input()
                self.status = self.output()  # 리턴값으로 False를 리턴 -> 루프 종료
            self.onEnd()
            return
        else:
            return

def pack(group: Group, version: float = header["Version"], displayInput: str = ">>> ", helpCmd: bool = True,\
     trigStart: object = lambda: os.system("cls"), trigEnd: object = lambda: print("종료됨"),\
     trigLoop: object = lambda: os.system("cls")) -> dict:
    value = {
        "group": group,
        "version": version,
        "displayInput": displayInput,
        "helpCmd": helpCmd,
        "trigger": {
            "start": trigStart,
            "end": trigEnd,
            "loop": trigLoop
        }
    }
    return value

# 임시 예제

# def testobj(arg: bool, argext = 1, notarg = 1, *it: int):
#     print(f"{arg}, {argext}, {notarg}, {it}")
#     pass

# def testobj1(ar1: str, ar9: bool = True, *arg: int):
#     print(f"\"{arg}\"")
# c_zzfzz = Category("zzfzz")
# a = Command("test", "테스트 중입니다.", [["a", "arg에 대한 설명입니다."], [None, None], [None, None], ["a", None]], testobj, c_zzfzz)
# b = Command("abc", "예?", [["a", "b"], [None, None], [None, None]], testobj1, c_zzfzz)
# a_group = Group(a, b)
# package = pack(a_group, 1.0, ">>> ", True)
# consoleEx = Console(package)
# consoleEx.run()