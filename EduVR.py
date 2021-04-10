from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
app = Ursina()
grass_t = load_texture('assets/grass_block.png')
stone_t = load_texture('assets/stone_block.png')
brick_t = load_texture('assets/brick_block.png')
dirt_t = load_texture('assets/dirt_block.png')
water_t = load_texture('assets/water_block.png')
sand_t = load_texture('assets/sand_block.png')
brick1_t = load_texture('assets/brick1_block.png')
brick2_t = load_texture('assets/brick2_block.png')
brick3_t = load_texture('assets/brick3_block.png')
brick4_t = load_texture('assets/brick4_block.png')
sky_t = load_texture('assets/skybox.png')
arm_t = load_texture('assets/arm_texture.png')

punch_s = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1
window.fps_counter.enabled = False
window.exit_button.visible = False
def update():
	global block_pick
	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()
	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4
	if held_keys['5']: block_pick = 5
	if held_keys['6']: block_pick = 6
	if held_keys['7']: block_pick = 7
	if held_keys['8']: block_pick = 8
	if held_keys['9']: block_pick = 9
	if held_keys['0']: block_pick = 0
class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_t):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)

	def input(self,key):
		if self.hovered:
			if key == 'left mouse down':
				punch_s.play()
				if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_t)
				if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_t)
				if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_t)
				if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_t)
				if block_pick == 5: voxel = Voxel(position=self.position + mouse.normal, texture=water_t)
				if block_pick == 6: voxel = Voxel(position=self.position + mouse.normal, texture=sand_t)
				if block_pick == 7: voxel = Voxel(position=self.position + mouse.normal, texture=brick1_t)
				if block_pick == 8: voxel = Voxel(position=self.position + mouse.normal, texture=brick2_t)
				if block_pick == 9: voxel = Voxel(position=self.position + mouse.normal, texture=brick3_t)
				if block_pick == 0: voxel = Voxel(position=self.position + mouse.normal, texture=brick4_t)

			if key == 'right mouse down':
				punch_s.play()
				destroy(self)

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_t,
			scale = 150,
			double_sided = True)
class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_t,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))
	def active(self):
		self.position = Vec2(0.3,-0.5)
	def passive(self):
		self.position = Vec2(0.4,-0.6)

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)
xpix, ypix = 20, 20
pic = []
for i in range(xpix):
	row = []
	for j in range(ypix):
		noise_val = noise1([i / xpix, j / ypix])
		noise_val += 0.5 * noise2([i / xpix, j / ypix])
		noise_val += 0.25 * noise3([i / xpix, j / ypix])
		noise_val += 0.125 * noise4([i / xpix, j / ypix])
		if (noise_val < -0.27):
			row.append(-2)
		elif (noise_val < -0.1):
			row.append(-1)
		elif (noise_val < 0.1):
			row.append(0)
		elif (noise_val < 0.3):
			row.append(1)
		else:
			row.append(2)
	pic.append(row)
for z in range(xpix):
	for x in range(ypix):
			voxel = Voxel(position = (x,pic[z][x],z))
			voxel = Voxel(position=(x, -1, z),texture=water_t)
			voxel = Voxel(position=(x, -3, z))
player = FirstPersonController()
sky = Sky()
hand = Hand()
app.run()