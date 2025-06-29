# Raycasting-in-pygame

A simple **2.5D raycasting engine** built with Python and Pygame, inspired by the early days of 3D gaming (like *Wolfenstein 3D*). This project renders a pseudo-3D view using raycasting and supports first-person movement, collision detection, and a minimap.

---

## Features

- Raycasting-based rendering for 3D effect
- Player movement and rotation (WASD + QE keys)
- Collision detection with push-back response
- Dynamic shading based on distance
- Top-down minimap with real-time updates


---
## Controls

| Key | Action |
|-----|--------|
| `W` | Move Forward |
| `S` | Move Backward |
| `A` | Rotate Left |
| `D` | Rotate Right |
| `Q` | Strafe Left |
| `E` | Strafe Right |

---

## Map Configuration

The game world is built using rectangles defined by:
(x, y, width, height)
```
walls = [
    (50, 50, 1100, 20),    # Top border
    (50, 650, 1100, 20),   # Bottom border
    (50, 50, 20, 600),     # Left border
    (1130, 50, 20, 600),   # Right border
    ...
]
```



---
## How It Works

### Raycasting
The player emits 500 rays within a 60° field of view (FOV). Each ray is tested against all wall edges to find the closest intersection.

### Intersection Detection
Wall rectangles are broken into individual line segments. Each ray uses 2D line-line intersection math to detect hits with walls.

### Fish-Eye Correction
Rays farther from the center can distort the perceived image. To correct this, the distance is adjusted using cosine based on the ray’s angle offset.

### Wall Rendering
The shorter the distance to the wall, the taller it appears. This inverse-distance scaling gives the illusion of depth.

### Shading
The color of wall slices is darkened based on distance. Distant walls appear dimmer to enhance realism.

### Collision Detection
Movement is restricted when the player’s circular radius overlaps with any wall. A push-back vector moves the player slightly away from the obstacle.

### Minimap
A top-down 2D map shows walls as black rectangles, the player as a red circle, and the view direction as a line.


---
## Code Overview


| Component         | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `player_pos`      | A `pygame.Vector2` representing the player's current position in the world. |
| `linecord`        | A second point used to determine the player's view direction vector.        |
| `walls`           | A list of rectangles, each defined by `(x, y, width, height)` for obstacles.|
| `line_intersect()`| A function that calculates 2D line-line intersections for ray-wall hits.    |
| Raycasting Loop   | The main loop that casts rays, calculates distances, and renders walls.     |
| Movement Logic    | Handles forward/backward/strafe movement based on direction vector.         |
| Collision Logic   | Prevents the player from moving through walls using circle-rectangle collision detection. |
| Fish-Eye Correction | Corrects the ray length distortion for side rays using cosine adjustment. |
| Minimap Rendering | Draws a top-down view of the player and walls in a scaled-down corner.      |


---
## Running the Game

1. Clone the repository:

```bash
git clone https://github.com/your-username/pygame-raycaster.git
cd pygame-raycaster
```
2. Install dependencies
```bash
pip install pygame
```
3. Run the game:
```bash
python raycasting.py
```

---
## Screenshots and Demos

### Gameplay Demo
![Gameplay Demo](22.gif)

### Gameplay Screenshots

![Gameplay Screenshot 1](Screenshot%202025-06-29%20130129.png)

![Gameplay Screenshot 2](Screenshot%202025-06-29%20130202.png)
