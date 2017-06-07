# coding=utf-8

__author__ = 'Folaefolc'
"""
Licence CC BY NC SA 4.0
"""

import zlib
import base64
import hashlib
import configparser
import PIL.Image
import pytesseract
import socket
import sys
import requests
import json

imports = ['zlib', 'base64', 'hashlib', 'configparser', 'PIL.Image', 'pytesseract', 'sys', 'socket', 'requests', 'json']

ext_sauvegarde_fichiers = ['bak', 'bck', 'old', 'save', 'back', '~', 'sav', 'data']
ponctuation_and_spe_chars = list(" .,:!/?<>*+-'\"~&{}[]()|\\^=")
alphabet = list("abcdefghijklmnopqrstuvwxyz")


req = lambda r, p: requests.get(r, params=p)


def req_check_sc(sc):
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


if __name__ == '__main__':
    content = [d for d in dir() if d not in imports and d[:2] != '__' and d[-2:] != '__']
    while True:
        cmd = input("$ ")
        if cmd.strip() == ":q": break
        elif cmd == "help": print("Type :q to quit")
        ok = False
        for c in content:
            if cmd.find(c):
                ok = True; break
        if not ok: print("Can not find", cmd)
        else:
            try: eval("print(" + cmd + ")", globals(), locals())
            except NameError: print("Can not execute '{}'".format(cmd))