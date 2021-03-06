#GPIO Connection Module
import pigpio

pi1 = pigpio.pi()

def DB0(state):
	pi1.write(5, int(state))
          
def DB1(state):
	pi1.write(6, int(state))

def DB2(state):
	pi1.write(13, int(state))

def DB3(state):
	pi1.write(19, int(state))

def Enable(state):
	pi1.write(17, int(state))

def Select(state):
	pi1.write(18, int(state))
	
def ALL(state):
	pi1.write(5, int(state))
	pi1.write(6, int(state))
	pi1.write(13, int(state))
	pi1.write(19, int(state))
	pi1.write(17, int(state))
	pi1.write(18, int(state))

def nibble(s, a, b, c, d):
	Enable(1)
	Select(s)
	DB0(d)
	DB1(c)
	DB2(b)
	DB3(a)
	Enable(0)



def Char(s, var):
	a = var[0]
	b = var[1]
	c = var[2]
	d = var[3]
	nibble(s, a, b, c, d)
	a = var[4]
	b = var[5]
	c = var[6]
	d = var[7]
	nibble(s, a, b, c, d)

def Text(T):
	for C in T:
		Char(1, Table[C])

def initiate():
	#Set to 4bit
	nibble(0,0,0,1,0)
	
	#set "Function Set" was auch immer
	Char(0, "00101000")
	
	#Display ON. Cursor ON, Blinkin ON
	#Char(0, "00001111")
	
	#Display ON. Cursor OFF, Blinkin OFF
	Char(0, "00001100")
	
	#entry mode
	Char(0, "00000110")
	
	#Display zurueck setzen
	ClearDisp()

def ClearDisp():
	Char(0, "00000001")

def ShiftCursor(direction, n):
	for x in range(0, n):
		if direction == "L":
			Char(0, "00010000")
		elif direction == "R":
			Char(0, "00010100")
		else:
			print("Bitte L oder R eingeben")

def ShiftDisp(direction, n):
	for x in range(0, n):
		if direction == "L":
			Char(0, "00011000")
		elif direction == "R":
			Char(0, "00011100")
		else:
			print("Bitte L oder R eingeben")
		T.sleep(0.5)

##### sign table start: #####	
Table = {' ':'00100000'}
Table['!'] = "00100001"
Table['"'] = "00100010"
Table['#'] = "00100011"
Table['$'] = "00100100"
Table['%'] = "00100101"
Table['&'] = "00100110"
Table['\''] = "00100111"
Table['('] = "00101000"
Table[')'] = "00101001"
Table['*'] = "00101010"
Table['+'] = "00101011"
Table[','] = "00101100"
Table['-'] = "00101101"
Table['.'] = "00101110"
Table['/'] = "00101111"
Table['0'] = "00110000"
Table['1'] = "00110001"
Table['2'] = "00110010"
Table['3'] = "00110011"
Table['4'] = "00110100"
Table['5'] = "00110101"
Table['6'] = "00110110"
Table['7'] = "00110111"
Table['8'] = "00111000"
Table['9'] = "00111001"
Table[':'] = "00111010"
Table[';'] = "00111011"
Table['<'] = "00111100"
Table['='] = "00111101"
Table['>'] = "00111110"
Table['?'] = "00111111"
Table['@'] = "01000000"
Table['A'] = "01000001"
Table['B'] = "01000010"
Table['C'] = "01000011"
Table['D'] = "01000100"
Table['E'] = "01000101"
Table['F'] = "01000110"
Table['G'] = "01000111"
Table['H'] = "01001000"
Table['I'] = "01001001"
Table['J'] = "01001010"
Table['K'] = "01001011"
Table['L'] = "01001100"
Table['M'] = "01001101"
Table['N'] = "01001110"
Table['O'] = "01001111"
Table['P'] = "01010000"
Table['Q'] = "01010001"
Table['R'] = "01010010"
Table['S'] = "01010011"
Table['T'] = "01010100"
Table['U'] = "01010101"
Table['V'] = "01010110"
Table['W'] = "01010111"
Table['X'] = "01011000"
Table['Y'] = "01011001"
Table['Z'] = "01011010"
Table['['] = "01011011"
Table['€'] = "01011100"
Table[']'] = "01011101"
Table['^'] = "01011110"
Table['_'] = "01011111"
Table['`'] = "01100000"
Table['a'] = "01100001"
Table['b'] = "01100010"
Table['c'] = "01100011"
Table['d'] = "01100100"
Table['e'] = "01100101"
Table['f'] = "01100110"
Table['g'] = "01100111"
Table['h'] = "01101000"
Table['i'] = "01101001"
Table['j'] = "01101010"
Table['k'] = "01101011"
Table['l'] = "01101100"
Table['m'] = "01101101"
Table['n'] = "01101110"
Table['o'] = "01101111"
Table['p'] = "01110000"
Table['q'] = "01110001"
Table['r'] = "01110010"
Table['s'] = "01110011"
Table['t'] = "01110100"
Table['u'] = "01110101"
Table['v'] = "01110110"
Table['w'] = "01110111"
Table['x'] = "01111000"
Table['y'] = "01111001"
Table['z'] = "01111010"
Table['{'] = "01111011"
Table['|'] = "01111100"
Table['}'] = "01111101"
Table['²'] = "01111110" # arrow pointing right
Table['³'] = "01111111" # arrow pointing left
Table['°'] = "11011011" # position
Table['~'] = "11111111" # FULL

##### sign table end #####
