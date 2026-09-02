#include <stdio.h>

#ifdef DEBUG
    #define DPRINT(...) printf(__VA_ARGS__);
#else
    #define DPRINT(...)
#endif

#ifdef PLATFORM_LINUX
    int main(int argc, char **argv)
#elif PLATFORM_WINDOWS
    #include <windows.h>
    #define argc __argc
    #define argv __argv
    int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR lpCmdLine, int nCmdShow)
#endif
{
    DPRINT("hello c world\n\n")

    for (int i = 0; i < argc; i++)
        printf("Argument %i: %s\n", i, argv[i]);

    return 0;
}