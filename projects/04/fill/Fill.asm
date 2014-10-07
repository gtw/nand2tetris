// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.
	
	@KBD // load keyboard into A
	D=M // Check current keyboard signal
	@BLACK
	D;JGT
	@WHITE
	D;JEQ

(BLACK)

	@R2
	M=0

(LOOPBLACK)

	@SCREEN
	D=A
	@R2 //get current pixel
	D=D+M //store it in D
	A=D //load that location
	M=0 //set it to 0
	M=!M //then flip all bits
	@R2
	M=M+1	

	D=M //get current pixel
	@8192
	D=A-D
	@BLACKWAIT
	D;JLE

	@KBD
	D=M
	@LOOPBLACK
	D;JGT
	@WHITE
	D;JEQ

(BLACKWAIT)
	@KBD
	D=M
	@BLACKWAIT
	D;JGT
	@WHITE
	D;JEQ

	
(WHITE)

	@R2
	M=0

(WHITELOOP)

	@SCREEN
	D=A
	@R2 //get current pixel
	D=D+M //store it in D
	A=D //load that location
	M=0 //set it to 0
	@R2
	M=M+1	

	D=M //get current pixel
	@8192
	D=A-D
	@WHITEWAIT
	D;JLE

	@KBD
	D=M
	@WHITELOOP
	D;JEQ
	@BLACK
	D;JGT

(WHITEWAIT)
	@KBD
	D=M
	@WHITEWAIT
	D;JEQ
	@BLACK
	D;JGT	