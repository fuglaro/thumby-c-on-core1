
all: build/othercore.bin

clean:
	rm build/othercore.o build/othercore.bin
	rmdir build

build:
	mkdir build

build/othercore.o: othercore.c build
	arm-none-eabi-gcc -static -ffunction-sections -mthumb -march=armv6-m -pie -nostartfiles -Wl,-T linker -o build/othercore.o othercore.c

build/othercore.bin: build/othercore.o
	arm-none-eabi-objcopy -j .text -O binary build/othercore.o build/othercore.bin
	@echo
	@echo
	@echo  \ \ \ \ BINARY FILE\: build/othercore.bin
	@echo
	@echo
