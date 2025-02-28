import msvcrt
while True:
    if msvcrt.kbhit():
        char = msvcrt.getch()
        print(char)