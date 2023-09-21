import ChessClasses as ch
import ChessPieceBehavior as chpb
import Chess as c
import pygame
import math
import os

class ChessPiece:
     def __init__(self, piece, timesMoved):
          self.piece = piece
          self.timesMoved = timesMoved
          allChessPieces.append(self)

# This script is for the chess game itself.  Things such as the board, initializing the board etc.

allChessPieces = []
allChessTiles = []
virtualBoard = []
# Chess Board generation
def generate_board(startPos = (0,0)):
    tileX, tileY = startPos
    newTileRow = []
    virtualBoardRow = []
    for y in range(8):
        for x in range(8):
            # Determines Color
            tileColor = c.WHITE_TILE
            if ((x+y) % 2 != 0):
                tileColor = c.BLACK_TILE

            # Creates Tile Collider
            halfPadding = c.TILE_COLLIDER_PADDING/2
            tileColliderSize = c.TILE_SIZE - c.TILE_COLLIDER_PADDING
            tileColliderRect = pygame.Rect(tileX+halfPadding,tileY+halfPadding, tileColliderSize, tileColliderSize)

            # Creates tile
            tileRect = pygame.Rect(tileX,tileY,c.TILE_SIZE,c.TILE_SIZE)
            tileRenderer = ch.RectRenderer(tileRect,tileColor,0)
            tile = ch.GameObject(tileRenderer,tileColliderRect, None , 0, (x,y))

            # Appends tile to new tile row
            newTileRow.append(tile)
            virtualBoardRow.append(" ")

            # Moves tile placer
            tileX += c.TILE_SIZE
        tileY += c.TILE_SIZE
        tileX = startPos[0]

        # Adds new row to allChessTiles
        allChessTiles.append(newTileRow.copy())
        virtualBoard.append(virtualBoardRow.copy())
        newTileRow.clear()
        virtualBoardRow.clear()

def generate_pieces():
    # Black Pieces
    for i in range(8):
        generate_piece("Black_Pawn.png", "♟", (i,1))

    generate_piece("Black_Rook.png", "♜", (0,0))
    generate_piece("Black_Rook.png", "♜", (7,0))

    generate_piece("Black_Knight.png", "♞", (1,0))
    generate_piece("Black_Knight.png", "♞", (6,0))

    generate_piece("Black_Bishop.png", "♝", (2,0))
    generate_piece("Black_Bishop.png", "♝", (5,0))

    generate_piece("Black_King.png", "♚", (4,0))
    generate_piece("Black_Queen.png", "♛", (3,0))

    # White Pieces
    for i in range(8):
        generate_piece("White_Pawn.png", "♙", (i,6))

    generate_piece("White_Rook.png", "♖", (0,7))
    generate_piece("White_Rook.png", "♖", (7,7))

    generate_piece("White_Knight.png", "♘", (1,7))
    generate_piece("White_Knight.png", "♘", (6,7))

    generate_piece("White_Bishop.png", "♗", (2,7))
    generate_piece("White_Bishop.png", "♗", (5,7))

    generate_piece("White_King.png", "♔", (4,7))
    generate_piece("White_Queen.png", "♕", (3,7))

def generate_piece(pieceImage, pieceType, coords):
    rect1 = pygame.Rect(0,0,c.PIECE_SIZE,c.PIECE_SIZE)
    imgPath = os.path.join(c.pieceSpriteDirectory,pieceImage)
    newRenderer = ch.ImageRenderer(rect1,imgPath)
    piece = ch.GameObject(newRenderer, None, 0, 2,coords) # layer 2 reserved for pieces

    # Places piece on virtual board
    virtualBoard[coords[1]][coords[0]] = ChessPiece(pieceType,0) #pieceType

    # Places Piece
    x, y = coords
    targetTile = allChessTiles[y][x]
    targetTile.tag = piece
    place_piece(piece,targetTile)

def place_piece(piece, tile): # Only changes the physical location of the GameObjects and nothing else
    if tile is not None and piece is not None:
            piece.setPos_center(tile.get_center())
            c.PIECE_PLACE_SOUND.play() 
    elif tile is not None:
            c. PIECE_RELEASE_SOUND.play()  

def reset_piece(startCoords):
    startX, startY = startCoords
    startTile = allChessTiles[startY][startX]
    c.selectedObj = None
    startTile.tag.setPos_center(startTile.get_center())
    c.PIECE_RELEASE_SOUND.play()

def attempt_move_piece(startCoords, targetCoords):
    # If no target -> Reset
    if targetCoords is None:
        reset_piece(startCoords)
        return
    
    # Checks if piece can move there
    if targetCoords not in chpb.currentValidTargets:
         reset_piece(startCoords)
         return
    
    # If successful
    move_piece(startCoords, targetCoords)


def move_piece(startCoords, targetCoords):
    
    # Defines coordinates
    startX, startY = startCoords
    targetX, targetY = targetCoords

    # Handles virtual board
    virtualPiece = virtualBoard[startY][startX]
    if virtualPiece == ' ':
         return # Stops function if there is no piece to be moved
    
    # Erase the start virtual tile first, so that it doesn't end up empty when placing on the same tile
    virtualBoard[startY][startX] = " "
    virtualBoard[targetY][targetX] = virtualPiece
    
    # Defines tile objects
    targetTile = allChessTiles[targetY][targetX]
    startTile = allChessTiles[startY][startX]
    startPiece = startTile.tag

    # Moves piece GameObject
    startPiece.setPos_center(targetTile.get_center())
    c.PIECE_PLACE_SOUND.play() 

    # Removes piece on target tile if there is something there
    if targetTile.tag is not None and targetTile.tag is not startTile.tag:
        targetTile.tag.destroy()

    # Moves object in the tile tags
    startTile.tag = None
    targetTile.tag = startPiece

    # Sets tag
    # We need to track how many times the piece has moved to accomodate for en passant
    virtualBoard[targetY][targetX].timesMoved += 1
   
    print_board()

# Click and Drag
def drag_select_obj(selectedObj, mousePos):
    if selectedObj is not None:     
        selectedObj.setPos_center((mousePos[0], mousePos[1]))

# Getting info from the board
def print_board():
     virtualBoardString = []
     for row in virtualBoard:
            stringRow = []
            for tileObj in row:
                if isinstance(tileObj, ChessPiece):
                    stringRow.append(tileObj.piece)
                else:
                    stringRow.append(tileObj)
            print(stringRow)
            stringRow.clear()
        


def get_virtual_piece(coords):
     x, y = coords
     return virtualBoard[y][x]

# Other info

# Getting other info


