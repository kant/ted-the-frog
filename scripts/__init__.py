import os
import zlib
import bge

from pathlib import Path
from ast import literal_eval
from pprint import pprint, pformat

from bge.logic import globalDict, expandPath

DEFAULT_SCORE = {'Time' : 30, 'Points' : 0}

os.system('cls')

def main():
	globalDict['Score'] = DEFAULT_SCORE
	loadSettings()
	loadLang()
	loadScores()

def saveScores():
	_file = Path(expandPath('//scores.dat'))
	_file = _file.resolve() if _file.exists() else _file
	
	with open(_file.as_posix(), 'wb') as openedFile:
		openedFile.write(zlib.compress(str(globalDict['Scores']).encode(), 1))
		print('> Scores written to:', _file.name)

def generateScoreBoard():
	
	globalDict['ScoreBoard'] = ''
	globalDict['Scores'].sort(reverse=True)
	
	if len(globalDict['Scores']) > 7:
		globalDict['Scores'] = globalDict['Scores'][0 : 7]
	
	for _score in globalDict['Scores']:
		globalDict['ScoreBoard'] += _score[1] + ' - ' + str(_score[0]) + globalDict['Lang'][globalDict['Settings']['Language']]['HudPoints2'] + '    '
		
	saveScores()

def loadSettings():
	_file = Path(expandPath('//settings.txt'))
	_file = _file.resolve() if _file.exists() else _file
	
	try:
		with open(_file.as_posix(), 'r') as openedFile:
			globalDict['Settings'] = literal_eval(openedFile.read())
			print('> Settings loaded from:', _file.name)
			
	except:
		globalDict['Settings'] = {
								'Fullscreen' : False,
								'Shaders' : True,
								'Language' : 'English'
								}
		print('X Failed to load settings, reset to default')
		
		_file.open(mode='w', encoding='utf_8').write(pformat(globalDict['Settings'], width=10))
		print('> Settings written to:', _file.name)

def loadLang():
	
	path = Path(expandPath('//lang/')).resolve()
	globalDict['Lang'] = {}
	
	for _file in path.iterdir():
		
		if _file.suffix == '.txt':
		
			try:
				globalDict['Lang'][_file.stem] = literal_eval(_file.open(encoding='utf_8').read())
				print('> Language read from:', _file.name)
				
			except:
				print('X Could not read language:', _file.name)

def loadScores():
	_file = Path(expandPath('//scores.dat'))
	_file = _file.resolve() if _file.exists() else _file
	
	try:
		with open(_file.as_posix(), 'rb') as openedFile:
			globalDict['Scores'] = literal_eval(zlib.decompress(openedFile.read()).decode())
			print('> Scores loaded from:', _file.name)
			
	except:
		globalDict['Scores'] = []
		print('X Failed to load scores, reset to default')
		saveScores()
		
	generateScoreBoard()

main()