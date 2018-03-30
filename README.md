# Attacking A Many Time Pad - Cryptography

This code investigates the properties of the one time pad - specifically that it can easily be broken if the same key is used more than once!

Given 10 ciphertexts encrypted using the same key, we can break the encryption, and generate all the plaintexts

XOR pairwise:
1. \\x00 -> both ciphers was the same
2. Space -> case flipped character
3. Uppercase letter:
   - space xor lowercase letter (same)
   - punctuation xor lowercase letter
4. Lowercase letter:
   - space xor uppercase letter
4. Numeric, Punctutation
   - different letters, different case
5. Control chars
   - different letters, same case

~~Rewrite and understand~~
~~2. Mini example~~
~~3. Rady z goo.gl/HvjcXp
 - Those two cases should be pretty easy to tell apart. Furthermore, in the first case, you can easily get the actual characters at that position in all the plaintexts just by flipping the case of all the letters you obtained by XORing the ciphertexts together.
 - Fill in letters
 - debug 4,5 -> thm, the~~
4. Python 3
5. Work on bytes
6. Language booster
7. Polskie znaki