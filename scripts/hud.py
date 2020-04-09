import bge

from bge.logic import globalDict, expandPath
from pprint import pformat

def text(cont):
	pass

def switchLang(scene):
	if globalDict['Settings']['Language'] == 'Português':
		globalDict['Settings']['Language'] = 'English'
		
	else:
		globalDict['Settings']['Language'] = 'Português'
		
	scene.restart()
	
	with open(expandPath('//settings.txt'), 'w') as openedFile:
		openedFile.write(str(globalDict['Settings']))
		print('Saved settings to', openedFile.name)

def widget(cont):
	
	own = cont.owner
	scene = own.scene
	camera = scene.active_camera
	
	over = cont.sensors['Over']
	lmb = cont.sensors['LMB']
	
	game_path = expandPath('//main.blend')
	
	if not over.positive:
		own.color[3] = 0.7
	
	if over.positive:
		own.color[3] = 0.9
		
		if own.groupObject and lmb.positive:
			
			if 'Command' in own.groupObject:
				try:
					commands = own.groupObject['Command'].split(' | ')
					for command in commands:
						exec(command)
					
				except:
					print('X Cannot eval expression:', own.groupObject['Command'])