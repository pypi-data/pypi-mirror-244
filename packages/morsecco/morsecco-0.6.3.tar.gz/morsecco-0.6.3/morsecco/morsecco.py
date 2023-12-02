#!/usr/bin/env python3

# morsecco is a minimalistic, but mighty programming language using morse code as source code

import sys, re, os, rlcompleter

sys.path.append(os.path.dirname(__file__))
from alphabet import morsecodes
from mC import Cell, ExecutionPointer, Cellstorage, Cellstack, int2code, code2int, subroutine, error, initGlobals
import mC

def goto():
	address = mC.addressstack.pop()
	mC.ep = address.getExecutionPointer()
	while (mC.ep.generation > 0):
		mC.ep.generation -= 1
		for address in mC.addressstack.getAll():
			if (address.size() > 0 and address.content[0] == ' '):
				address.content = address.content[1:]
			else:
				error("leaving command with local address in stack.")
		parent = mC.storage.getChild('')
		if (parent):
			mC.storage = parent
		else:
			error("returning from orphan storage.")

def execute():
	while (not mC.err):
		#try:
			#print(f"executing at #{mC.ep.position} in {mC.storage.getContent(mC.ep.id)}")
			command = mC.ep.getToken()
			#print(f"»{command}«")
			if mC.storage.getMode(command) == '-..-': # eXecute mode overwrites build-in commands
				subroutine(command)
			elif mC.storage.getMode(command) == '.-..' and not mC.storage.isFile(command):
				subroutine(command)
			elif (command == '--.-' or command == chr(0)): # Quit or end of current code
				if ((mC.ep.id != '' or mC.storage.getChild('')) and mC.addressstack.size()):
					# we are in a subroutine and the tos could be a return address
					goto()
				else:
					break
			elif (command == ''): # ignore an empty command
				pass

			elif (command == '....'): # Help
				try:
					topic = mC.ep.getToken()
					if (topic == chr(0) or topic == '\n'):
						topic = ''
					helpfile = open(os.path.dirname(__file__) + '/help.txt')
					text = helpfile.read()
					print(re.sub(r"(?s)\n\n.*", '', re.sub(r"(?s).*?\n" + topic.replace('.', '\\.') + "\n", '', text, 1)))
				except:
					error(f"could not open help file")
				
			elif (command == '.'): # Enter cell
				token = mC.ep.getToken()
				if (len(token)):
					mC.stack.push(Cell(token))
				else:	# if . is followed by double space, enter until double space
					text = ''
					while ((token := mC.ep.getToken()) != ''):
						text = text + token + ' '
					mC.stack.push(Cell(text.strip()))

			elif (command == '-'): # Transform the stack: swap, copy or delete items
				positions = Cell(mC.ep.getToken())
				if (positions.content == ''): # For empty subcommand (double space after -)
					positions = mC.stack.pop() # take command list from stack instead
				while (positions.len()):
					nextToken = positions.getToken()
					if (nextToken == ''):
						pass
					else:
						pos = code2int(nextToken)
						if (not '-' in nextToken):
							mC.stack.roll(nextToken.count('.'))
						elif (pos > 0): # copy item to the top the stack
							mC.stack.pick(pos - 1)
						elif (pos < 0): # negative numbers delete items; beware to start with upmost
							mC.stack.delete(- pos - 1)
						else:
							error("this should never happen")

			elif (command == '.-..'): # Length
				mC.stack.push(Cell(int2code(len(mC.stack.pop().content))))

			elif (command == '-.-.'): # Cut/Concatenate
				positions = Cell(mC.ep.getToken())
				if (positions.content == ''): # For empty subcommand (double space after -)
					positions = mC.stack.pop() # take command list from stack instead
				while (positions.len()):
					nextToken = positions.getToken()
					pos = code2int(nextToken)
					tos = mC.stack.pop()
					if (not '-' in nextToken): # join two stack items with zero, one or more spaces
						mC.stack.push(mC.stack.pop().append(Cell(nextToken.replace('.',' ')[1:]).append(tos)))
					elif (abs(pos) > tos.len()):
						error(f"cannot cut »{tos.content}« at {pos}.")
					elif (pos > 0):
						mC.stack.push(Cell(tos.content[pos:]))
						mC.stack.push(Cell(tos.content[:pos]))
					elif (pos < 0):
						pos = tos.len() + pos;
						mC.stack.push(Cell(tos.content[:pos]))
						mC.stack.push(Cell(tos.content[pos:]))
					else:
						error("this should never happen")

			elif (command == '..-'): # Use address as File, Stack, whatever
				subcommand = mC.ep.getToken()
				if (subcommand == ''):
					error("Use command does currently not support an empty subcommand.")
				elif (subcommand == '..-.'): # use as File handle
					filename = mC.ep.getToken()
					handle = mC.stack.pop().content
					if (filename == ""):
						filename = mC.stack.pop().content
					filename = filename.replace('- ','/').replace('. ',' ')
					mC.storage.createFile(handle, filename)
				elif (subcommand == '-.-.'): # Close
					handle = mC.stack.pop().content
					if (mC.storage.isFile(handle)):
						if (mC.storage.files[handle] != ""):
							mC.storage.files[handle].close()
						del mC.storage.files[handle]
						del mC.storage.modes[handle]
						#mC.storage.cells.pop(handle) why not leave the filename for later reuse
					else:
						error(f"File {handle} was not open.")
				elif (subcommand == '-..'): # Delete
					target = mC.stack.pop().content
					if (mC.storage.isFile(target)):
						filename = mC.storage.getContent(target)
						try:
							os.remove(filename)
						except:
							error(f"failed to remove file »{filename}«.")
					elif (mC.storage.exists(target)):
						del mC.storage.cells[target]
				elif (subcommand == '--'): # Move in file
					handle = mC.stack.pop().content
					if (mC.storage.isFile(handle)):
						file = mC.storage.fileHandle(handle)
						if (file == ''): # not yet open
							try:
								file = open(mC.storage.getContent(handle), 'r')
								mC.storage.setFileHandle(handle, file)
							except:
								error(f"could not open file »{mC.storage.getContent(handle)}« for »{handle}«.")
						seek = mC.stack.pop().content
						try:
							if (seek == '...'): # Start
								file.seek(0)
							elif (seek == '..-.'): # Finish
								file.seek(0, whence = 2)
							else:
								file.seek(code2int(seek), whence = 1)
						except:
							error(f"unable to Move »{seek}« in file »{handle}«.")
					else:
						error(f"no open file for »{handle}«.")
				else:
					mC.storage.setMode(mC.stack.pop().content, subcommand)

			elif (command == '.--'): # Write to memory/file
				mC.storage.write(mC.stack.pop().content, mC.stack.pop())

			elif (command == '.-.'): # Read from memory/file
				mC.stack.push(mC.storage.read(mC.stack.pop().content))

			elif (command == '---'): # Output cell content with newline
				print(mC.stack.pop().content)

			elif (command == '-.-'): # Konvert
				subcommand = mC.ep.getToken()
				tos=mC.stack.pop()
				text = ''
				if (subcommand == '-'): # to Text
					while (tos.len()):
						code = code2int(tos.getToken())
						if (code >= 0):
							text += chr(code)
						else:
							error(f"Failing to convert {code} to a unicode char.")
				elif (subcommand == '-.'): # to Number string
					while (tos.len()):
						token = tos.getToken()
						if (token == ''):
							text += ' '
						else:
							text += str(code2int(token)) + ' '
					text = text.strip()
				elif (subcommand == '--'): # to Morse code
					lowercase = False
					morselist = list(morsecodes.keys())
					charlist = list(morsecodes.values())
					while (tos.len()):
						token = tos.getToken()
						if (token == ''):
							text += ' '
						else:
							code = code2int(token)
							if (code < 0):
								error(f"Failing to convert negativ code {code} to a morse letter.")
							else:
								if (chr(code).isalpha()):
									if (chr(code).isupper() == lowercase):
										text += '---- '
										lowercase = not lowercase
									token = int2code(ord(chr(code).upper()))
								if (token in charlist):
									text += morselist[charlist.index(token)] + ' '
								else:
									text += token + ' '
					text = text.strip()
				elif (subcommand == '.-'): # from text
					for char in tos.content:
						text += int2code(ord(char)) + ' '
					text = text.strip()
				elif (subcommand == '.-.'): # from number
					while (tos.len()):
						token = tos.getToken(clean=True)
						text += int2code(int(token)) + ' '
					text = text.strip()
				elif (subcommand == '.--'): # from Morse code
					lowercase = False
					while (tos.len()):
						token = tos.getToken(clean=True)
						if (token == ''):
							text += ' '
						elif (token == '----'): # officially CH, here: Case Hack
							lowercase = not lowercase
						elif (token in morsecodes.keys()):
							for element in morsecodes[token].split(' '):
								if (code2int(element) < 0):
									error(f"The morse table is messed with negative code »{element}«.")
									text += element + ' '
								else:
									char = chr(code2int(element))
									if (lowercase):
										text += int2code(ord(char.lower())) + ' '
									else:
										text += element + ' '
						elif (code2int(token) > 0):
							text += token + ' '
						else:
							error(f"No idea how to convert token {token} ({code2int(token)}) to unicode.")
					text = text[:len(text)-1]
				mC.stack.push(Cell(text))

			elif (command == '.-'): # Add
				mC.stack.push(mC.stack.pop().add(mC.stack.pop()))

			elif (command == '-...'): # Binary NAND
				op = mC.ep.getToken()
				mC.stack.push(mC.stack.pop().binary(mC.stack.pop(), op))

			elif (command == '--'): # Mark position (put ep on return stack)
				target = mC.ep.copy()
				target.back() # now pointing to the mark command itself
				offset = mC.ep.getToken()
				if (offset == ''): # Move address stack pointer to pattern given by tos
					pointer = mC.addressstack.pop().getExecutionPointer()
					pointer.search(mC.stack.pop().content)
					mC.addressstack.push(Cell(pointer.toCode()))
				elif (not '-' in offset): # number of dots gives address to drop
					mC.addressstack.delete(offset.count('.') - 1)
				else:
					skips = code2int(offset)
					while (skips < 0):
						target.back()
						skips += 1
					while (skips > 1): # skip one means address of the Mark command
						target.getToken()
						skips -= 1
					mC.addressstack.push(Cell(target.toCode()))

			elif (command == '--.'): # Go to position given by top of address stack
				goto()

			elif (command == '--..'): # Zero-skip (skip commands, if tos is 0 or empty)
				stoptoken = mC.ep.getToken()
				topcell = mC.stack.pop()
				newcell = topcell.copy()
				token = ''
				if newcell.len():
					token = newcell.getToken()
				if token == '':
					while (mC.ep.getToken() != stoptoken):
						pass
					if newcell.len():
						mC.stack.push(newcell) # leave the rest of the cell on the stack
				elif code2int(token):
					mC.stack.push(topcell) # be polite and leave it on the stack
				else:
					while (mC.ep.getToken() != stoptoken):
						pass
					if (newcell.len()): # the cell contains more
						mC.stack.push(newcell) # be polite and leave the rest on the stack

			elif (command == '-..-'): # eXecute top cell as code
				code = mC.stack.pop().content
				if (code == '-..-'): # execute -..- means recurse
					command = mC.ep.id
				elif (code == '.-'): # execute Again
					command = code
				else:
					command = '.-' # use unaccessible address .- as storage
					mC.storage.cells[command] = Cell(code)
				mC.addressstack.push(Cell(mC.ep.toCode())) # place return address on the address stack
				mC.ep = ExecutionPointer(command) # execute 
				
			elif (command == '...-.'): # (verified) print stack and storage
				print('===')
				mC.stack.trace()
				if (mC.addressstack.size()):
					print('===')
					mC.addressstack.trace()
				print(':::')
				mC.storage.print()

			elif (mC.storage.exists(command)):
				subroutine(command)
		#except:
			#error("uncaught error.")
			#break

def interactive():
	while (True):
		try:
			script = input('> ') + '\n'
			if (script == '--.-\n'):
				break
			previously = rootstorage.cells[''].content
			mC.ep = ExecutionPointer(position = len(previously), id='')
			mC.storage = rootstorage
			rootstorage.cells.update({'': Cell(previously + script)})
			execute()
			mC.err = False
		except EOFError as e:
			print(' Bye!')
			break

usage='Usage: morsecco [-f scriptfile] [-r cellfile] [script] [-i]\n\
with any number of scriptfiles and scripts.\n\
Options:\n\
-f scriptfile  executes the contents of scriptfile\n\
-r cellfile    read the contents of cellfile to the stack\n\
-q             quite mode to suppress error messages by empty error handler\n\
-i             enter interactive mode\n\
-h             show this help\n\
-v             show version'

rootstorage = Cellstorage()
mC.initGlobals(rootstorage)

def main():
	#storage = rootstorage
	#stack = Cellstack()
	#addressstack = Cellstack()
	#ep = ExecutionPointer('')
	
	args=sys.argv[1:]
	if (len(args) == 0): # without arguments, enter interactive mode
		print('Thank you for entering morsecco ' + chr(0x1F37E) + ' interactive mode. Type .... for Help. Leave with --.-')
		interactive()
		sys.exit()
	
	while (len(args)):
		if (args[0] == '-h'):
			print(usage)
			sys.exit()
		elif (args[0] == '-v'):
			print('morsecco programming language v0.6.2 -- with dot, dash and space around the world')
			sys.exit()
		elif (args[0] == '-q'): # quite = empty error handler
			rootstorage.cells.update({'.': Cell('')})
		elif (args[0] in ['-f','-r']): # script file or to read to the stack
			if (len(args) > 1):
				try:
					file = open(args[1], 'r', encoding='utf-8')
					code = file.read()
					file.close()
				except:
					print(f"Error: could not read from file »{args[1]}«")
					sys.exit()
				if (args[0] == '-f'):
					rootstorage.cells.update({'': Cell(rootstorage.cells[''].content + code)})
				else:
					mC.stack.push(Cell(code))
				args = args[1:] # remove argument
			else:
				print('option -f requires a filename as argument')
				sys.exit()
		elif (args[0] == '-i'): # mixed interactive mode
			interactive()
		else: # if it's no option, it's a script!
			rootstorage.cells.update({'': Cell(rootstorage.cells[''].content + args[0] + '\n')})
		args = args[1:]
	execute()

if __name__ == "__main__":
    main()
