# Testsript display
# to run: exec(open("/home/pi/Desktop/DisplayScript/DisScri.py").read())

import time as T

import pygame, sys
import pygame.locals

import random

print(T.ctime())

response = input("Do you want to use Emulator only? y/n")
EmuOnly = 0

print("--- --- --- --- --- --- ---")
print("Type Game() to start a Game")
print("--- --- --- --- --- --- ---")

if response == 'n':
	import GPIOcom as GPcom
	EmuOnly = 0
elif response == 'y':
	import AsciiTable as GPcom
	EmuOnly = 1
else:
	print ("Nope")
	sys.exit()


#pi1 = pigpio.pi()

#Array that is rendered while playing
Screen = {}

#Array for mine positions and counters
Mines = {}

#Cursor-Array [row, column, stroed sign]
Cursor = [1,1, '~']

def Start(ImageTable, windowSurface):
	#create the 4 rows
	for x in range(0, 4):
		Screen['R'+str(x+1)] = {}
		for y in range(0, 20):
			Screen['R'+str(x+1)]['Z'+str(y+1)] = '~'
	
	#Startposition
	#Screen['R1']['Z1'] = 'position'
	
	#create mines
	for x in range(0, 4):
		Mines['R'+str(x+1)] = {}
		for y in range(0, 20):
			Mines['R'+str(x+1)]['Z'+str(y+1)] = random.choice(["0","0","0","0","0","0","X"])
	
	#generate numbers around mines
	Row = 1
	MineStore = {}
	m = 0
	for r in range(0, 4):
		Cell = 1
		for z in range(0, 20):
			if Mines['R'+str(Row)]['Z'+str(Cell)] == "X":
				### Zellen Berechnen ###
				### N Zelle ###
				if Row != 1 and Mines['R'+str(Row - 1)]['Z'+str(Cell)] != "X":
					counter = int(Mines['R'+str(Row - 1)]['Z'+str(Cell)]) + 1
					Mines['R'+str(Row - 1)]['Z'+str(Cell)] = str(counter)
				### S Zelle ###
				if Row != 4 and Mines['R'+str(Row + 1)]['Z'+str(Cell)] != "X":
					counter = int(Mines['R'+str(Row + 1)]['Z'+str(Cell)]) + 1
					Mines['R'+str(Row + 1)]['Z'+str(Cell)] = str(counter)
				### W Zelle ###
				if Cell != 1 and Mines['R'+str(Row)]['Z'+str(Cell - 1)] != "X":
					counter = int(Mines['R'+str(Row)]['Z'+str(Cell - 1)]) + 1
					Mines['R'+str(Row)]['Z'+str(Cell - 1)] = str(counter)
				### E Zelle ###
				if Cell != 20 and Mines['R'+str(Row)]['Z'+str(Cell + 1)] != "X":
					counter = int(Mines['R'+str(Row)]['Z'+str(Cell + 1)]) + 1
					Mines['R'+str(Row)]['Z'+str(Cell + 1)] = str(counter)
				### NW Zelle ###
				if Row != 1 and Cell != 1 and Mines['R'+str(Row - 1)]['Z'+str(Cell - 1)] != "X":
					counter = int(Mines['R'+str(Row - 1)]['Z'+str(Cell - 1)]) + 1
					Mines['R'+str(Row - 1)]['Z'+str(Cell - 1)] = str(counter)
				### NE Zelle ###
				if Row != 1 and Cell != 20 and Mines['R'+str(Row - 1)]['Z'+str(Cell + 1)] != "X":
					counter = int(Mines['R'+str(Row - 1)]['Z'+str(Cell + 1)]) + 1
					Mines['R'+str(Row - 1)]['Z'+str(Cell + 1)] = str(counter)
				### SW Zelle ###
				if Row != 4 and Cell != 1 and Mines['R'+str(Row + 1)]['Z'+str(Cell - 1)] != "X":
					counter = int(Mines['R'+str(Row + 1)]['Z'+str(Cell - 1)]) + 1
					Mines['R'+str(Row + 1)]['Z'+str(Cell - 1)] = str(counter)
				### SE Zelle ###
				if Row != 4 and Cell != 20 and Mines['R'+str(Row + 1)]['Z'+str(Cell + 1)] != "X":
					counter = int(Mines['R'+str(Row + 1)]['Z'+str(Cell + 1)]) + 1
					Mines['R'+str(Row + 1)]['Z'+str(Cell + 1)] = str(counter)
				
			Cell += 1
		Row += 1
		
	#Alle Nullen durch leer ersetzen
	Row = 1
	for r in Mines.values():
		Cell = 1
		for z in r.values():
			if Mines['R'+str(Row)]['Z'+str(Cell)] == "0":
				Mines['R'+str(Row)]['Z'+str(Cell)] = " "
			Cell += 1
		Row += 1
	
	#render Start screen
	render(GSScreen, ImageTable, windowSurface)
	
	#wait a second
	T.sleep(2)
	
	Cursor = [1,1, '°']
	render(Screen, ImageTable, windowSurface)

def AlterSign(screen, row, pos, sign):
	screen['R'+str(row)]['Z'+str(pos)] = sign
			
def AlterRow(screen, row, content):
	z = 1
	for c in content:
		screen['R'+str(row)]['Z'+str(z)] = c
		if z == 20:
			break
		z += 1

def render(element, ImageTable, windowSurface):
	#clear game screen
	windowSurface.blit(ImageTable['BackGround'], (0,0))
	
	#Zeile 1 Rendern
	z = 1
	while z < 21:
		#search through the Table dictionary and return the ascii-code for a special character
		ascii = GPcom.Table[element['R1']['Z'+str(z)]]
		
		#function to render the character to the hardware screen
		if EmuOnly == 0:
			GPcom.Char(1, ascii)
		
		#render the character to the Emulator                      
		windowSurface.blit(ImageTable[ascii], (14+((z-1)*36),16))
		
		z +=1
	#Zeile 3 Rendern
	z = 1
	while z < 21:
		ascii = GPcom.Table[element['R3']["Z"+str(z)]]
		if EmuOnly == 0:
			GPcom.Char(1, ascii)
		windowSurface.blit(ImageTable[ascii], (14+((z-1)*36),124))
		z +=1
	#Zeile 2 Rendern
	z = 1
	while z < 21:
		ascii = GPcom.Table[element['R2']["Z"+str(z)]]
		if EmuOnly == 0:
			GPcom.Char(1, ascii)
		windowSurface.blit(ImageTable[ascii], (14+((z-1)*36),70))
		z +=1
	#Zeile 4 Rendern
	z = 1
	while z < 21:
		ascii = GPcom.Table[element['R4']["Z"+str(z)]]
		if EmuOnly == 0:
			GPcom.Char(1, ascii)
		windowSurface.blit(ImageTable[ascii], (14+((z-1)*36),178))
		z +=1
	#refreshes the Emulator screen
	pygame.display.flip()

#function to move the cursor around (triggered by the arrow-keys in the Game-Loop)		
def MoveCursor(direction, ImageTable, windowSurface):
	
	#writes the stored position to the field that was hidden by the cursor
	Screen['R' + str(Cursor[0])]['Z'+str(Cursor[1])] = Cursor[2]
	
	if direction == 'D':
		if Cursor[0] == 4:
			Cursor[0] = 1
		else:
			Cursor[0] +=1
	if direction == 'U':
		if Cursor[0] == 1:
			Cursor[0] = 4
		else:
			Cursor[0] -=1
	if direction == 'L':
		if Cursor[1] == 1:
			Cursor[1] = 20
		else:
			Cursor[1] -=1
	if direction == 'R':
		if Cursor[1] == 20:
			Cursor[1] = 1
		else:
			Cursor[1] +=1
	
	#Stores the character that is now hidden by the cursor
	Cursor[2] = Screen['R' + str(Cursor[0])]['Z'+str(Cursor[1])]
	
	Screen['R' + str(Cursor[0])]['Z'+str(Cursor[1])] = '°'
	render(Screen, ImageTable, windowSurface)

##### MAIN MENU SCREEN #####

MMScreen = {}
for x in range(0, 4):
	MMScreen['R'+str(x+1)] = {}
	for y in range(0, 20):
		MMScreen['R'+str(x+1)]['Z'+str(y+1)] = '_'

#replace specific parts with other characters
AlterRow(MMScreen, 1, '--Choose an option--')
AlterRow(MMScreen, 2, '²1.  Play MineDigger')
AlterRow(MMScreen, 3, '²2.  Play TexVenture')
AlterRow(MMScreen, 4, '²ESC to Exit        ')



##### GAME START SCREEN ####

#write an array full of underscores
GSScreen = {}
for x in range(0, 4):
	GSScreen['R'+str(x+1)] = {}
	for y in range(0, 20):
		GSScreen['R'+str(x+1)]['Z'+str(y+1)] = '_'
AlterRow(GSScreen, 2, '_GAME START')
AlterRow(GSScreen, 3, '_MINEDIGGER')


##### GAME OVER SCREEN #####

GOScreen = {}
for x in range(0, 4):
	GOScreen['R'+str(x+1)] = {}
	for y in range(0, 20):
		GOScreen['R'+str(x+1)]['Z'+str(y+1)] = '_'
AlterRow(GOScreen, 2, '_GAME OVER')
AlterRow(GOScreen, 4, '_______RESTARTING...')

#reveal a field
def dig(ImageTable, windowSurface):
	#check if you did not hit a mine
	if Mines["R" + str(Cursor[0])]["Z" + str(Cursor[1])] != 'X':
		#overwirtes a part of the Screen-Array with the Mines-Array
		Screen["R" + str(Cursor[0])]["Z" + str(Cursor[1])] = Mines["R" + str(Cursor[0])]["Z" + str(Cursor[1])]
		#updates the Cursor storage with the revealed field
		Cursor[2] = Screen['R' + str(Cursor[0])]['Z'+str(Cursor[1])]
		
		#if the field i completely empty
		if Mines["R" + str(Cursor[0])]["Z" + str(Cursor[1])] == ' ':
			#automatically reveal the surrounding fields
			reveal(Cursor[0], Cursor[1])			
		render(Screen, ImageTable, windowSurface)
	else:
		render(GOScreen, ImageTable, windowSurface)
		T.sleep(2)
		Start(ImageTable, windowSurface)

#reveal is a subfunction of dig() to reveal around an empty field
def reveal(x, y):
	### reveal N ###
	if x != 1:
		Screen["R" + str(x-1)]["Z" + str(y)] = Mines["R" + str(x-1)]["Z" + str(y)]
	### reveal S ###
	if x != 4:
		Screen["R" + str(x+1)]["Z" + str(y)] = Mines["R" + str(x+1)]["Z" + str(y)]
	### reveal W ###
	if y != 1:
		Screen["R" + str(x)]["Z" + str(y-1)] = Mines["R" + str(x)]["Z" + str(y-1)]
	### reveal E ###
	if y != 20:
		Screen["R" + str(x)]["Z" + str(y+1)] = Mines["R" + str(x)]["Z" + str(y+1)]
	### reveal NW ###
	if x != 1 and y != 1:
		Screen["R" + str(x-1)]["Z" + str(y-1)] = Mines["R" + str(x-1)]["Z" + str(y-1)]
	### reveal NE ###
	if x != 1 and y != 20:
		Screen["R" + str(x-1)]["Z" + str(y+1)] = Mines["R" + str(x-1)]["Z" + str(y+1)]
	### reveal SW ###
	if x != 4 and y != 1:
		Screen["R" + str(x+1)]["Z" + str(y-1)] = Mines["R" + str(x+1)]["Z" + str(y-1)]
	### reveal SE ###
	if x != 4 and y != 20:
		Screen["R" + str(x+1)]["Z" + str(y+1)] = Mines["R" + str(x+1)]["Z" + str(y+1)]






#Story screen
StoryScreen = {}
for x in range(0, 4):
	StoryScreen['R'+str(x+1)] = {}
	for y in range(0, 20):
		StoryScreen['R'+str(x+1)]['Z'+str(y+1)] = ' '

def LoadStoryContent(filename):
	with open(filename) as f:
		StoryContent = f.readlines()
		return StoryContent

def StartStory(ImageTable, windowSurface, StoryContent):
	Index = 0
	for c in StoryContent:
		print(c)
	for i in range(0, 4):
		AlterRow(StoryScreen, Index+1, StoryContent[Index][4:])
		Index += 1
	render(StoryScreen, ImageTable, windowSurface)
	return [4, 4]
		
def ScrollUp(StoryIndex):
	if StoryIndex[1] == 5:
		print("scrolling up")
		CopyRow(StoryScreen, "R2", "R1")
		CopyRow(StoryScreen, "R3", "R2")
		CopyRow(StoryScreen, "R4", "R3")
		StoryIndex[1] = 4
	else:
		pass
	return StoryIndex

def CopyRow(Screen, SourceRow, TargetRow):
	Screen[TargetRow] = {}
	Screen[TargetRow].update(Screen[SourceRow])
	

def ClearRows():
	for x in range(0, 4):
		StoryScreen['R'+str(x+1)] = {}
		for y in range(0, 20):
			StoryScreen['R'+str(x+1)]['Z'+str(y+1)] = ' '

def GetCase(StoryIndex, StoryContent):
	a = StoryContent[StoryIndex[0]].index('[') + 1
	b = StoryContent[StoryIndex[0]].index(']')
	Case = StoryContent[StoryIndex[0]][a:b]
	return Case


def GetLine(StoryIndex, StoryContent):
	b = StoryContent[StoryIndex[0]].index(']')
	Line = str(StoryContent[StoryIndex[0]][b+2:-2])
	return Line

#reading the next line and deciding what to do
def NextLine(ImageTable, windowSurface, StoryIndex, StoryContent):	
	Case = GetCase(StoryIndex, StoryContent)
	print(Case)
	while Case == "I":
		StoryIndex[0] += 1
		Case = GetCase(StoryIndex, StoryContent)
		print(Case)
	
	while Case == 'M':
		StoryIndex[0] += 1
		Case = GetCase(StoryIndex, StoryContent)
		print(Case)
	
	#Clear screen case
	if Case == 'L':
		ClearRows()
		StoryIndex[1] = 1
	
	#Read line case
	elif Case == 'R':
		StoryIndex = ScrollUp(StoryIndex)
		Line = GetLine(StoryIndex, StoryContent)
		print ( "Line: " + Line)
		AlterRow(StoryScreen, StoryIndex[1], Line)
		StoryIndex[1] += 1
	
	elif Case == "yn":
		Line = GetLine(StoryIndex, StoryContent)
		print(Line)
		StoryIndex = ScrollUp(StoryIndex)
		c = Line.index(';')
		
		#read textmark-links
		yes = Line[2:c]
		print('YES == ' + yes)
		no = Line[c+3:Line.index('}')]
		print('NO == ' + no)
		
		#prepare vars to remember lines
		MarkYes = 0
		MarkNo = 0
		
		# morph StoryIndex to a list to save some information to jump to the right place in the storyline
		#['type', ChoiceYes, ChoiceNo, choosen]
		StoryIndex = ['yn',0,0,0]
		
		x = 0
		#search through Content for textmarks and identify matching to yes
		for L in StoryContent:
			Type = L[L.index('['):L.index(']')+1]
			if Type == '[M]':
				print (L)
				MarkName = L[L.index('{')+1:L.index('}')]
				print ('found ' + MarkName + ' in line ' + str(x+1))
				if MarkName == yes:
					print('found YES')
					StoryIndex[1] = x
					StoryIndex[3] = x
			x += 1
			
		x = 0
		#search through Content for textmarks and identify matching to no
		for L in StoryContent:
			Type = L[L.index('['):L.index(']')+1]
			if Type == '[M]':
				print (L)
				MarkName = L[L.index('{')+1:L.index('}')]
				print ('found ' + MarkName + ' in line ' + str(x+1))
				if MarkName == no:
					print('found NO')
					StoryIndex[2] = x
			x += 1
		
		global GameType
		GameType = 'TVClosedQuestion'
		#printing answers
		Answersline = Line[Line.index('}')+2:]
		print(Answersline)
		AlterRow(StoryScreen, 4, Answersline)
		
		#creating left Arrow
		AlterSign(StoryScreen, 4, 1, '²')
		
		render(StoryScreen, ImageTable, windowSurface)
		return StoryIndex
	
	#End of story case
	elif Case == 'E':
		StoryIndex = 'END'
		return StoryIndex
	else:
		pass	
	render(StoryScreen, ImageTable, windowSurface)
	StoryIndex[0] += 1
	return StoryIndex

def cycletime(ctime, maxfps):
	# 1s = 1000ms = 1000µs
	# µs per frame
	limit = 1 / maxfps * 1000 #min limit in ms
	current = T.time() - ctime
	wait = limit - current *1000
	#print('Limit: ' + str(limit)[:8] + 'ms | Current: ' + str(current * 1000)[:8] + 'ms | Wainting- ' + str(wait)[:8] +'ms')
	T.sleep(wait/1000)
	
GameType = ''	

# ----- ----- ----- GAME ----- ----- ----- #
def Game():
	pygame.init()
	
	#limits to 60 cycles per second
	fpslimit = 60
	
	global GameType
	GameType = 'MainMenu'
	
	#Creating Game/ProgrammWindow
	BLACK = (0,0,0)
	WIDTH = 740
	HEIGHT = 240
	windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
	windowSurface.fill(BLACK)
	
	#List for StoryContent and Index
	#StoryIndex = 0
	#StoryContent = []
	
	#Set LCD Emulator Folder
	# EmuFolder = Workfolder + 'LCD_Emulator/'
	EmuFolder = 'LCD_Emulator/'
	
	#Loading Background to ImageTable
	ImageTable = {'BackGround':pygame.image.load(EmuFolder + 'LCD_Images/LCD_Emu.png')}
	
	#Loading ASCII signs to image table based on Table{}
	for i in GPcom.Table.values():
		ImageTable[str(i)] = pygame.image.load(EmuFolder + 'LCD_Images/' + i +'.png')

	#Give ingame key information in console
	print("1. press I to initiate the hardware display")
	print("2. press RETURN to reveal a Field")
	print("3. press M to show mines")
	print("4. press R to hide mines")
	print("5. use arrow keys to navigate")
	print("6. press ESC to quit the game")
	print("--- --- --- --- --- --- --- ---")
	print("You'll need to initiate the hardware display at least once")
	print("to re-initiate press I twice")
	

	#Setting ingame Background
	windowSurface.blit(ImageTable['BackGround'], (0,0))
	
	#update the Game-Screen
	pygame.display.flip()

	#render MainMenu screen
	render(MMScreen, ImageTable, windowSurface)
	#Gameloop (Mainly Key-Bindings)
	while True:
		event = pygame.event.poll()
		if GameType == 'MainMenu':
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_1):
				GameType = 'MineDigger'
				Start(ImageTable, windowSurface)
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_2):
				GameType = 'TexVenture'
				StoryContent = LoadStoryContent('./StoryFiles/Terraforming.txt')
				StoryIndex = StartStory(ImageTable, windowSurface, StoryContent)
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
				if EmuOnly == 0:
					GPcom.ClearDisp()
				pygame.quit()
				break
		elif GameType =='MineDigger':
			#arrow key controls
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_UP):
				MoveCursor('U', ImageTable, windowSurface)
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_DOWN):
				MoveCursor('D', ImageTable, windowSurface)
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT):
				MoveCursor('L', ImageTable, windowSurface)
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT):
				MoveCursor('R', ImageTable, windowSurface)
			
			#reveal a field
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
				dig(ImageTable, windowSurface)	
			
			#show mines
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m):
				render(Mines, ImageTable, windowSurface)
			
			#re-render the screen
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
				render(Screen, ImageTable, windowSurface)
			
			#ESC to Exit MineDigger
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
				GameType = 'MainMenu'
				render(MMScreen, ImageTable, windowSurface)
		elif GameType =='TexVenture':
			#Next line with RETURN
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
				if str(StoryIndex[0]).isdigit():
					StoryIndex = NextLine(ImageTable, windowSurface, StoryIndex, StoryContent)
				elif StoryIndex == 'END':
					GameType = 'MainMenu'
					render(MMScreen, ImageTable, windowSurface)
			
			#ESC to Exit TexVenture
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
				GameType = 'MainMenu'
				render(MMScreen, ImageTable, windowSurface)
		
		#Yes or NO question for TexVenture
		elif GameType == 'TVClosedQuestion':
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT):
				AlterSign(StoryScreen, 4, 1, '²')
				AlterSign(StoryScreen, 4, 20, ' ')
				#alter the choosen story index
				StoryIndex[3] = StoryIndex[1]
				#render new arrow position
				render(StoryScreen, ImageTable, windowSurface)
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT):
				AlterSign(StoryScreen, 4, 1, ' ')
				AlterSign(StoryScreen, 4, 20, '³')
				#alter the choosen story index
				StoryIndex[3] = StoryIndex[2]
				#render new arrow position
				render(StoryScreen, ImageTable, windowSurface)		
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
				StoryIndex = [StoryIndex[3], 1]
				ClearRows()
				GameType = 'TexVenture'
				StoryIndex = NextLine(ImageTable, windowSurface, StoryIndex, StoryContent)
			
			#ESC to Exit TexVenture
			if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
				GameType = 'MainMenu'
				render(MMScreen, ImageTable, windowSurface)
		
		#clear screen
		if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_c):
			if EmuOnly == 0:
				GPcom.ClearDisp()
		
		#initiate screen
		if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_i):
			if EmuOnly == 0:
				GPcom.initiate()
				
		#FrameLimiter
		ctime = T.time()
		ctime = cycletime(ctime, fpslimit)
		
Game()
