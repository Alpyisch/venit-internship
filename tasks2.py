import sys
from collections import Counter

def fonk2(word):

    harf_sayaci = Counter(word)

    print(f"Kelime: {word}")
    for harf, sayi in harf_sayaci.items():
        print(f"Harf: {harf}, Sayi: {sayi}")
