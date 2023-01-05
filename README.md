# thumby-c-on-core1
Launch precompiled C binaries on Core1 of a Cortex-M0+ from MicroPython running on Core0

This includes a demonstration of how you can launch C code on Core1 from Thumby's MicroPython based flash, and then communicate between MicroPython on Core0 and C code on Core1 via a shared memory buffer.

The files included in this repository include the launching and bootstrapping code and also example code that uses it! The intention is for you to take this an customise it in your own code.

## Running the Example

* Open up the Thumby Code Editor at code.thumby.us.
* Load the MicroPython launcher **corelauncher.py**: FILE -> IMPORT FROM PC -> corelauncher.py
* Connect your Thumby (via USB): CONNECT THUMBY
* Upload the prebuilt example C code binary **example/othercore.bin** to your Thumby: UPLOAD -> example/othercore.bin
	* Just drop it at the root for now by selecting "\\" before hitting OK.
* Run the codelauncher with: FAST EXECUTE

The screen should show horizontal lines and increase in brightness in stages.

### What is Happening?

The MicroPython code is bootstrapping Core1 (the other core) to launch the compiled C code found in **othercore.bin**. It's the C code that is drawing the lines and making the display go brighter. Actually, to be specific, the MicroPython is sending the brightness value via a shared memory buffer that is then read by the C code to change the brightness.

You can see the C code that is being run at **othercore.c**

There also some messages being relayed between the cores via the inter-core messaging systems. Core1 is sending some debug status pings. You can see then being displayed in the Shell output in the first value of *Response* which should show *99*. The second value of *Response* is from the shared memeory buffer where the C code on Core1 is writing back a value the MicroPython code on Core0 placed in a different spot in the shared memory buffer. That shows a couple of good ways for the two cores to talk to each other.

## How does this Work?

All that's happening is that the MicroPython launcher is sending the Cortex-M0+ insttructions to initialise to some loaded binary code via directly manipluating the control registers in memory.

You can see these commands being sent to the memory registers in the Shell output *MSG* lines. The bigger MSG command values will vary but an example of the the commands are as follows:
* [0]: Bootstrapping Core 1 - lead in.
* [0]: Bootstrapping Core 1 - lead in.
* [1]: Bootstrapping Core 1 - lead in.
* [536911504]: Bootstrapping Core 1 - the memory address of the interrupt handler table (VTOR).
* [536934704]: Bootstrapping Core 1 - the memory address of the stack.
* [536912641]: Bootstrapping Core 1 - the memory address of the execution code.
* [536911232]: The memory address of the shared memory buffer (sent to the C code itself).

Interestingly, these print statements seems to be providing the equivalence of calling the SEV (send event) assembly command which gives Core1 a kick to respond. I couldn't find a better way to do the SEV as it isn't yet supported in MicroPython's asm_thumb.

The VTOR interrupt handler table is just set up empty. The stack is empty too and given a default size of 2048 bytes. You can increase this easily. The execution code is just the binary bytes from **othercore.bin** loaded straight into RAM.

## Building your own Core1 C Code

Go ahead and take a look at **othercore.c** and **corelauncher.py** which both contain example code you most likely want to customise. For **othercore.c** everything after *//#### Example code for Core1 ####//* is just to demo things. The same for everything after "#### Example code for communicating with Core1 ####" in **corelauncher.py**.

Once you have edited **othercore.c** you will need to build it with the Makefile. You can do that with the following steps:
* Get set up with a Makefile compatible development environment.
* Install the gcc Cortex-M0+ sdk. You will need the commands **arm-none-eabi-gcc** and **arm-none-eabi-objcopy**. Available. I used one from homebrew on my macos:
```
==> osx-cross/arm/arm-gcc-bin@10: stable 10.3-2021.10
Pre-built GNU toolchain for Arm Cortex-M and Cortex-R processors
https://developer.arm.com/open-source/gnu-toolchain/gnu-rm
/opt/homebrew/Cellar/arm-gcc-bin@10/10.3-2021.10_1 (6,758 files, 715.3MB) *
  Built from source on 2023-01-03 at 12:57:38
From: https://github.com/osx-cross/homebrew-arm/blob/HEAD/Formula/arm-gcc-bin@10.rb
```
* Clone this git repo!
* Then run `make` in your clone.
* You can then find your built binary at **build/othercore.bin** which you can load to your Thumby just like with **example/othercore.bin**.

Shout out and thanks to @Doogle for inspiration, and also with @Timendus for display controller manipulation example code in [thumby-grayscale library](https://github.com/Timendus/thumby-grayscale/blob/main/lib/thumbyGrayscale.py)!

