#include <stdio.h>

#ifdef DEBUG
    #define PRINT(...) printf(__VA_ARGS__);
#else
    #define PRINT(...)
#endif

int main(int argc, char **argv) {
    PRINT("hello c world\n\n")

    for (int i = 0; i < argc; i++) {
        printf("Argument %i: %s\n", i, argv[i]);
    }

    return 0;
}