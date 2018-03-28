#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import collections

print_set = string.printable


# XORs two string
def strxor(a, b):  # xor two strings (trims the longer input)
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])


# 10 unknown ciphertexts (in hex format), all encrpyted with the same key


ciphers = []

for i in range(0, 20):
    with open("xxd/dump{0}.txt".format(i), 'r') as myfile:
        string = myfile.read().replace('\n', '')
        ciphers.append(string)

# The target ciphertext we want to crack
target_cipher = "1ba332ddb0b5fd07b5e4a8a472175565502ea1bf34490857d6e7c7b70b924358040a48582444a892bb244326d7a5314e3d883f460aabe942472dd3df39f3f368353782b0e17f59724be0ddac8143fc08ae2bba7cd43226212af57a25a56288ca6fed2133a1fd54e8261c171823c6efd0db8f7f40f65b8fbc37e5858def0cecc06ea18dc14746afac237bd9d72b49aa37121163311b6dfeaf245ce2013b9ebcfeab24dd25b049468c051bb6ca4b519050feab295932212f5b63613182bcf510ea29e757227294dec1a3e44584847b58e6eeedda2dbcb48d695259d36e736f4a6c31671ba81f3ac770c19f63f636690a2996a634bbe164c5e26efdecdfe11b1a23daac278eb5b4ee84b9e0ace36956437b587954b97db01150cef01cfa0b958758181592416a53a099ef657e7fdfbafc582558384604bfff0f5ebfcfd16bcbf07c3b23997ae03e5ebe08ea9435c489631aae226062d9e33c352aeb692cb47d8a846bf9723eac6c56ab3e42580d30dbefde9a81a903e51e99bd28ffc49ba00d22996fa0c8dd0dd5a4a62f28d3da2207bf781901933c08a7f2e6bb52ad183dd0a6b8df4cb10f8a41498f1384b1cc5814c411cdb3f85539372f4f757a6d9da5e51ea66eb0027528dfc6caf6b710c9c16d55ecadfdd673f9fcd9"

# To store the final key
final_key = [None] * 512
# To store the positions we know are broken
known_key_positions = set()

# For each ciphertext
for current_index, ciphertext in enumerate(ciphers):

    counter = collections.Counter()
    # for each other ciphertext
    for index, ciphertext2 in enumerate(ciphers):
        if current_index != index:  # don't xor a ciphertext with itself
            for indexOfChar, char in enumerate(strxor(ciphertext.decode('hex'), ciphertext2.decode('hex'))):
                # Xor the two ciphertexts
                # If a character in the xored result is a alphanumeric character, it means there was probably a space character in one of the plaintexts (we don't know which one)
                if char.isalpha(): counter[indexOfChar] += 1  # Increment the counter at this index
    knownSpaceIndexes = []

    # Loop through all positions where a space character was possible in the current_index cipher
    for ind, val in counter.items():
        # If a space was found at least 7 times at this index out of the 9 possible XORS, then the space character was likely from the current_index cipher!
        if val >= 7: knownSpaceIndexes.append(ind)
    # print knownSpaceIndexes # Shows all the positions where we now know the key!

    # Now Xor the current_index with spaces, and at the knownSpaceIndexes positions we get the key back!
    xor_with_spaces = strxor(ciphertext.decode('hex'), ' ' * 512)
    for index in knownSpaceIndexes:
        # Store the key's value at the correct position
        final_key[index] = xor_with_spaces[index].encode('hex')
        # Record that we known the key at this position
        known_key_positions.add(index)

# Construct a hex key from the currently known key, adding in '00' hex chars where we do not know (to make a complete hex string)
final_key_hex = ''.join([val if val is not None else '00' for val in (final_key)])
# Xor the currently known key with the target cipher
target_cipher_decoded = target_cipher.decode('hex')
final_key_hex_decoded = final_key_hex.decode('hex')
# print "Target: ", target_cipher_decoded
# print "Key: ", final_key_hex_decoded
output = strxor(target_cipher_decoded, final_key_hex_decoded)
# Print the output, printing a * if that character is not known yet
print(''.join([char if index in known_key_positions else '*' for index, char in enumerate(output)]))

# From the output this prints, we can manually complete the target plaintext from:
# The secuet-mes*age*is: Wh** usi|g **str*am cipher, nev***use th* k*y *ore than onc*
# to:
# The secret message is: When using a stream cipher, never use the key more than once

# We then confirm this is correct by producing the key from this, and decrpyting all the other messages to ensure they make grammatical sense
# target_plaintext = "The secret message is: When using a stream cipher, never use the key more than once"
# print target_plaintext
# key = strxor(target_cipher.decode('hex'),target_plaintext)
# for cipher in ciphers:
#	print strxor(cipher.decode('hex'),key)
