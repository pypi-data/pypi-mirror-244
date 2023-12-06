import numpy as np
import os
from platform import system
import time
import pynput


pressed_keys = set()
# translate key
translate = lambda key: key.char if hasattr(key, "char") else key.name

def on_press(key):
    key = translate(key)   
    if key not in pressed_keys:
        pressed_keys.add(key)

def on_release(key):
    key = translate(key)
    if key in pressed_keys:
        pressed_keys.remove(key)

def init(catch_sys=True):
    os_name = system()

    if os_name == 'Windows':
        os.system('cls')
    elif os_name == 'Linux' or os_name == 'Darwin':
        os.system('clear')
    else:
        if catch_sys:
            raise RuntimeError(f"Unsoported OS: {system()}. Use init(catch_sys=False) to ignore.")


    global keyboard_listener
    keyboard_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

def qquit():
    try:
        keyboard_listener.stop()
    except NameError:
        pass
    quit()
    



# TODO: COMPATIBLE WITH OTHER OS?



def overlay(from_array: np, to_array: np, pos: tuple):
    
    # CHECK IF OFF SCREEN, IF YES THEN DON'T BOTHER
    if (pos[0] + from_array.shape[1]) < 0 or (pos[1] + from_array.shape[0]) < 0 or (pos[0] > to_array.shape[1]) or (pos[1] > to_array.shape[0]):
        return to_array

    # OTHERWISE SAFTELY STACK THEM
    pad = np.max(from_array.shape)
    a = np.pad(to_array, pad, constant_values='padding')
    start_y = pos[1]+pad
    start_x = pos[0]+pad
    a[start_y:start_y+from_array.shape[0], start_x:start_x+from_array.shape[1]] = from_array

    start_y, end_y = pad, a.shape[0] - pad
    start_x, end_x = pad, a.shape[1] - pad

    a = a[start_y:end_y, start_x:end_x]

    return a


last_time = time.time()
def tick(FPS):
    global last_time

    min_time = 1/FPS
    # How long we need to wait to maintain FPS
    wait_time = min_time - last_time + time.time()
    if wait_time > 0:
        time.sleep(wait_time)

    last_time = time.time()



class Box:
    def __init__(self, size: tuple, pos=(0, 0), fill='box', custom_pattern=None):
        # NOTE: pos refers to position in the (x, y) format. Numpy thinks in the [y, x] format.
        self.pos = pos
        
        if size[0] <=0 or size[1] <= 0:
            raise ValueError(f"size ({size}) cannot be less than or equal to zero")

        def make_box(t, b, l, r, tl, tr, bl, br, center=" ", mini_box="□", thin_v="║", thin_h="═"):
            # CREATE A BOX SHAPE
            if size == (1, 1):
                self.plate = np.array([[mini_box]])
            elif size[0] == 1:
                self.plate = np.full(size[::-1], thin_v)
            elif size[1] == 1:
                self.plate = np.full(size[::-1], thin_h)
            else:
                self.plate = np.full(size[::-1], center)
                self.plate[0,], self.plate[-1,] = t, b
                self.plate[:,0], self.plate[:,-1] = l, r
                self.plate[0][0], self.plate[0][-1], self.plate[-1][0], self.plate[-1][-1] = tl, tr, bl, br

        # DEFUALT FILLS
        if fill == 'box':
            make_box('─', '─', '│', '│', '┌', '┐', '└', '┘')
        elif fill == 'rounded box':
            make_box('─', '─', '│', '│', '╭','╮','╰','╯')
        elif fill == 'lines':
            self.plate = np.full(size[::-1], "─")
        elif fill == 'grid':
            make_box('┬', '┴', '├', '┤', '┌', '┐', '└', '┘', '┼')
        elif fill == 'solid fill':
            self.plate = np.full(size[::-1], "█")
        elif fill == 'solid empty':
            self.plate = np.full(size[::-1], " ")
        elif fill == 'custom':
            self.plate = np.array([list(i) for i in custom_pattern.strip('\n').split('\n')])  # MULTI-LINE STRING -> NUMPY ARRAY
            if self.plate.shape[0] > size[1] or self.plate.shape[1] > size[0]:
                raise ValueError(f"Custom Pattern of size {self.plate.shape[::-1]} does not fit in size {size}")
            else:
                self.plate = np.pad(self.plate, ((0, size[1]-self.plate.shape[0]),(0, size[0]-self.plate.shape[1])),constant_values="-")
        else:
            raise ValueError(f"{fill} is not an option for fill.")
        
        self.face = self.plate

    def draw(self, other_box, from_scratch=True):
        p = other_box.pos
        if from_scratch:
            self.face = overlay(other_box.plate, self.plate, p)
        else:  # from_scratch=False is the same as draw_next(other_box)
            self.face = overlay(other_box.plate, self.face, p)

    def draw_next(self, other_box):
        p = other_box.pos
        self.face = overlay(other_box.plate, self.face, p)

    def move(self, x, y):
        self.pos = self.pos[0]+x, self.pos[1]+y

    def collide(self, other_box):
        # TEST COLLISION BY INTERSECTING THE SETS OF X AND Y COORDINATES IT EXISTS AT
        self_x = [i for i in range(self.pos[0], self.pos[0] + self.plate.shape[1])]
        self_y = [i for i in range(self.pos[1], self.pos[1] + self.plate.shape[0])]
        other_x = [i for i in range(other_box.pos[0], other_box.pos[0] + other_box.plate.shape[1])]
        other_y = [i for i in range(other_box.pos[1], other_box.pos[1] + other_box.plate.shape[0])]

        x_overlap = set(self_x).intersection(other_x)
        y_overlap = set(self_y).intersection(other_y)
        if (x_overlap == set()) or (y_overlap == set()):
            return False
        else:
            return True

    def __repr__(self):
        # Transforms the numpy aray into a string. \x1b[H is code for "Go to top left"
        return "\x1b[H" + "\n".join(["".join(r) for r in self.face])



def test():
    # EXAMPLE...
    class Sprite(Box):
        def update(self, keys):
            if "left" in keys:
                self.pos = self.pos[0]-1, self.pos[1]
            if "right" in keys:
                self.pos = self.pos[0]+1, self.pos[1]
            if "up" in keys:
                self.pos = self.pos[0], self.pos[1]-1
            if "down" in keys:
                self.pos = self.pos[0], self.pos[1]+1

    b = Sprite((4, 4))
    s = Box((150, 30), fill='rounded box')

    init()

    s.draw(b)
    print(s)
    run = True
    while run:
        b.update(pressed_keys)
        s.draw(b)
        print(s)
        print(b.pos)

        if 'esc' in pressed_keys:
            run = False
        tick(30)

    qquit()


if __name__ == "__main__":
    test()
    
# Chome dino. Just becuase
dino = '''
                     
           ████████  
          ███▄███████
          ███████████
          ███████████
          ██████     
          █████████  
█       ███████      
██    ████████████   
███  ██████████  █   
███████████████      
███████████████      
 █████████████       
  ███████████        
    ████████         
     ███  ██         
     ██    █         
     █     █         
     ██    ██        
                     
'''
