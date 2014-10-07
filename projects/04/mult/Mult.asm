// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

//To multiply we must do repeated adding
	@R2 
	M=0 //ensure R2 begins at 0
(LOOP)	
	
	@R0 // load R0 into A
	D=M // Put whatever is in R0 into D
	@END
	D;JLE //Jump to end if R0 is less than or equal to 0
	@R0 // load R0 for decrementing
	M=M-1 // R0 is decremented

	@R1 // R1 will be loaded to add to R2
	D=M // R1 is placed in D
	@R2 // prepare R2 for adding
	M=M+D //increase R2 by R1's value

	@LOOP
	0;JMP // return to top of loop

(END)
	@END
	0;JMP //infinte loop