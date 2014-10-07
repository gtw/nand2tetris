class Parser():
	
	def __init__(self, input_file):
		"""opens the file to be parsed, removes unnecessary
		   formatting and initializes values to be used for
		   full assembly process"""

		#file name taken from command line
		file_in = open(input_file)

		#to eventually hold the cleaned file
		clean_file = []

		#loop goes through each line of file
		for line in file_in.read().splitlines():
			#we remove tabs and spaces
			no_white = line.replace(" ","").replace("	","")
		
			comment_start = no_white.find("//")

			#if a comment is detected, we only keep the contents of the line prior to the comment
			if comment_start != -1:
				no_white = no_white[0:comment_start]
			
			#at this point if we have a non-empty line we write it to the file with a new-line character		
			if len(no_white) > 0:
				clean_file.append(no_white)

		#the file is closed
		file_in.close()

		#clean_file is added to the parser object
		self.clean_file = clean_file

		self.current_command = ""
		self.current_command_num = 0

	def hasMoreCommands(self):
		if self.current_command_num >= len(self.clean_file):
			return 0
		else:
			return 1

	def advance(self):
		#if more commands available, load the next one
		#increment the counter of commands

		if self.hasMoreCommands():
			self.current_command = self.clean_file[self.current_command_num]	
		self.current_command_num = self.current_command_num + 1

	def commandType(self):
		if self.current_command[0] == "@":
			return "A_COMMAND"
		elif self.current_command[0] == "(":
			return "L_COMMAND"
		else:
			return "C_COMMAND"

	#will need to implemented later
	def symbol(self):
		if self.commandType() not in ("A_COMMAND","L_COMMAND"):
			print "SYMBOL CALLED ON COMPUTATION COMMAND"
			return "ERROR"

		if self.current_command[0]=="@":
			return self.current_command[1:]
		else:
			return self.current_command.replace("(","").replace(")","")

	def dest(self):
		if self.commandType() != "C_COMMAND":
			print "DEST CALLED ON NON-C COMMAND"
			return "ERROR"

		#either the command sets no values, in which case return NULL
		#or we simply take all text leading up to the equals sign
		equal_loc = self.current_command.find("=")
		if equal_loc<0:
			return "NULL"
		else:
			return self.current_command[0:equal_loc]

	def comp(self):
		
		if self.commandType() != "C_COMMAND":
			print "COMP CALLED ON NON-C COMMAND"
			return "ERROR"

		#since = and ; are indicators of the kind of command,
		#we merely check for their presence and then take text
		#occuring on either side of them. Note if = is missing all
		#characters starting at 0 are computation characters,
		#and if ; is missing all characters until the end of the command
		#are computation characters

		equal_loc = self.current_command.find("=")
		semi_loc = self.current_command.find(";")

		if equal_loc < 0:
			if semi_loc < 0:
				return self.current_command
			else:
				return self.current_command[0:semi_loc]
		else:
			if semi_loc < 0:
				return self.current_command[equal_loc+1:]
			else:
				return self.current_command[equal_loc+1:semi_loc]


	def jump(self):
		if self.commandType() != "C_COMMAND":
			print "JUMP CALLED ON NON-C COMMAND"
			return "ERROR"

		# either there's no semicolon and hence no jump, or we
		# return all characters after the semicolon
		# e.x. AD=A+D;JMP would just pass JMP

		semi_loc = self.current_command.find(";")
		if semi_loc<0:
			return "NULL"
		else:
			return self.current_command[semi_loc+1:]

class Code():

	"""Code objects merely hold various functions to compose
	commands into binary equivalents"""

	def __init__(self):

		#All information stored in a dict, this object is basically a collection
		#of lookup tables and easy functions for navigating them.

		self.dest_dict = {"M":"001",
						  "D":"010",
						  "MD":"011",
						  "A":"100",
						  "AM":"101",
						  "AD":"110",
						  "AMD":"111",
						  "NULL":"000"
						 }

		self.jump_dict = {"JGT":"001",
						  "JEQ":"010",
						  "JGE":"011",
						  "JLT":"100",
						  "JNE":"101",
						  "JLE":"110",
						  "JMP":"111",
						  "NULL":"000"
						  }

		self.comp_dict = {"0":"101010",
						  "1":"111111",
						  "-1":"111010",
						  "D":"001100",
						  "A":"110000",
						  "!D":"001101",
						  "-A":"110011",
						  "D+1":"011111",
						  "A+1":"110111",
						  "D-1":"001110",
						  "A-1":"110010",
						  "D+A":"000010",
						  "D-A":"010011",
						  "A-D":"000111",
						  "D&A":"000000",
						  "D|A":"010101"
						  }

	def dest(self,string):
		return self.dest_dict.get(string,"NO SUCH DEST")


	def comp(self,string):

		#look for M in string to know how to set first bit right away
		if string.find("M")>0:
			a = "1"
		else:
			a = "0"

		#only commands with A are encoded in dictionary, Ms must therefore be switched
		string = string.replace("M","A")
		c = self.comp_dict.get(string,"NO SUCH COMP")

		return a+c

	def jump(self,string):
		return self.jump_dict.get(string,"NO SUCH JUMP")

parse = Parser(".\sample_code.txt")
code  = Code()
while parse.hasMoreCommands():
	parse.advance()
	print parse.current_command
	print "111",code.comp(parse.comp()),code.dest(parse.dest()),code.jump(parse.jump())