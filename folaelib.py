# coding=utf-8

__author__ = 'Folaefolc'
"""
Licence CC BY NC SA 4.0
"""

from itertools import chain, product
from os import path
from folaelib_plugins import *
import os, functools, platform, colorama, numpy, pickle, ast
import time, zlib, base64, hashlib, configparser, socket, sys, requests, json

GLOBALS, LOCALS = globals(), locals()
_exec = lambda c: exec(c, GLOBALS, LOCALS)
include = lambda m: _exec("{module} = __import__('{module}')".format(module=m))
__create_fake_module = lambda m: _exec("class {module}: pass".format(module=m))
__add_module_to_fake_module = lambda ms, m: _exec("class {ms}: pass\n{module}.{ms} = {ms}".format(ms=ms, module=m))

def var_exists(name):
    __exists = lambda m: _exec("try: {n} = True if {last} else True\nexcept NameError: {n} = False\nexcept: {n} = True".format(last=m, n="__lock_var_exists_or_not"))
    __exists(name); return __lock_var_exists_or_not

# not portable
ext_libs = ['PIL.Image', 'pytesseract', 'msvcrt', 'getch']
imported = []
for module in ext_libs:
    try:
        if '.' in module:
            prefix, *m = module.split('.'); prefixs = [prefix]
            if len(m) > 1: prefixs = [p for p in m[:-1]] + [prefix]
            last = prefixs.pop(0); __create_fake_module(last) if not var_exists(last) else 0
            for p in prefixs:
                __add_module_to_fake_module(p, last); last = p
        include(module); imported.append(module)
    except ImportError: pass

def check_imported(*modules):
    def decorator(function):
        def new_function(*args, **kwargs):
            ret = None
            for m in modules:
                if m not in imported:
                    ret = ImportError("{} was not imported ! Can not execute {}".format(m, function.__name__)); break
            if ret is not None: raise ret
            ret = function(*args, **kwargs)
            return ret
        functools.update_wrapper(new_function, function)
        return new_function
    return decorator

imports = [
    'zlib',  'base64',  'hashlib', 'configparser', 'sys',      'socket', 'requests', 'json',
    'chain', 'product', 'path',    'functools',    'platform', 'os',     'time',     'colorama',
    'numpy', 'pickle',  'ast'
] + imported

colorama.init()

ext_sauvegarde_fichiers = ['bak', 'bck', 'old', 'save', 'back', '~', 'sav', 'data']
ponctuation_and_spe_chars = list(" .,:!/?<>*+-'\"~&{}[]()|\\^=")
alphabet = list("abcdefghijklmnopqrstuvwxyz")
files_here_http_code = ('200', '100', '403')
refusal_chars = list("qn")
getchar = msvcrt.getch if "msvcrt" in imported else getch.getch

req = lambda r, p: requests.get(r, params=p)
exc_name = lambda e: e.__class__.__name__

def _str(s):
    try:
        return s.decode()
    except AttributeError:
        return str(s)


class ProgramArgumentError(Exception):
    pass


def info_about_pc():
    print("Machine: {} ; Ver: {} ; Platform: {} ; Proc: {} ; Node: {} ; FQDN: {}"
            .format(platform.machine(), platform.version(), platform.platform(), platform.processor(), platform.node(), socket.getfqdn()))


class Console:
    class Fore: pass
    class Back: pass
    class Style: pass
    
    def print(*args, end="\n", sep=" ", flush=False):
        for arg in args:
            print(arg, end="", flush=flush)
        print(Console.Style.RESET_ALL, end=end, flush=flush)
    
    def write(msg):
        if isinstance(msg, (list, tuple)):
            while msg:
                if _str(getchar()).lower() not in refusal_chars:
                    print("\n".join(msg[:20]))
                    for i in range(20 if len(msg) > 20 else len(msg)): msg.pop(0)
                else: break
        elif isinstance(msg, str):
            msg = msg.split("\n"); Console.write(msg)
        else: print(msg)
Console.Fore = colorama.Fore
Console.Back = colorama.Back
Console.Style = colorama.Style


def ls(directory=".", l=False, a=False, _n=20):
    files, suffixes = [f for f in os.listdir(directory) if f[0] != "."] if not a else os.listdir(directory), ["o", "Ko", "Mo", "Go", "To"]
    if l:
        Console.print("{:<28}  {:<8}    {:<8}    {}".format("Dir/file name", "Mode", "Type", "Size"))
        for name in files:
            full_path, inode, fsize, suffix = path.join(directory, name), os.stat(full_path), path.getsize(full_path), suffixes[0]
            Console.print("{:<28}".format(name), "  ", Console.Fore.YELLOW, "{:<8}".format(str(inode.st_mode)), end="    ")
            if   path.isdir(full_path): Console.print(Console.Fore.GREEN, "{:<8}".format("dir"), end="    ")
            elif path.isfile(full_path): Console.print(Console.Fore.CYAN, "{:<8}".format("file"), end="    ")
            while int(fsize) % 1024 and fsize / 1024 >= 1:
                fsize /= 1024; suffix = suffixes[suffixes.index(suffix) + 1]
            Console.print(Console.Fore.YELLOW, "{:.1f} {}".format(fsize, suffix))
    else:
        for i, name in enumerate(files):
            kind, fmt = "dir" if path.isdir(path.join(directory, name)) else "file", "{:<" + str(_n) + "}"
            Console.print(Console.Fore.GREEN if kind == "dir" else Console.Fore.CYAN, fmt.format(name), end="\n" if not (i + 1) % 4 else "")
        print()


def cwd(directory):
    os.chdir(directory)


def is_port_listened(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r = s.connect_ex(('127.0.0.1', port))
    s.close()
    return r == 0


def find_listenned_ports():
    listenned = []
    for i in range(65536):
        if is_port_listened(i):
            listenned.append(i)
    Console.write([str(i) for i in listenned])


def printProgressBar(iteration, total, prefix='', suffix='', length=100):
    # init : printProgressBar(0, 57, prefix='Progress:', suffix='Complete', length=50)
    # update : for i in range(57): printProgressBar(i + 1, 57, prefix='Progress:', suffix='Complete', length=50)
    percent = ("{0:.2f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total: print()


def bruteforce(charset, maxlength):
    return (''.join(candidate) for candidate in chain.from_iterable(product(charset, repeat=i) for i in range(1, maxlength + 1)))


def scrap_website(*args):
    args = list(args)
    wlist, exts = [], []
    spec_args = ("words", "exts")
    
    if "words" in args:
        ind = args.index("words")
        wlist_name = ""
        if len(args) > ind + 1:
            wlist_name = args[ind + 1]
        if path.exists(wlist_name):
            with open(wlist_name) as f:
                wlist = f.readlines()
        else:
            raise FileNotFoundError(wlist_name)
    if "exts" in args:
        ind = args.index("exts")
        extslist_name = ""
        if len(args) > ind + 1:
            extslist_name = args[ind + 1]
        if path.exists(extslist_name):
            with open(extslist_name) as f:
                exts = f.readlines()
        else:
            raise FileNotFoundError(extslist_name)
    
    if args:
        tested = {}
        if args[0] not in spec_args:
            addr = args[0] if args[0][-1] == "/" else args[0] + "/"
            if wlist:
                for w in wlist:
                    o = r.get(addr + w).status_code
                    if o in files_here_http_code:
                        tested[addr + w] = o
                    for e in exts:
                        o2 = r.get(addr + w + e).status_code
                        if o2 in files_here_http_code:
                            tested[addr + w + e] = o2
            else:
                chars = ''.join(chr(i) for i in range(129))
                for i in range(1, 17):
                    for attempt in bruteforce(chars, i):
                        o = r.get(addr + attempt).status_code
                        if o in files_here_http_code:
                            tested[addr + attemp] = o
                        for e in exts:
                            o2 = r.get(addr + attempt + e).status_code
                            if o2 in files_here_http_code:
                                tested[addr + attempt + e] = o2
            print("\n".join(" ".join(str(s) for s in i) for i in list(tested.items())))
        else:
            raise ProgramArgumentError
    else:
        raise ProgramArgumentError


def req_check_sc(sc, debug=False):
    if debug:
        if sc == 200:
            print("OK")
        elif sc == 301:
            print("The server is redirecting you to a different endpoint")
        elif sc == 401:
            print("You are not logged in")
        elif sc == 400:
            print("Bad request")
        elif sc == 403:
            print("Access forbidden")
        elif sc == 404:
            print("Resource not found")
        else:
            print("Unknown status code {}".format(sc))
    
    return sc == 200


def req_api(c, a={}):
    r = req(c, a) if a else req(c)
    sc = r.status_code
    if req_check_sc(sc):
        return r.json()


def get_ip(name):
    return socket.gethostbyname(name)


@check_imported('PIL.Image', 'pytesseract')
def read_text_on_image(image, lg=None):
    if isinstance(image, str):
        image = PIL.Image.open(image)
    return pytesseract.image_to_string(image, lang=lg)


def zlib_compress(msg):
    return zlib.compress(str(msg).encode())


def zlib_decompress(msg):
    return zlib.decompress(msg)


def affine_crypt(code, key, key2):
    code = code.lower()
    g = lambda x: (key * x + key2) % len(alphabet)
    crypted = []
    for c in code:
        if c not in ponctuation_and_spe_chars:
            crypted.append(alphabet[g(alphabet.index(c))])
        else:
            crypted.append(c)
    return "".join(crypted)


def affine_decrypt(code, key, key2):
    code = code.lower()
    decrypted, k = [], 0
    p = lambda _k: -(_k * key2) % len(alphabet)
    while (k * key) % len(alphabet) != 1:
        k += 1
    for c in code:
        if c not in ponctuation_and_spe_chars:
            decrypted.append(alphabet[(k * alphabet.index(c) + p(k)) % len(alphabet)])
        else:
            decrypted.append(c)
    return "".join(decrypted)


def caesar_crypt(code, key):
    if not isinstance(key, str):
        key = alphabet[key]
    key = key.lower()
    code = code.lower()
    crypted = []
    crypted_abc = alphabet[alphabet.index(key):] + alphabet[:alphabet.index(key)]
    for c in code:
        if c not in ponctuation_and_spe_chars:
            crypted.append(crypted_abc[alphabet.index(c)])
        else:
            crypted.append(c)
    return "".join(crypted)


def caesar_decrypt(code, key):
    decrypted = []
    if not isinstance(key, str):
        key = alphabet[key]
    crypted_abc = alphabet[alphabet.index(key):] + alphabet[:alphabet.index(key)]
    for c in code:
        if c not in ponctuation_and_spe_chars:
            decrypted.append(alphabet[crypted_abc.index(c)])
        else:
            decrypted.append(c)
    return "".join(decrypted)


def vigenere_crypt(code, key):
    crypted = []
    key = key.lower()
    code = code.lower()
    reformatted_key = []
    for c in key:
        if c not in reformatted_key:
            reformatted_key.append(c)
    crypted_abc = [c for c in reformatted_key]
    for c in alphabet:
        if c not in crypted_abc:
            crypted_abc.append(c)
    for c in code:
        if c not in ponctuation_and_spe_chars:
            crypted.append(crypted_abc[alphabet.index(c)])
        else:
            crypted.append(c)
    return "".join(crypted)


def vigenere_decrypt(code, key):
    decrypted = []
    reformatted_key = []
    for c in key:
        if c not in reformatted_key:
            reformatted_key.append(c)
    crypted_abc = [c for c in reformatted_key]
    for c in alphabet:
        if c not in crypted_abc:
            crypted_abc.append(c)
    for c in code:
        if c not in ponctuation_and_spe_chars:
            decrypted.append(alphabet[crypted_abc.index(c)])
        else:
            decrypted.append(c)
    return "".join(decrypted)


def dict_key_from_value(d, value):
    for k, v in d.items():
        if isinstance(v, (list, tuple)) and value in v:
            return k
        elif value == v:
            return k
    return None


def sha256(word):
    return hashlib.sha256(word.encode()).hexdigest()


def crypt_base(x, msg):
    msg = msg.encode()
    if x == 16:
        return base64.b16encode(msg)
    elif x == 32:
        return base64.b32encode(msg)
    elif x == 64:
        return base64.b64encode(msg)
    elif x == 85:
        return base64.b85encode(msg)
    else:
        raise ValueError("Unknown base : " + str(x))


def decrypt_base(x, msg):
    if x == 16:
        return base64.b16decode(msg)
    elif x == 32:
        return base64.b32decode(msg)
    elif x == 64:
        return base64.b64decode(msg)
    elif x == 85:
        return base64.b85decode(msg)
    else:
        raise ValueError("Unknown base : " + str(x))


def load_ini(path):
    c = configparser.ConfigParser()
    c.read(path)
    return c


class Switch:
    def __init__(self, kwargs):
        self.options = kwargs

    def __call__(self, value):
        o = None
        for k, v in self.options.items():
            if k(value):
                o = v(value)
                break
        return o


class NeuralNet:
    @staticmethod
    def nonlin(x, deriv=False):
        # sigmoid function
        if deriv:
            return x * (1 - x)
        return 1 / (1 + numpy.exp(-x))
    
    def __init__(self):
        # input dataset
        self.input = numpy.array([
            [0, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])
        # output dataset
        self.output = numpy.array([[0], [1], [1], [0]]).T
    
    def train(self):
        numpy.random.seed(1)
        
        # randomly initialize our weights with mean 0
        syn0 = 2 * numpy.random.random((3, 4)) - 1
        syn1 = 2 * numpy.random.random((4, 1)) - 1

        for j in range(60000):
            # Feed forward through layers 0, 1, and 2
            l0 = self.input
            l1 = NeuralNet.nonlin(numpy.dot(l0, syn0))
            l2 = NeuralNet.nonlin(numpy.dot(l1, syn1))

            # how much did we miss the target value?
            l2_error = self.output - l2
            
            if not j % 10000:
                print("Error:" + str(numpy.mean(numpy.abs(l2_error))))
                
            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            l2_delta = l2_error * NeuralNet.nonlin(l2, deriv=True)

            # how much did each l1 value contribute to the l2 error (according to the weights)?
            l1_error = l2_delta.dot(syn1.T)
            
            # in what direction is the target l1?
            # were we really sure? if so, don't change too much.
            l1_delta = l1_error * NeuralNet.nonlin(l1, deriv=True)

            syn1 += l1.T.dot(l2_delta)
            syn0 += l0.T.dot(l1_delta)

        print("Output After Training:")
        print(l1)


if __name__ == '__main__':
    ### My shell
    unimported = set(ext_libs) ^ set(imported)
    Console.print(Console.Fore.RED, "[!] ", Console.Style.RESET_ALL, "Could not import {}".format(", ".join(list(unimported)))) if unimported else 0
    _exec("cfg = {}".format(open('.folaelib.config').read())) if path.exists('.folaelib.config') else 0; cfg = {} if not var_exists("cfg") else cfg
    content, aliases, _white_list_exc = [d for d in dir() if d not in imports and d[:2] != '__' and d[-2:] != '__'], {}, ('SyntaxError')
    while True:
        Console.print(*cfg.get('input', "$ "), end=" ")
        cmd = input()
        if   cmd.strip() == ":q": break
        elif cmd.strip() == ":al": aliases = {} if not path.exists('.folaelib.aliases') and not aliases else pickle.load(open('.folaelib.aliases', 'rb'))
        elif cmd.strip() == ":as": pickle.dump(aliases, open('.folaelib.aliases', 'wb'))
        elif cmd == "help": print(
            "\t:q to quit", "\t:al to load aliases", "\t:as to save aliases",
            "\taliases is the dictionary containing your aliases (python lambda/function taking no arguments)",
            sep="\n")
        elif len(cmd) and cmd[0]:
            try:
                _exec(
"""
__temp_code = {code}
if (not isinstance(__temp_code, dict) and '{code}' not in aliases.keys()) or isinstance(__temp_code, dict): _ = __temp_code
else:
    if type(aliases['{code}']).__name__ in ('function', 'builtin_function_or_method'): _ = aliases['{code}']()
    else: _ = aliases['{code}']
print(_) if _ != None else 0
""".format(code=cmd))
            except Exception as e1:
                if exc_name(e1) not in _white_list_exc:
                    Console.print(Console.Fore.MAGENTA, "[!] ", Console.Style.RESET_ALL, "{}: {}".format(exc_name(e1), e1))
                try: _exec(cmd)
                except Exception as e2: Console.print(Console.Fore.RED, "[!] ", Console.Style.RESET_ALL, "{}: {}".format(exc_name(e2), e2))
    open('.folaelib.config', 'w').write(str(cfg))
#






