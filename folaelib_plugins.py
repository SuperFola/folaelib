import os


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
    os.system("git commit -m {}".format(msg))


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