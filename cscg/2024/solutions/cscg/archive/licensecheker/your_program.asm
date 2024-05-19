section .data
    format db "%x", 10, 0     ; Format string for printf, including newline

section .text
    global _start
    extern printf

_start:
    ; Your number to print is stored in RAX
    mov rax, 123               ; Example number to print
    mov     eax, 0x40024fa5
    ror     eax, 0x15

    ; Setup for calling printf
    mov rdi, format            ; First argument: format string
    mov rsi, rax               ; Second argument: number to print (from RAX)
    xor rax, rax               ; Clear RAX to indicate no floating point arguments

    ; Call printf
    call printf

    ; Exit
    mov rax, 60                ; syscall for exit
    xor rdi, rdi               ; Status 0
    syscall


