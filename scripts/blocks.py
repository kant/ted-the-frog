import bge

from random import choice, randrange

def animateWaterRipples(cont):
	own = cont.owner
	always = cont.sensors[0]
	
	ALPHA_FACTOR = 0.005
	SCALING_FACTOR = 0.01
	ROTATION_FACTOR = 0.01
	
	if always.positive and own.color[3] > 0:
		own.color[3] -= ALPHA_FACTOR
		own.applyRotation([0, 0, ROTATION_FACTOR], True)
		own.applyRotation([0, 0, ROTATION_FACTOR], True)
		own.localScale.x += SCALING_FACTOR
		own.localScale.y += SCALING_FACTOR
		
	else:
		own.endObject()

def normal(cont):
	
	own = cont.owner
	
	autostart = cont.sensors[0]
	
	if autostart.positive:
		
		own.replaceMesh(choice(['Rock1', 'Rock2', 'LilyPad']))
		
		if own['FirstBlock']:
			for obj in own.childrenRecursive:
				if not 'Water' in obj:
					obj.endObject()
		
		else:
		
			flies = own.childrenRecursive['Flies']
			clock = own.childrenRecursive['Clock']
			props = [flies, clock]
			
			prop = choice(props)
			chance = 25 if prop.name == 'Flies' else 10
			
			for p in props:
				if p.name != prop.name:
					p.endObject()
					
			if randrange(0, 100) not in range(0, randrange(0, chance)):
				prop.endObject()