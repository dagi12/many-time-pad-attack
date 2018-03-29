#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import string

PRINT_SET = string.printable

TARGET_CIPHER = '1ba332ddb0b5fd07b5e4a8a472175565502ea1bf34490857d6e7c7b70b924358040a48582444a892bb244326d7a5314e3d883f460aabe942472dd3df39f3f368353782b0e17f59724be0ddac8143fc08ae2bba7cd43226212af57a25a56288ca6fed2133a1fd54e8261c171823c6efd0db8f7f40f65b8fbc37e5858def0cecc06ea18dc14746afac237bd9d72b49aa37121163311b6dfeaf245ce2013b9ebcfeab24dd25b049468c051bb6ca4b519050feab295932212f5b63613182bcf510ea29e757227294dec1a3e44584847b58e6eeedda2dbcb48d695259d36e736f4a6c31671ba81f3ac770c19f63f636690a2996a634bbe164c5e26efdecdfe11b1a23daac278eb5b4ee84b9e0ace36956437b587954b97db01150cef01cfa0b958758181592416a53a099ef657e7fdfbafc582558384604bfff0f5ebfcfd16bcbf07c3b23997ae03e5ebe08ea9435c489631aae226062d9e33c352aeb692cb47d8a846bf9723eac6c56ab3e42580d30dbefde9a81a903e51e99bd28ffc49ba00d22996fa0c8dd0dd5a4a62f28d3da2207bf781901933c08a7f2e6bb52ad183dd0a6b8df4cb10f8a41498f1384b1cc5814c411cdb3f85539372f4f757a6d9da5e51ea66eb0027528dfc6caf6b710c9c16d55ecadfdd673f9fcd9'

SPACE_STRING = ' ' * 512


def str_xor(a, b):  # xor two strings (trims the longer input)
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])


def read_cipher_file(i):
    with open("xxd/dump{0}.txt".format(i), 'r') as myfile:
        return myfile.read().replace('\n', '')


def main():
    ciphers = []
    for i in range(0, 20):
        ciphers.append(read_cipher_file(i))
    final_key = [None] * 512
    for i1, txt1 in enumerate(ciphers):

        counter = collections.Counter()
        txt1_decoded = txt1.decode('hex')

        for i2, txt2 in enumerate(ciphers):
            if i1 != i2:
                txt2_decoded = txt2.decode('hex')
                txt_xored = str_xor(txt1_decoded, txt2_decoded)
                for i3, char in enumerate(txt_xored):
                    if char in PRINT_SET and char.isalpha():
                        counter[i3] += 1

        space_indexes = []
        for i, val in counter.items():
            if val > 16:
                space_indexes.append(i)
        xor_with_spaces = str_xor(txt1_decoded, SPACE_STRING)
        for i in space_indexes:
            final_key[i] = xor_with_spaces[i].encode('hex')

    final_key_hex = ''.join(val if val is not None else '00' for val in final_key)


main()
