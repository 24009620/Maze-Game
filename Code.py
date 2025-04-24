from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Set up the window
window.fullscreen = True
window.borderless = False
window.cog_button.disable()
window.collider_counter.disable()
window.entity_counter.disable()
window.fps_counter.disable()
window.exit_button.disable()

# Create the ground
map = Entity(model="plane", scale=100, collider="mesh", texture="grass", outline=True, y=0)
Sky()

# Add lighting
light = PointLight(parent=map, position=(110, 100, 0), color=color.white, intensity=1)  # Increased intensity
ambient_light = AmbientLight(color=color.rgba(100, 100, 100, 0.5), intensity=0.5)  # Increased intensity

# Define maze position offset
maze_offset_x = -50  # Change this value to move the maze left/right
maze_offset_z = 50  # Change this value to move the maze forward/backward

# Create walls for the maze
def create_wall(x, y, z):
    wall = Entity(model='cube', texture="brick", color=color.gray, scale=(1, 5, 1), position=(x + maze_offset_x, 2.5, z + maze_offset_z),
                  collider='box')
    return wall

# Generate a simple random maze layout
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # Randomly carve out paths in the maze
    for i in range(1, height - 1, 2):
        for j in range(1, width - 1, 2):
            maze[i][j] = 0  # Create a path
            if random.choice([True, False]):
                if j + 1 < width - 1:
                    maze[i][j + 1] = 0  # Carve right
            else:
                if i + 1 < height - 1:
                    maze[i + 1][j] = 0  # Carve down

    return maze

# Create a 100x100 maze layout
maze_layout = generate_maze(100, 100)

# Create the maze based on the layout
for z, row in enumerate(maze_layout):
    for x, cell in enumerate(row):
        if cell == 1:
            create_wall(x, 0, -z)

# Set up the player
player = FirstPersonController(y=10)
player.speed = 10  # Default speed
player.jump_height = 10
player.gravity = 0.5

# Create the exit
exit_position = (maze_offset_x + 1, 0, maze_offset_z - 1)  # Adjust this position as needed
exit_entity = Entity(model='cube', color=color.green, scale=(1, 1, 1), position=exit_position, collider='box')

# Function to handle exit collision
def on_exit():
    print("You've found the exit! Game Over.")
    application.quit()  # Exit the game

# Add collision detection for the exit
def update():
    if player.intersects(exit_entity).hit:
        on_exit()

app.run()
