# -*- coding: utf-8 -*-

#Michał Foryt

import random
import re
from Crypto.Util.number import GCD
from Crypto.PublicKey import RSA


def variable_random(first):
    return random.randint(1, long(first) - 1)


def complete_message(string):
    length_message = len(string)
    add_ch = 4096 - length_message
    return string + '=' * add_ch


def delete_noise(string):
    return re.sub('=*$', '', str(string))


def coprime(first, second):
    return GCD(first, second) == 1


def generate_coprime_random(message):
    generated = random.randint(0, 4096)
    while not coprime(message, generated):
        generated = random.randint(0, 4096)
    return generated


def open_key(key):
    with open(key, 'r') as key_file:
        rsa = RSA.importKey(key_file.read())
        return rsa
