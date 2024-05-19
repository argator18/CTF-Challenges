# Makefile for assembling and linking assembly code

# Define the source file and output file
SRC = your_program.asm
OUT = your_program

# Define the default target
all: $(OUT)

# Rule to assemble the source file
$(OUT): $(SRC)
	nasm -f elf64 $(SRC) -o $(OUT).o

# Rule to link the object file
	ld $(OUT).o -o $(OUT) -lc -dynamic-linker /lib64/ld-linux-x86-64.so.2


# Clean rule to remove the object file and executable
clean:
	rm -f $(OUT).o $(OUT)

