.intel_syntax noprefix
.global _start

_start:
    mov rdi, [rsp]
    lea rsi, [rsp + 8]
    call main

    mov rdi, rax
    mov rax, 60
    syscall