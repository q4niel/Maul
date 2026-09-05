#include <print>

inline constexpr bool kDebug =
#ifdef DEBUG
        true;
#else
        false;
#endif

#ifdef PLATFORM_LINUX
    auto main(int argc, char **argv) -> int
#elif PLATFORM_WINDOWS
    #include <windows.h>
    #define argc __argc
    #define argv __argv
    auto WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR lpCmdLine, int nCmdShow) -> int
#endif
{
    if constexpr (kDebug)
        std::println("hello c++ world\n");

    for (int i = 0; i < argc; i++)
        std::println("Argument {}: {}", i, argv[i]);

    return 0;
}