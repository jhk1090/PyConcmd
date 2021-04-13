import os
import inspect

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
    Make a command.\n
    ***\n
    name - Input Command Name (str type)\n
    desc - Input Command Description (str type)\n
    argdetail - Input Command Arguments (list type)\n
    Template: [[Short Description, Long Description], [Short...
    trigger - Input Executable Function of Command (function type)\n
    category - Input Command Category (Category type)\n
    stop - Stop Loop When Input This Command (bool type - default | False)\n
    ***
    """

    def __init__(self, name: str, desc: str, argdetail: list, trigger: object, category: Category, stop: bool = False):
       self.name = name
       self.desc = desc
       self.trigger = trigger
       self.argspec = inspect.getfullargspec(self.trigger)
       self.args = self.argspec.args
       self.argrequ = []
       self.argdisply = []
       self.argdetail = argdetail
       self.category = category

    def help(self):
        print("=" * 50)
        print(f"카테고리 \"{self.category.name}\"")
        print(self.desc)
        print()
        print(self.name.upper(), end=" ")
        if self.args != []:
            for index, i in enumerate(self.args + [self.argspec.varargs] + self.argspec.kwonlyargs):
                isAnnotation = False
                isAstArg = False
                isDefaultFront = False
                isDefaultBehind = False
                if i in self.argspec.annotations.keys():
                    isAnnotation = True
                if i in self.args:
                    if len(self.args) - len(self.argspec.defaults) > index:
                        pass
                    else:
                        isDefaultFront = True
                if i in self.argspec.kwonlyargs:
                    if i in self.argspec.kwonlydefaults.keys():
                        isDefaultBehind = True
                if i == self.argspec.varargs:
                    isAstArg = True
                em1 = "" if isAstArg == False else "*"
                em2 = i.lower()
                em3 = "" if isAnnotation == False else f" : {self.argspec.annotations[i].__name__}"
                em4 = "" if isDefaultFront == False else f" = {list(self.argspec.defaults)[len(self.argspec.defaults) - index]}"
                em5 = "" if isDefaultBehind == False else f" = {self.argspec.kwonlydefaults[i]}"
                self.argdisply.append(f"{em1}[{em2}{em3}{em4}{em5}]")
                print(self.argdisply[index], end=" ")
                if isDefaultFront or isDefaultBehind:
                    pass
                else:
                    self.argrequ.append(i)
            print("\n")
            print("*" * 50)
            print()
            for index, i in enumerate(self.args + [self.argspec.varargs] + self.argspec.kwonlyargs):
                if self.argdetail[index][0] != None:
                    print(f"{self.argdisply[index]} - {self.argdetail[index][0]}")
                else:
                    continue
                if self.argdetail[index][1] != None:
                    print(f"{self.argdetail[index][1]}")
                print()
            print("*" * 50)
        else:
            pass
        print("=" * 50)
        print(self.argrequ)
        pause()

class Group:
    def __init__(self, *cmd: Command):
        self.cmd = list(cmd)

class Console:
    def __init__(self, pack: dict):
        self.package = pack
        self.group = self.package["group"]
        self.version = self.package["version"]
        self.displayInput = self.package["displayInput"]
        self.helpCmd = self.package["helpCmd"]
        self.onStart = self.package["trigger"]["start"]
        self.onEnd = self.package["trigger"]["end"]
        self.onLoop = self.package["trigger"]["loop"]

    def sort(self, cmd, args):
        cmdIndex = self.group.cmd.index(cmd)
        argConfig = self.group.cmd[cmdIndex]
        argCollab = argConfig.args + [argConfig.argspec.varargs] + argConfig.argspec.kwonlyargs
        argInput = []
        for index, i in enumerate(args):
            if i[0] != "$":
                pass

    def input(self):
        self.content = input(f"{self.displayInput}")

    def output(self):
        if self.content != "":
            content = self.content.split()
            cmd = content[0]
            args = content[1:]
            if cmd.upper() == [i.__name__.upper() for i in self.group.cmd]:
                pass
            else:
                print(f"오류: \"{cmd}\" 명령어는 등록되지 않았습니다.")
                return True
        else:
            return True

    def run(self):
        status = True
        self.onStart()
        while status:
            self.onLoop()
            self.input()
            status = self.output()  # 리턴값으로 False를 리턴 -> 루프 종료
        self.onEnd()

def pack(group: Group, version: int = 2.0, displayInput: str = ">>> ", helpCmd: bool = True,\
     trigStart: object = lambda: os.system("cls"), trigEnd: object = lambda: print("종료됨"),\
     trigLoop: object = lambda: os.system("cls"), ) -> dict:
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

def testobj(arg: int, argext = 1, *it: int, arg2 = 1, arg3: float):
    pass

c_ㅋㅋㄹㅋㅋ = Category("ㅋㅋㄹㅋㅋ")
a = Command("test", "테스트 중입니다.", [["a", "arg에 대한 설명입니다."], [None, None], ["a", None], [None, None], ["d", None]], testobj, c_ㅋㅋㄹㅋㅋ)
a.help()
a_group = Group(a)