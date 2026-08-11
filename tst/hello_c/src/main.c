#ifdef DEBUG
    #include <stdio.h>
    #define PRINT(...) printf(__VA_ARGS__);
#else
    #define PRINT(...)
#endif

int main(int argc, char **argv) {
    PRINT("hello c world\n")
    return 0;
}