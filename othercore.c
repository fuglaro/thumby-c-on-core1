#define MEM(L) (volatile unsigned int *)(L)
#define FIFOR (*MEM(0xd0000000+0x058))
#define FIFOW (*MEM(0xd0000000+0x054))
#define FIFOS (*MEM(0xd0000000+0x050))

#define SPI0 (MEM(0x4003c000))
#define SIO (MEM(0xd0000000))



// NOTE! Varaibles should only be declarted inside functions (on stack only).
// NOTE! Malloc or any kind of heap access is not supported (use stack only).



static void main(void) {
	//== Remaining bootstraping process of core1 ==
	while((FIFOS & 3) != 3){} // wait for respondable shared buffer message
	char* shared_buffer = (char*)(FIFOW = FIFOR);








	//#### Example code for Core1 ####//
	//== Functionality to run on the other core ==
	#include <stdint.h>
	uint32_t divremu(const uint32_t n, const uint32_t d, uint32_t* r) {
		*r = n % d;
		return n / d;
	}
	int i;
	while(1) {
		FIFOW = 99; // ping status code back to core0

		// Test reading and sending data back to core0 through the shared buffer
		shared_buffer[1] = shared_buffer[0];

		// Test function calls and data access
		shared_buffer[2] = divremu(11, 10, (uint32_t*)&i);
		shared_buffer[3] = i;

		// Test drawing a frame to the display
		SIO[6] = (1 << 16); // cs(0)
		SIO[5] = (1 << 17); // dc(1)
		i = 0;
		while(i<360){
			while((SPI0[3] & 2) == 0){}
			SPI0[2] = 1; // SPI0->DR = val
			i++;
		}
		SIO[6] = (1 << 17); // dc(0)

		// Test changing the display brightness from a shared buffer value
		while((SPI0[3] & 2) == 0){}
		SPI0[2] = 0x81; // SPI0->DR = BRIGHTNESS
		while((SPI0[3] & 2) == 0) {}
		SPI0[2] = shared_buffer[0]; // SPI0->DR = val
		while((SPI0[3] & 4) == 4) {i = SPI0[2];}
		while((SPI0[3] & 0x10) == 0x10) {}
		while((SPI0[3] & 4) == 4) {i = SPI0[2];}
	}
}


