import sys
from collections import defaultdict

def fonk2(word):
    word = sys.argv[1].upper()

    harf_sayaci = defaultdict(int)
    for harf in word:
        if harf != " ":
            harf_sayaci[harf] += 1

    Kelimeler = word.split()
    print(f"Kelime: {Kelimeler}")
    print(len(Kelimeler))
    for harf, sayi in harf_sayaci.items():
        print(f"Harf: {harf}, Sayi: {sayi}")
        