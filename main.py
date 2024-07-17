import sys
from tasks2 import fonk2


if len(sys.argv) != 2:
    print("Kullanim: python harf_sayaci.py <alperen>")
    sys.exit(1)
fonk2(sys.argv[1]) 

