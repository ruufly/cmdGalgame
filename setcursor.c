#include <windows.h>
#include <stdlib.h>

void setcursor(int x, int y)
{
	SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), (COORD){ x, y });
}

int main(int argc, char* argv[])
{
    setcursor(atoi(argv[1]),atoi(argv[2]));
    return 0;
}
