#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import string

PRINT_SET = string.printable
KEY_LENGTH = 150
SPACE_STRING = ' ' * KEY_LENGTH

# TARGET_CIPHER_DECODED = '1ba332ddb0b5fd07b5e4a8a472175565502ea1bf34490857d6e7c7b70b924358040a48582444a892bb244326d7a5314e3d883f460aabe942472dd3df39f3f368353782b0e17f59724be0ddac8143fc08ae2bba7cd43226212af57a25a56288ca6fed2133a1fd54e8261c171823c6efd0db8f7f40f65b8fbc37e5858def0cecc06ea18dc14746afac237bd9d72b49aa37121163311b6dfeaf245ce2013b9ebcfeab24dd25b049468c051bb6ca4b519050feab295932212f5b63613182bcf510ea29e757227294dec1a3e44584847b58e6eeedda2dbcb48d695259d36e736f4a6c31671ba81f3ac770c19f63f636690a2996a634bbe164c5e26efdecdfe11b1a23daac278eb5b4ee84b9e0ace36956437b587954b97db01150cef01cfa0b958758181592416a53a099ef657e7fdfbafc582558384604bfff0f5ebfcfd16bcbf07c3b23997ae03e5ebe08ea9435c489631aae226062d9e33c352aeb692cb47d8a846bf9723eac6c56ab3e42580d30dbefde9a81a903e51e99bd28ffc49ba00d22996fa0c8dd0dd5a4a62f28d3da2207bf781901933c08a7f2e6bb52ad183dd0a6b8df4cb10f8a41498f1384b1cc5814c411cdb3f85539372f4f757a6d9da5e51ea66eb0027528dfc6caf6b710c9c16d55ecadfdd673f9fcd9'.decode('hex')
TARGET_CIPHER_DECODED = "32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904".decode(
    'hex')
known_key_positions = set()


def example_ciphers():
    c1 = "315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba50"
    c2 = "234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb741"
    c3 = "32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de812"
    c4 = "32510ba9aab2a8a4fd06414fb517b5605cc0aa0dc91a8908c2064ba8ad5ea06a029056f47a8ad3306ef5021eafe1ac01a81197847a5c68a1b78769a37bc8f4575432c198ccb4ef63590256e305cd3a9544ee41"
    c5 = "3f561ba9adb4b6ebec54424ba317b564418fac0dd35f8c08d31a1fe9e24fe56808c213f17c81d9607cee021dafe1e001b21ade877a5e68bea88d61b93ac5ee0d562e8e9582f5ef375f0a4ae20ed86e935de812"
    c6 = "32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd2061bbde24eb76a19d84aba34d8de287be84d07e7e9a30ee714979c7e1123a8bd9822a33ecaf512472e8e8f8db3f9635c1949e640c621854eba0d"
    c7 = "32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd90f1fa6ea5ba47b01c909ba7696cf606ef40c04afe1ac0aa8148dd066592ded9f8774b529c7ea125d298e8883f5e9305f4b44f915cb2bd05af513"
    c8 = "315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e941"
    c9 = "271946f9bbb2aeadec111841a81abc300ecaa01bd8069d5cc91005e9fe4aad6e04d513e96d99de2569bc5e50eeeca709b50a8a987f4264edb6896fb537d0a716132ddc938fb0f836480e06ed0fcd6e9759f404"
    c10 = "466d06ece998b7a2fb1d464fed2ced7641ddaa3cc31c9941cf110abbf409ed39598005b3399ccfafb61d0315fca0a314be138a9f32503bedac8067f03adbf3575c3b8edc9ba7f537530541ab0f9f3cd04ff503"
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]


def exercise_ciphers():
    ciphers = []
    for i in range(0, 20):
        ciphers.append(read_cipher_file(i))
        return ciphers


def str_xor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])


def read_cipher_file(i):
    with open("xxd/dump{0}.txt".format(i), 'r') as myfile:
        return myfile.read().replace('\n', '')


def main():
    ciphers = example_ciphers()
    final_key = [None] * KEY_LENGTH

    xor_with_spaces_list = [None] * len(ciphers)

    counter = [None] * len(TARGET_CIPHER_DECODED)
    for i in range(len(TARGET_CIPHER_DECODED)):
        counter[i] = collections.Counter()
    for i1, txt1 in enumerate(ciphers):

        # counter = collections.Counter()
        txt1_decoded = txt1.decode('hex')

        for i2, txt2 in enumerate(ciphers):
            # if i1 != i2:
            if i2 > i1:
                txt2_decoded = txt2.decode('hex')
                txt_xored = str_xor(txt1_decoded, txt2_decoded)
                for i3, char in enumerate(txt_xored):
                    if char in PRINT_SET and char.isalpha():
                        counter[i3][i1] += 1
                        counter[i3][i2] += 1

        xor_with_spaces_list[i1] = str_xor(txt1_decoded, SPACE_STRING)

    for i, counter_list in enumerate(counter):
        if sum(counter_list.itervalues()) > 0:
            max_index, max_value = counter_list.most_common()[0]
            if max_value > 4:
                xor_with_spaces = xor_with_spaces_list[max_index]
                final_key[i] = xor_with_spaces[i].encode('hex')
                known_key_positions.add(i)

    final_key_hex = ''.join(val if val is not None else '00' for val in final_key)
    final_key_hex_decoded = final_key_hex.decode('hex')
    output = str_xor(TARGET_CIPHER_DECODED, final_key_hex_decoded)
    print ''.join([char if char in PRINT_SET and i in known_key_positions else '*' for i, char in
                   enumerate(output)])


main()
