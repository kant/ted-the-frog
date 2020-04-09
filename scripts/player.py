import datetime

import bge
import mathutils

from random import choice

from bge.logic import mouse, globalDict
from bge import events as k

from . import generateScoreBoard

SPAWN_DIST = 13
DEFAULT_SCORE = {'Time' : 30, 'Points' : 0}

def updateScores():
	
	curDate = datetime.datetime.now()
	globalDict['Scores'].append((
		globalDict['Score']['Points'],
		str(curDate.day).zfill(2) + '/' + str(curDate.month).zfill(2) + '/' + str(curDate.year)[2:4] + ' ' + str(curDate.hour) + ':' + str(curDate.minute).zfill(2)
	))
	
	generateScoreBoard()

def main(cont):
	
	own = cont.owner
	scene = own.scene
	
	always = cont.sensors['Always']
	always60 = cont.sensors['Always60']
	
	lmb = mouse.events[k.LEFTMOUSE] == 1
	rmb = mouse.events[k.RIGHTMOUSE] == 1
	
	actShort = cont.actuators['Short']
	actLong = cont.actuators['Long']
	actStopped = cont.actuators['Stopped']
	actJump = cont.actuators['Jump']
	actJumpL = cont.actuators['JumpLong']

	frogArmature = own.childrenRecursive['FrogArmature']

	if always.positive:
		
		death(cont)
		
		if always.status == 1:
			globalDict['Score']['Points'] = 0
			globalDict['Score']['Time'] = 30
			updateLevel(cont)
	
		if always60.positive and globalDict['Score']['Time'] > 0 and not own['Dead']:
			globalDict['Score']['Time'] -= 1
			
			if globalDict['Score']['Time'] <= 0:
				updateScores()
				cont.activate(cont.actuators['SDeath'])
				own['Dead'] = True
				own.sendMessage('Death')
		
		if not own.isPlayingAction():
			own['IsJumping'] = False
		
		if not own['IsJumping'] and not own['Dead']:
			
			own['CurPos'] = (int(own.worldPosition.x) // 2) * 2
				
			if lmb or rmb:
				own['IsJumping'] = True
				cont.activate(cont.actuators['SJump'])
				updateLevel(cont)
				cont.deactivate(actShort)
				cont.deactivate(actLong)
					
				if lmb:
					own['ShortJump'] = True
					cont.activate(actShort)
					globalDict['Score']['Points'] += 1
					
				if rmb:
					own['ShortJump'] = False
					cont.activate(actLong)
					globalDict['Score']['Points'] += 2
			
	
		if own['Dead'] == False:
			
			if own['IsJumping'] == False:
				cont.activate(actStopped)
				
			else:
				if own['ShortJump']:
					cont.activate(actJump)
					
				if not own['ShortJump']:
					cont.activate(actJumpL)
	pass

def updateLevel(cont):
	
	own = cont.owner
	scene = own.scene
	curPos = own['CurPos']
	
	blocks = ('BlockDeath', 'BlockNormal')
	blocksRange = tuple(range(curPos - SPAWN_DIST - 1, curPos + SPAWN_DIST + 2, 2))
	bgRange = tuple(range(curPos // 10 * 10 -20, curPos // 10 * 10 +21, 10))
	
	if not 'Background' in scene:
		scene['Background'] = {}
	
	if not 'Blocks' in scene:
		scene['Blocks'] = {}
		
	for i in bgRange:
		if not i in scene['Background'].keys():
			bg = scene.addObject('BGGround')
			bg.worldPosition.x = i
			scene['Background'][i] = bg
			
	for i in scene['Background'].copy().keys():
		
		if not i in bgRange:
			scene['Background'].pop(i).endObject()
		
	for i in blocksRange:
		
		block = None
		
		if not i in scene['Blocks'].keys():
			
			if i == 0:
				block = scene.addObject('BlockNormal')
				block['FirstBlock'] = True
			
			elif i-2 in scene['Blocks'].keys():
				
				if 'BlockDeath' in scene['Blocks'][i-2]:
					block = scene.addObject('BlockNormal')
					
				else:
					block = scene.addObject(choice(blocks))
				
			else:
				block = scene.addObject(choice(blocks))
				
		if block:
			block.worldPosition.x = i
			scene['Blocks'][i] = block
			
	for i in scene['Blocks'].copy().keys():
		
		if not i in blocksRange:
			scene['Blocks'].pop(i).endObject()
	pass

def death(cont):
	
	own = cont.owner
	
	collision = cont.sensors['Collision']
	curPos = int(own.worldPosition.x)
	
	if collision.positive and collision.status == 1 and curPos != 0:
		
		if 'Flies' in collision.hitObject:
			cont.activate(cont.actuators['SFly'])
			collision.hitObject.endObject()
			globalDict['Score']['Points'] += 4
		
		if 'Clock' in collision.hitObject:
			cont.activate(cont.actuators['STime'])
			collision.hitObject.endObject()
			globalDict['Score']['Time'] += 5
		
		if 'Death' in collision.hitObject:
			updateScores()
			cont.activate(cont.actuators['SDeath'])
			cont.activate(cont.actuators['SRoar'])
			own.scene.addObject('WaterRipples', collision.hitObject.parent.childrenRecursive['WaterRipplesSpawner'])
			own['Dead'] = True
			own.sendMessage('Death')
			
			for obj in own.childrenRecursive:
				if 'FrogMesh' in obj:
					obj.visible = False
					break
			
			for obj in collision.hitObject.parent.childrenRecursive:
				if 'Croc' in obj:
					obj.playAction('Croc', 0, 11)
					break
	pass

def moveCamera(cont):
	own = cont.owner
	always = cont.sensors[0]
	
	if always.positive:
		own.worldPosition.z = 0

def updateWater(cont):
	
	own = cont.owner
	scene = own.scene
	
	always = cont.sensors[0]
	
	transMatrix = mathutils.Matrix.Translation([0.01, 0, 0])
	
	if always.positive:
		
		if scene.name == 'Menu':
			water = None
			
			if not 'Water' in scene:
				try:
					scene['Water'] = [obj for obj in scene.objects if 'Water' in obj][0]
					
				except:
					scene['Water'] = None
					
			water = scene['Water']
				
			if water is not None:
				water.meshes[0].transformUV(-1, transMatrix)
		
		elif scene.name == 'Game':
			water = [obj for obj in scene['Blocks'][own['CurPos']].childrenRecursive if 'Water' in obj][0]
			water.meshes[0].transformUV(-1, transMatrix)
	pass