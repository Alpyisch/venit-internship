def unrepeateds(words):
    tekraredenler = set()
    sonuc = []
    for char in words:
        if char not in tekraredenler:
            tekraredenler.add(char)
            sonuc.append(char)
    return ''.join(sonuc)

words = "alperen"
print(unrepeateds(words))