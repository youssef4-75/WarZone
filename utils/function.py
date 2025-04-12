import pygame as pg 
from icecream import ic

from utils.var import GRID_SIZER, GRID_SIZEC, WIDTH, HEIGHT, MARGX, MARGY, CIRCLE_SIZE


def gridify(x, y, rows=GRID_SIZER,
            cols=GRID_SIZEC, total_width=WIDTH,
            total_height=HEIGHT):
    """
    Convert a coordinate (x, y) to a grid position based on the number of rows and columns.
    """
    cell_width = total_width // cols
    cell_height = total_height // rows
    grid_x = x // cell_width
    grid_y = y // cell_height
    return grid_x, grid_y



def draw_grid(screen, rows= GRID_SIZER, cols=GRID_SIZEC, 
                width=None, height=None,
                color=(255, 255, 255), 
                line_width=3, offset_x=MARGX, offset_y=MARGY):
    """
    Draw a grid on the given pygame surface.
    
    Parameters:
        screen (pygame.Surface): The surface to draw on
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
        width (int): Total width of the grid in pixels
        height (int): Total height of the grid in pixels
        color (tuple): RGB color of the grid lines (default: white)
        line_width (int): Width of the grid lines in pixels (default: 1)
    """
    # ic()
    if width is None: width = WIDTH - offset_x * 2 
    if height is None: height = HEIGHT - offset_y * 2
    # Calculate cell dimensions
    cell_width = width // cols
    cell_height = height // rows
    
    # Draw vertical lines
    for x in range(0, width + 1, cell_width):
        pg.draw.line(screen, color, (x + offset_x, offset_y), 
                    (x + offset_x, height + offset_y), line_width)
    
    # Draw horizontal lines
    for y in range(0, height + 1, cell_height):
        pg.draw.line(screen, color, (offset_x, y + offset_y),
                    (width + offset_x, y + offset_y), line_width)


def color_cell(surface, col, row, color, 
               cols=GRID_SIZEC, rows=GRID_SIZER, 
               width=None, height=None,
               offset_x=MARGX, offset_y=MARGY):
    """
    Color a grid cell without needing explicit cell size
    
    Args:
        surface: Pygame surface to draw on
        col: Column index (0-based)
        row: Row index (0-based)
        cols: Total columns in grid
        rows: Total rows in grid
        total_width: Total grid width in pixels
        total_height: Total grid height in pixels  
        color: Fill color (RGB tuple)
    """
    
    if width is None: width = WIDTH - offset_x * 2 
    if height is None: height = HEIGHT - offset_y * 2
    
    if col < 0 or col >= cols or row < 0 or row >= rows:
        return
    
    cell_width = width // cols
    cell_height = height // rows
    
    x = col * cell_width
    y = row * cell_height
    
    pg.draw.rect(surface, color, (x + offset_x, y + offset_y, cell_width, cell_height))



def draw_cell_circle(surface, col, row,    
                    cols=GRID_SIZEC, rows=GRID_SIZER, 
                    width=None, height=None,
                    offset_x=MARGX, offset_y=MARGY):
    """
    Draw a black circle centered in a grid cell, accounting for grid offsets
    
    Args:
        surface: Pygame surface to draw on
        col: Column index (0-based)
        row: Row index (0-based)
        cols: Total columns in grid
        rows: Total rows in grid
        total_width: Total grid width in pixels
        total_height: Total grid height in pixels
        offset_x: Horizontal offset from left edge
        offset_y: Vertical offset from top edge
    """
    
    if width is None: width = WIDTH - offset_x * 2 
    if height is None: height = HEIGHT - offset_y * 2

    if col < 0 or col >= cols or row < 0 or row >= rows:
        return
    
    cell_width = width // cols
    cell_height = height // rows
    
    # Calculate cell position with offset
    x = offset_x + col * cell_width
    y = offset_y + row * cell_height
    
    # Calculate center of cell
    center_x = x + cell_width // 2
    center_y = y + cell_height // 2
    
    # Draw circle with radius 90% of half the smallest dimension
    radius = int(CIRCLE_SIZE * min(cell_width, cell_height) // 2)
    pg.draw.circle(surface, (0, 0, 0), (center_x, center_y), radius)


def draw_advanced_background(screen, background_surface, 
                           position=(0, 0), 
                           scale_mode=None, 
                           opacity=255,
                           blend_mode=0):
    """
    Enhanced background drawing with more options
    
    Args:
        scale_mode: None/"fit"/"fill"/"stretch" (background scaling behavior)
        opacity: 0-255 transparency value
        blend_mode: pygame blend mode constant
    """
    bg = background_surface.copy()
    
    # Apply opacity if needed
    if opacity < 255:
        bg.fill((255, 255, 255, opacity), None, pg.BLEND_RGBA_MULT)
    
    # Handle scaling
    if scale_mode == "fit":
        # Scale preserving aspect ratio (letterbox)
        ratio = min(screen.get_width()/bg.get_width(), 
                   screen.get_height()/bg.get_height())
        new_size = (int(bg.get_width()*ratio), int(bg.get_height()*ratio))
        bg = pg.transform.smoothscale(bg, new_size)
    elif scale_mode == "fill":
        # Scale and crop to fill screen
        ratio = max(screen.get_width()/bg.get_width(), 
                   screen.get_height()/bg.get_height())
        new_size = (int(bg.get_width()*ratio), int(bg.get_height()*ratio))
        bg = pg.transform.smoothscale(bg, new_size)
    elif scale_mode == "stretch":
        # Stretch to exact screen dimensions
        bg = pg.transform.smoothscale(bg, screen.get_size())
    
    # Calculate position
    if scale_mode in ("fit", "fill"):
        pos = ((screen.get_width() - bg.get_width()) // 2,
               (screen.get_height() - bg.get_height()) // 2)
    else:
        pos = position
    
    # Blit with optional blend mode
    screen.blit(bg, pos, special_flags=blend_mode)