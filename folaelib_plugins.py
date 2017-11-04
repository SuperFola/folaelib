import os


class InvalidPathError(Exception): pass


def locate_and_cwd(path, portable_drive=False):
    """
    Try to find the drive on which PATH could be, then cd inside
    Raise a FileNotFoundError if the folder can not be found
    """
    hard_drives, flash_drives, located, is_dir = ['c:', 'd:'], ["{}:".format(chr(i)) for i in range(101, 123)], False, True
    p = lambda D, P: "{}{}".format(D, P) if P[0] in ('/', '\\') else "{}{}{}".format(D, os.sep, P)
    if not portable_drive:
        for drive_letter in hard_drives:
            _p = p(drive_letter, path)
            if os.path.exists(_p):
                is_dir = os.path.isdir(_p)
                if not is_dir: raise InvalidPathError
                os.chdir(_p); located = True; break
    else:
        for drive_letter in flash_drives:
            _p = p(drive_letter, path)
            if os.path.exists(_p):
                is_dir = os.path.isdir(_p)
                if not is_dir: raise InvalidPathError
                os.chdir(_p); located = True; break
    if not located: raise FileNotFoundError("Can not locate ?:{} on any drive".format(path))


def diff(file):
    "git diff FILE"
    os.system("git diff {}".format(file))


def pull():
    "git pull"
    os.system("git pull")


def push():
    "git push"
    os.system("git push")


def commit(msg):
    """
    git add .
    git commit -m MESSAGE
    """
    os.system("git add .")
    os.system("git commit -m \"{}\"".format(msg))


def stus():
    "git status -sb"
    os.system("git status -sb")


def glog(n):
    "git log --oneline -n N"
    os.system("git log --oneline -n {}".format(n))


def glogf(f):
    "git log -p FILE"
    os.system("git log -p {}".format(f))


def npp(f):
    "'C:\\Program Files (x86)\\Notepad++\\notepad++.exe' FILE"
    os.system("'C:\\Program Files (x86)\\Notepad++\\notepad++.exe' {}".format(f))


def clear():
    "cls | clear (depending on the system)"
    if os.name == 'nt': os.system("cls")
    else: os.system("clear")