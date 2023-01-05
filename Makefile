
all: build/othercore.bin

clean:
	rm othercore.o othercore.bin
	rmdir build

build:
	mkdir build

build/othercore.o: othercore.c build
	arm-none-eabi-gcc -mthumb -march=armv6-m -c -o build/othercore.o othercore.c

build/othercore.bin: build/othercore.o
	arm-none-eabi-objcopy -j .text -O binary build/othercore.o build/othercore.bin
	@echo
	@echo
	@echo  \ \ \ \ BINARY FILE\: build/othercore.bin
	@echo
	@echo
