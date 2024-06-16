import color
#attribute.py

#player
player = {
'color': color.brown,
'width': 44,
'height': 44,
'thick': 5,
'speed': 3,
'health': 10,
'dodge': 0,
'eyecolor': color.black,
'eyeradius': 5,
}

#bullet
bullet = {
'color': color.black,
'width': 5,
'height': 5,
'speed': 5.5,
'rate': 3,
'range': 500,
'damage': 20,
}
bullet['radius'] = 4 + bullet['damage']*0.2

#zombie
zombie = {
'bodycolor': color.brown,
'eyecolor': color.red,
'mouthcolor': color.black,
'toothcolor': color.white,
'width': 45,
'height': 45,
'speed': 1,
'health': 100,
'dodge': 0,
'frequency': 5,
'health_up': 5,
}