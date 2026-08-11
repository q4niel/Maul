#include <print>

inline constexpr bool kDebug =
#ifdef DEBUG
        true;
#else
        false;
#endif

auto main(int argc, char **argv) -> int {
    if constexpr (kDebug)
        std::println("hello c++ world");
    return 0;
}