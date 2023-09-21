import ChessClasses as ch
import ChessFunctions as chf
import ChessPieceBehavior as chpb
import pygame
from sys import exit
import math
import os

# Pygame init
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 500, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # surface
pygame.display.set_caption("Chess!")
ch.screen = SCREEN

thisScriptDirectory = os.path.realpath(__file__)
thisScriptDirectory = os.path.split(thisScriptDirectory)[0]
pieceSpriteDirectory = os.path.join(thisScriptDirectory, "Pieces")

# Game Settings
FPS = 60
TILE_SIZE = 60
TILE_COLLIDER_PADDING = 10

PIECE_SIZE = TILE_SIZE
SELECTED_PIECE_SIZE = 80

# Graphical Settings
TEXT_FONT_1 = pygame.font.SysFont("Arial",30)
TEXT_FONT_2 = pygame.font.SysFont("Arial",20)

BACKGROUND_COLOR = (100,100,100)
GRIDBORDER_COLOR = (50,50,50)
TEXT_COLOR = (255,255,255)
TILE_HIGHLIGHT_COLOR = (50,150,0)

WHITE_TILE = (255,255,255)
BLACK_TILE = (90,100,90)



# Sounds

PIECE_PICK_UP_SOUND = pygame.mixer.Sound(os.path.join(thisScriptDirectory, "Sounds", "Abstract1.ogg"))
PIECE_RELEASE_SOUND = pygame.mixer.Sound(os.path.join(thisScriptDirectory, "Sounds", "Abstract2.ogg"))
PIECE_PLACE_SOUND = pygame.mixer.Sound(os.path.join(thisScriptDirectory, "Sounds", "Abstract2.ogg"))

# Global Variables
selectedObj = None
selectedTileCoords = None

# Game Functions
def draw_window():
    SCREEN.fill(BACKGROUND_COLOR)
    ch.draw_objects()

    pygame.display.update()

def start():
    chf.generate_board((10,10))
    chf.generate_pieces()
    #chf.generate_piece("Black_King.png",(0,0))

def main():
    global selectedObj

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        mousePos = pygame.mouse.get_pos()
        #
        chf.drag_select_obj(selectedObj, mousePos) 
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN: # MOUSE CLICK
                match event.button:
                    case 1: # Left Click
                        # Pick up piece
                        hitTile = ch.check_collision(event.pos,0)
                        if hitTile is not None:
                            selectedTileCoords = hitTile.data
                            selectedObj = hitTile.tag
                            if selectedObj is not None:
                                PIECE_PICK_UP_SOUND.play()
                                chpb.get_piece_valid_moves(selectedTileCoords)

                                #selectedObj.move_layer(3)
                                selectedObj.setSize((SELECTED_PIECE_SIZE,SELECTED_PIECE_SIZE))  

            if event.type == pygame.MOUSEBUTTONUP: # MOUSE Release
                match event.button:
                    case 1: # Left Click Release
                        if selectedObj is not None:
                            #selectedObj.move_layer(2)
                            selectedObj.setSize((PIECE_SIZE,PIECE_SIZE))  

                            targetTile = ch.check_collision(mousePos,0)
                            targetCoords = None
                            if targetTile is not None:
                                targetCoords = targetTile.data        
                            chf.attempt_move_piece(selectedTileCoords, targetCoords) # This function can handle a None input on targetTile        
                            chpb.unhighlight_all()    
                            chpb.currentValidTargets.clear()                           
                            selectedObj = None 
        draw_window()
    pygame.quit()

# Game Start
if __name__ == "__main__": # Ensures that the game is run only when this file is run directly
    start()
    main()