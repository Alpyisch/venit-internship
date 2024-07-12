def unrpeateds(words):
    sonuc = []
    tekrar_edenler = set()
    harfler = list(words)


    for char in harfler:
        if harfler.count(char) > 1:
            tekrar_edenler.add(char)
    for char in harfler:
        if char not in tekrar_edenler:
            sonuc.append(char)
            return sonuc
        
words ="abcc"
print(unrpeateds(words))