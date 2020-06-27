import pygame
import os.path
from block import Block

FILE_EXT = ".mario"

class Level:

    blocks = []
    name = ""
    grid_size = 20 # default grid size

    def __init__(self, dir_path):
        self.path = f"{dir_path}/{FILE_EXT}"
        if os.path.exists(self.path):
            self.load()
        else:
            self.save()
   
    def compress_vertical(self, column):
        line = ""

        if len(column) == 1:

            # add one
            line += f"{column[0]}"

        elif len(column) > 1:

            # add multiple
            count = 1
            last_val = column[0]
            for val in column[1:]:
                if val == last_val:             # repeat
                    count += 1
                elif count > 1:                 # multiple
                    line += f"{last_val}x{count},"
                    count = 1
                else:
                    line += f"{last_val},"      # single

                # update value
                last_val = val
                
            # add last to line
            line += f"{last_val}x{count}" if count > 1 else f"{last_val}"
        
        return line
    
    def compress_horizontal(self, grid):
        lines = []

        if len(grid) == 1:

            # add one
            line = self.compress_vertical(grid[0])
            lines.append(line)

        elif len(grid) > 1:
            count = 1
            last_line = self.compress_vertical(grid[0])

            # add multiple
            for col in grid[1:]:
                line = self.compress_vertical(col)

                if line == last_line:               # repeat
                    count += 1
                elif count > 1:                     # multiple
                    lines.append(f"({last_line})x{count}")
                    count = 1
                else:                               #single
                    lines.append(last_line)

                # update
                last_line = line

            # add last line
            line = f"({last_line})x{count}" if count > 1 else last_line
            lines.append(line)

        return lines
       

    def decompress_vertical(self, string):
        column = []

        if string:
            for item in string.split(","):
                if "x" in item:
                    # add compressed
                    repeatBlock = item.split("x")
                    block_id = int(repeatBlock[0])
                    count = int(repeatBlock[1])
                    while count > 0:
                        count -= 1
                        column.append(block_id)
    
                else:
                    # add regular
                    column.append(int(item))

        return column

    # ex: (0x3,4)x3
    def decompress_horizontal(self, strings):
        grid = []

        for string in strings:
            
            # decompress horizontally
            count = 1
            if string.startswith("("):
                [string, count] = string[1:].split(")x")
                count = int(count)

            # decompress vertically
            column = self.decompress_vertical(string)
           
            # add
            for i in range(count):
                grid.append(column.copy())

        return grid

    # load a .mario file into a usable 2D array (that uses x, y coordinates)
    def load(self):
        lines = []

        # read in file
        with open(self.path) as f:
            self.name = f.readline().strip()
            print(f"loading {self.name}...")
            
            for line in f:
                lines.append(line.strip())

        # decompress & save
        self.blocks = self.decompress_horizontal(lines)

    # save and overwrite file
    def save(self):
        print("saving...")
        lines = self.compress_horizontal(self.blocks)

        with open(self.path, "w") as f:

            # write level name
            f.write(f"{self.name}\n")

            for line in lines:
                f.write(line + "\n")
    
    def draw(self, screen):
        for col_idx in range(0, len(self.blocks)):
            col = self.blocks[col_idx]
            for row_idx in range(0, len(col)):
                value = col[row_idx]
                Block.draw(screen, col_idx, row_idx, value, self.grid_size)
  
    def toString(self):
        return f"{self.name}: {self.blocks}"
           

if __name__ == '__main__':
    project_dir = "/home/device/Projects/MND"
    level = Level(project_dir)
    print(level.toString())