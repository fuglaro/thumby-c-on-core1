
from machine import mem32
from os import stat

_FIFO_STATUS = const(0xd0000000+0x050)
_FIFO_READ = const(0xd0000000+0x058)
_FIFO_WRITE = const(0xd0000000+0x054)
_READY_BIT = const(2)
_VALID_BIT = const(1)

_buffs = [None, None, None] # VTOR, STACK, CODE

@micropython.viper
def _buff(buffNum, size:int) -> int:
    _buffs[buffNum] = bytearray(size)
    return int(ptr8(_buffs[buffNum]))

@micropython.viper
def _ptr(buff) -> int:
    return int(ptr8(buff))

def run(binary_file, shared_buffer, stack_size=2048):
    # Prepare launchable code
    vtorptr = _buff(0, 32*4)
    stackptr = _buff(1, stack_size) + len(_buffs[1])*8
    codeptr = _buff(2, stat(binary_file)[6]) + 1
    shrdptr = _ptr(shared_buffer)
    print(f"[ocore] Executing {binary_file} on core1:")
    with open(binary_file) as f:
        f.readinto(_buffs[2])
    print(f"[ocore]  Code/Stack size (bytes): {len(_buffs[2])}/{len(_buffs[1])}")
    # Launch code
    cmd_sequence = [0, 0, 1, vtorptr, stackptr, codeptr, shrdptr]
    # multicore_launch
    for cmd in cmd_sequence:
        # multicore_fifo_drain
        while not cmd and mem32[_FIFO_STATUS] & _VALID_BIT:
            mem32[_FIFO_READ]
        # multicore_fifo_push_blocking(cmd)
        while not (mem32[_FIFO_STATUS] & _READY_BIT):
            pass
        mem32[_FIFO_WRITE] = cmd
        # multicore_fifo_pop_blocking()
        print(f"[ocore]  MSG[{cmd}]...", end="") # __sev
        while not (mem32[_FIFO_STATUS] & _VALID_BIT):
            pass
        print("OK" if mem32[_FIFO_READ] == cmd else "FAIL") # __sev




#### Example code for communicating with Core1 ####
if 1: # Test example TODO
    shared = bytearray([55, 0, 0, 0])
    run("othercore.bin", shared)
    from time import sleep
    for i in range(5):
        shared[0] = i*5
        sleep(1)
        print(f"[ocore] Response: [{mem32[_FIFO_READ] if (mem32[_FIFO_STATUS] & _VALID_BIT) else None}, {shared[1]}] -- SBuff: {list(shared)}")
    from machine import reset
    reset()