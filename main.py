import pygame
import sys
import re
import pickle
from datetime import datetime
from enum import StrEnum
from PIL import Image
from itertools import cycle


class Color(StrEnum):
    # Skin Tones
    LIGHT_SKIN = '#FFE0BD'
    FAIR_SKIN = '#FFCD94'
    TAN_SKIN = '#EAC086'
    BROWN_SKIN = '#C68642'
    DARK_BROWN = '#8D5524'
    VERY_DARK_SKIN = '#4B2E1A'

    # Hair & Eyes
    BLACK = '#000020'
    DARK_GRAY = '#4B4B4B'
    BROWN = '#A0522D'
    BLONDE = '#FFD700'
    SILVER = '#A9A9A9'
    AUBURN = '#5B3C11'

    # Clothing
    CRIMSON = '#8B0000'
    RED = '#DC143C'
    ORANGE = '#FFA500'
    YELLOW = '#FFFF00'
    DARK_GREEN = '#006400'
    BRIGHT_GREEN = '#00FF00'
    NAVY = '#00008B'
    ROYAL_BLUE = '#4169E1'
    PURPLE = '#8A2BE2'
    PINK = '#FF69B4'
    SLATE_GRAY = '#708090'    
    OFF_WHITE = '#FFFFAA'
    
    # Metal/Utility/Outline
    STEEL = '#B0C4DE'
    LIGHT_METAL = '#C0C0C0'
    GOLD = '#FFEB3B'
    OUTLINE = '#2F2F2F'

    # Environment
    DIRT = '#8B4513'
    WATER = '#00CED1'
    STONE = '#7D7D75'
    GRASS = '#66BB66'  
    
    
    # lighter set
    # lighter skin tones    
    LIGHT_SKIN_L = '#FFF1E3'
    FAIR_SKIN_L = '#FFE4C8'
    TAN_SKIN_L = '#F8DDB5'
    BROWN_SKIN_L = '#E6B988'
    DARK_BROWN_L = '#C38C5A'
    VERY_DARK_SKIN_L = '#8A5B3A'
    
    # lighter hair & eyes
    BLACK_L = '#404060'
    DARK_GRAY_L = '#909090'
    BROWN_L = '#C98B60'
    BLONDE_L = '#E6E600'
    SILVER_L = '#E6E6E6'
    AUBURN_L = '#996B3A'
    
    # lighter clothing
    CRIMSON_L = '#C83232'
    RED_L = '#F2757F'
    ORANGE_L = '#FFCC66'
    YELLOW_L = '#FFFF44'
    DARK_GREEN_L = '#44AA44'
    BRIGHT_GREEN_L = '#99FF99'
    NAVY_L = '#4C4CBB'
    ROYAL_BLUE_L = '#92AFFF'
    PURPLE_L = '#C78DF2'
    PINK_L = '#FFA3D3'
    SLATE_GRAY_L = '#AAB9C2'
    OFF_WHITE_L = '#FFFFCC'
    
    # lighter metal/utility/outline
    STEEL_L = '#D8E4F0'
    LIGHT_METAL_L = '#EAEAEA'
    GOLD_L = '#FFE066'
    OUTLINE_L = '#6A6A6A'
    
    # lighter environment
    DIRT_L = '#B46A3B'
    WATER_L = '#66E8E9'
    STONE_L = '#BFBFB7'
    GRASS_L = '#A8EFA8'
    
    # lightest skin tones    
    LIGHT_SKIN_LL = '#FFF8F1'
    FAIR_SKIN_LL = '#FFEEDC'
    TAN_SKIN_LL = '#FAEACF'
    BROWN_SKIN_LL = '#F1D4B1'
    DARK_BROWN_LL = '#D7AB82'
    VERY_DARK_SKIN_LL = '#B07B59'
    
    # lightest hair & eyes
    BLACK_LL = '#606080'
    DARK_GRAY_LL = '#B0B0B0'
    BROWN_LL = '#DEB9A1'
    BLONDE_LL = '#FFF799'
    SILVER_LL = '#F5F5F5'
    AUBURN_LL = '#B98B5B'
    
    # lightest clothing
    CRIMSON_LL = '#E05B5B'
    RED_LL = '#F8A7AE'
    ORANGE_LL = '#FFE599'
    YELLOW_LL = '#FFFF99'
    DARK_GREEN_LL = '#77CC77'
    BRIGHT_GREEN_LL = '#CCFFCC'
    NAVY_LL = '#8080DD'
    ROYAL_BLUE_LL = '#BFD1FF'
    PURPLE_LL = '#E3BDF8'
    PINK_LL = '#FFC7E5'
    SLATE_GRAY_LL = '#C6D1D8'
    OFF_WHITE_LL = '#FFFFF5'
    
    # lightest metal/utility/outline
    STEEL_LL = '#EAF1F8'
    LIGHT_METAL_LL = '#E0E0E0'
    GOLD_LL = '#FFFCCD'
    OUTLINE_LL = '#D1D1D1'
    
    # lightest environment
    DIRT_LL = '#C98A5C'
    WATER_LL = '#99F2F3'
    STONE_LL = '#DCDCD6'
    GRASS_LL = '#CFF8CF'

    # eraser
    WHITE = '#FFFFFF'


class ColorTiles(pygame.Rect):
    def __init__(self, x, y, width, height, color, text_color=None):
        super().__init__(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 36)
        

    def draw(self, surface) -> None:
        global _selected_color
        
        if self.color.name == 'WHITE':
            pygame.draw.rect(surface, Color.BLACK, self)
            pygame.draw.rect(surface, self.color, self.inflate(-2, -2))
        else:
            pygame.draw.rect(surface, self.color, self)
        if self.text_color:
            text_surf = self.font.render(self.color.name, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.center)
            surface.blit(text_surf, text_rect)
            

        if _selected_color == self.color:
            pygame.draw.rect(surface, Color.BLACK, self.inflate(4, 4), 2)


    def is_clicked(self, pos):
        global _selected_color
        
        if self.collidepoint(pos):
            _selected_color = self.color
            return True
        return False

class DrawingTiles(ColorTiles):
    def __init__(self, x, y, width, height, color=Color.WHITE, text_color=None):
        super().__init__(x, y, width, height, color, text_color)

    def draw(self, surface, capture=False) -> None:
        if capture:
            pygame.draw.rect(surface, self.color, self)
        else:
            pygame.draw.rect(surface, Color.LIGHT_METAL, self)
            pygame.draw.rect(surface, self.color, self.inflate(-2, -2))

    def is_clicked(self, pos):
        if self.collidepoint(pos):
            self.color = _selected_color
            return True
        return False
    
class Buttons(ColorTiles):
    def __init__(self, x, y, width, height, color, text_color, text):
        super().__init__(x, y, width, height, color, text_color)
        self.text = text
        self.font = pygame.font.SysFont(None, 16)

    def is_clicked(self, pos):
        if self.collidepoint(pos):
            return True
        return False
    
    def draw(self, surface) -> None:
        if self.text_color and self.text:
            pygame.draw.rect(surface, self.color, self, 1)    
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.center)
            surface.blit(text_surf, text_rect)


def add_transparency_channel(path):
    img = Image.open(path).convert('RGBA')
    
    data = img.getdata()
    newData = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    
    img.save(path, "PNG")

_selected_color: Color = Color.WHITE
_save_slot: int = 0

      
def main():
    global _save_slot
    
    GRID_SIZE_OPTIONS  = [16, 22, 28, 8]
    cycle_grid_sizes = cycle(GRID_SIZE_OPTIONS)
    num_of_drawing_tiles = next(cycle_grid_sizes)
    drawing_tile_size = 25
    WIDTH: int = 800
    num_of_color_tiles = len(list(Color))
    n_rows = 3
    num_of_colors_in_row = num_of_color_tiles // n_rows
    margin = 10
    color_tile_size: int = int(round((WIDTH - margin * 2) / num_of_colors_in_row, 0))
    total_row_width = num_of_colors_in_row * color_tile_size
    x_offset = (WIDTH - total_row_width) // 2
    color_tile_x_pos: list[int] = [(i % num_of_colors_in_row) * color_tile_size + x_offset for i in range(num_of_color_tiles)]
    color_tile_y_pos: list[int] = [i // num_of_colors_in_row * (color_tile_size + 5) + 10 for i in range(num_of_color_tiles)]
    HEIGHT: int = (
        (num_of_color_tiles // num_of_colors_in_row) * color_tile_size + margin * 2 + # palette space 
        max(GRID_SIZE_OPTIONS) * drawing_tile_size + margin * 2 + # drawing space
        200 # label space
    )
    num_of_save_slots: int = 5
    save_slot_width: int = int(round((WIDTH - margin * 2) / num_of_save_slots, 0))
    save_slot_height: int = 30
    save_slot_x_pos: list[int] = [i * save_slot_width + x_offset for i in range(num_of_save_slots)]
    save_slot_y_pos: int = HEIGHT - margin * 14
    pygame.init()
    pygame.display.set_caption("Pixlr")
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 14)
    save_label_text =           'Ctrl + S:          Save to file'
    save_label_surface = font.render(save_label_text, True, (0, 0, 0))
    save_label_rect = save_label_surface.get_rect(bottomleft=(WIDTH // 2, HEIGHT - margin * 4))
    clear_label_text =          'Ctrl + Shift + K:  Clear grid'
    clear_label_surface = font.render(clear_label_text, True, (0, 0, 0))
    clear_label_rect = clear_label_surface.get_rect(bottomleft=(WIDTH // 2, HEIGHT - margin * 2))
    load_label_text =           'Ctrl + Shift + L:  Load progress'
    load_label_surface = font.render(load_label_text, True, (0, 0, 0))
    load_label_rect = load_label_surface.get_rect(bottomleft=(WIDTH // 2, HEIGHT - margin * 8))
    save_progress_label_text =  'Ctrl + Shift + A:  Save progress'
    save_progress_label_surface = font.render(save_progress_label_text, True, (0, 0, 0))
    save_progress_label_rect = save_progress_label_surface.get_rect(bottomleft=(WIDTH // 2, HEIGHT - margin * 6))
    color_label_text = 'Hover on a color to display color name and HEX code'
    color_label_surface = font.render(color_label_text, True, (0, 0, 0))
    color_label_rect = color_label_surface.get_rect(bottomleft=(margin * 3, HEIGHT - margin * 6))
    
    msg_label_text = 'Message: > messages are displayed here'
    msg_label_surface = font.render(msg_label_text, True, (0, 0, 0))
    msg_label_rect = color_label_surface.get_rect(bottomleft=(margin * 3, HEIGHT - margin * 2))
   
    
    colors = {}
    for name, value in vars(Color).items():
        if not re.match(r'^_.*_$', name):
            colors[name] = value

    color_tiles: list[ColorTiles] = []
    drawing_tiles: list[DrawingTiles] = []
    save_slots: list[Buttons] = []
    
    def reset_msg_label(msg_label_text):
        msg_label_surface = font.render(msg_label_text, True, (0, 0, 0))
        msg_label_rect = color_label_surface.get_rect(bottomleft=(margin * 3, HEIGHT - margin * 2))   
        
        return msg_label_surface, msg_label_rect    
    
    def reset_color_label(color_label_text):
        color_label_surface = font.render(color_label_text, True, (0, 0, 0))
        color_label_rect = color_label_surface.get_rect(bottomleft=(margin * 3, HEIGHT - margin * 6))
        
        return color_label_surface, color_label_rect

    def reset_drawing_tiles(num_of_drawing_tiles, drawing_tile_size) -> tuple[list[DrawingTiles], pygame.Surface, pygame.Rect]:
        print(f'Reset drawing tiles to {num_of_drawing_tiles} * {num_of_drawing_tiles}...')
        drawing_tiles: list[DrawingTiles] = []
        
        # Create DrawingTiles
        for i in range(num_of_drawing_tiles):
            for j in range(num_of_drawing_tiles):
                tile = DrawingTiles(x=i * drawing_tile_size + int(WIDTH - num_of_drawing_tiles * drawing_tile_size) / 2, y=j * drawing_tile_size + 150, width=drawing_tile_size, height=drawing_tile_size)
                drawing_tiles.append(tile)
                
        change_grid_label_text = f'Ctrl + Shift + G: Change grid size | Current: {num_of_drawing_tiles}'
        change_grid_label_surface = font.render(change_grid_label_text, True, (0, 0, 0))
        change_grid_label_rect = change_grid_label_surface.get_rect(bottomleft=(margin * 3, HEIGHT - margin * 4))

        
        return drawing_tiles, change_grid_label_surface, change_grid_label_rect

    def reset_save_slots():
        save_slots: list[Buttons] = []
        for i in range(num_of_save_slots):
            if i == _save_slot:
                save_slot_color = Color.RED
            else:
                save_slot_color = Color.BLACK_L
            slot = Buttons(x=save_slot_x_pos[i], y=save_slot_y_pos, width=save_slot_width, height=save_slot_height, color=save_slot_color, text_color=save_slot_color, text=f'Slot {i}')
            save_slots.append(slot)

        return save_slots

    # Create save slots
    save_slots = reset_save_slots()

    # Create ColorTiles
    for i, color in enumerate(Color):      
        tile = ColorTiles(x=color_tile_x_pos[i], y=color_tile_y_pos[i], width=color_tile_size - 5, height=color_tile_size, color=color)
        color_tiles.append(tile)

    drawing_tiles, change_grid_label_surface, change_grid_label_rect = reset_drawing_tiles(num_of_drawing_tiles, drawing_tile_size)

    running = True
    capture_drawing = False
    clearing_image = False
    saving_work = False
    loading_work = False


    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]:
                    for ct in color_tiles:
                        if ct.is_clicked(event.pos):
                            ...
                            # print(f"{ct.color=}")
                    for dt in drawing_tiles:
                        if dt.is_clicked(event.pos):
                            ...
                            # print(f"{ct.color=}")
                    for sl in save_slots:
                        if sl.is_clicked(event.pos):
                            _save_slot = int(sl.text.split(' ')[1])
                            save_slots = reset_save_slots()
                            break
                    msg_label_surface, msg_label_rect = reset_msg_label('Message: >')
                elif event.type == pygame.MOUSEMOTION:
                    hovered = False
                    for ct in color_tiles:
                        if ct.collidepoint(event.pos):
                            color_label_surface, color_label_rect = reset_color_label(f'{ct.color.name}: {ct.color}')
                            hovered = True
                            break
                    for dt in drawing_tiles:
                        if dt.collidepoint(event.pos):
                            color_label_surface, color_label_rect = reset_color_label(f'{dt.color.name}: {dt.color}')
                            hovered = True
                            break
                    if not hovered:
                        color_label_surface, color_label_rect = reset_color_label('')
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g and (event.mod & pygame.KMOD_CTRL) and (event.mod & pygame.KMOD_SHIFT):
                        num_of_drawing_tiles = next(cycle_grid_sizes)
                        drawing_tiles, change_grid_label_surface, change_grid_label_rect = reset_drawing_tiles(num_of_drawing_tiles, drawing_tile_size)
                        msg_label_surface, msg_label_rect = reset_msg_label('Grid changed!')
                    if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL) and not(event.mod & pygame.KMOD_SHIFT):
                        print('Saving image...')
                        msg_label_surface, msg_label_rect = reset_msg_label('Saving image...')
                        pygame.display.flip()
                        capture_drawing = True
                    if event.key == pygame.K_a and (event.mod & pygame.KMOD_CTRL) and (event.mod & pygame.KMOD_SHIFT):
                        # print('Saving your work...')
                        msg_label_surface, msg_label_rect = reset_msg_label('Saving your work...')
                        saving_work = True
                    if event.key == pygame.K_l and (event.mod & pygame.KMOD_CTRL) and (event.mod & pygame.KMOD_SHIFT):
                        # print('Loading your work...')
                        msg_label_surface, msg_label_rect = reset_msg_label('Loading your work...')
                        loading_work = True
                    elif event.key == pygame.K_k and (event.mod & pygame.KMOD_CTRL) and (event.mod & pygame.KMOD_SHIFT):
                        # print('Clearing image...')
                        msg_label_surface, msg_label_rect = reset_msg_label('Clearing image...')
                        clearing_image = True
                    
        except AttributeError as e:
            # print(f"{e=}: 'Something glitched during pygame.event.get()'")
            msg_label_surface, msg_label_rect = reset_msg_label(f"{e=}: 'Something glitched during pygame.event.get()'")
        except Exception as e:
            msg_label_surface, msg_label_rect = reset_msg_label(f"{e=}: 'Something glitched during pygame.event.get()'")
        finally:
            pass


        if saving_work:
            drawing_tile_colors = [dt.color for dt in drawing_tiles]
            with open(f'save_{_save_slot}.pkl', 'wb') as f:
                pickle.dump(drawing_tile_colors, f)
            # print('Your work is saved!')
            msg_label_surface, msg_label_rect = reset_msg_label('Your work is saved!')
            saving_work = False

        if loading_work:
            try:
                with open(f'save_{_save_slot}.pkl', 'rb') as f:
                    saved_tile_colors = pickle.load(f)
                for i, dt in enumerate(drawing_tiles):
                    dt.color = saved_tile_colors[i]
                msg_label_surface, msg_label_rect = reset_msg_label('Your work is loaded!')
                pygame.display.update()
            except FileNotFoundError as e:
                # print(f'Nothing saved in slot {_save_slot}')
                msg_label_surface, msg_label_rect = reset_msg_label(f'Nothing saved in slot {_save_slot}')
            finally:
                loading_work = False


        if clearing_image:
            for dt in drawing_tiles:
                dt.color = Color.WHITE
            # print('Image cleared!')
            msg_label_surface, msg_label_rect = reset_msg_label('Image cleared!')
            clearing_image = False
                    
        
        screen.fill((255, 255, 255)) 
        
        for ct in color_tiles:
            ct.draw(screen)  # Draw the color tiles
            
        for dt in drawing_tiles:
            dt.draw(screen, capture_drawing)  # Draw the drawing tiles
            
        for sl in save_slots:
            sl.draw(screen)
        
        screen.blit(save_label_surface, save_label_rect)
        screen.blit(clear_label_surface, clear_label_rect)
        screen.blit(load_label_surface, load_label_rect)
        screen.blit(change_grid_label_surface, change_grid_label_rect)
        screen.blit(save_progress_label_surface, save_progress_label_rect)
        screen.blit(color_label_surface, color_label_rect)
        screen.blit(msg_label_surface, msg_label_rect)
        
        pygame.display.flip()

        if capture_drawing:                    
            min_x = int((WIDTH - num_of_drawing_tiles * drawing_tile_size) / 2)
            min_y = 150
            # max_x = min_x + num_of_drawing_tiles * drawing_tile_size
            # max_y = min_y + num_of_drawing_tiles * drawing_tile_size
            
            width = num_of_drawing_tiles * drawing_tile_size
            height = num_of_drawing_tiles * drawing_tile_size
            
            capture_rect = pygame.Rect(min_x, min_y, width, height)
            
            drawing_surface = screen.subsurface(capture_rect).copy()
            
            now = datetime.now()
            now = now.strftime("%Y%m%d_%H%M%S")
                    
            pygame.image.save(drawing_surface, f'drawing_{now}.png')
            
            add_transparency_channel(f'drawing_{now}.png')
            
            # print('Image saved!')
            msg_label_surface, msg_label_rect = reset_msg_label('Image saved!')
            capture_drawing = False

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
