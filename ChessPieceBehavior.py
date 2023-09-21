import ChessClasses as ch
import ChessFunctions as chf
import Chess as c
import pygame
import math
import os

# Global Variables
allRays = []
currentValidTargets = []

class Ray: 
    def __init__(self, velocity, pos, side, limit=None, mode=None):
        self.velocity = velocity
        self.side = side
        if limit is None:
            limit = 64
        self.limit = limit
        self.pos = pos
        if mode is None:
            mode = 0
            # 0 - Both movement and capturing
            # 1 - movement only 
            # 2 - capture only
        self.mode = mode
        allRays.append(self)

    def destroy(self):
        allRays.remove(self)

    def update_location(self):
        currentX, currentY = self.pos    
        newX = currentX + self.velocity[0]
        newY = currentY + self.velocity[1]

        # Conditions for immediate ray destruction
        # If limit is less than 1 
        if self.limit <= 0:
            self.destroy()
            return
        self.limit -= 1

        # If ray is outside
        if newX >= 8 or newX < 0 or newY >= 8 or newY < 0:
            self.destroy()
            return
        
        # If intersecting with another piece
        obstructingVirtualPiece = chf.get_virtual_piece((newX,newY))
        if obstructingVirtualPiece != " ":
            if self.mode != 1: # mode 1 means movement only
                # Gets piece side.  Valid target only if opposing side
                side = get_piece_side(obstructingVirtualPiece.piece)
                if side != self.side:
                    currentValidTargets.append((newX,newY))
                    highlight_tile((newX,newY))

            self.destroy()
            return
        elif self.mode == 2: # Ray is set to capture only, and lands on an empty tile => continue
            self.pos = (newX, newY)
            return

        # Updates ray if not destroyed
        self.pos = (newX, newY)
        highlight_tile(self.pos)
        currentValidTargets.append((newX,newY))
    
# Ray Functions
def update_rays():
    while (len(allRays) > 0):
        for ray in allRays:
            ray.update_location()

# Piece Ray functions
def rook_ray(startPos, side):
    ray_top = Ray((0,-1),startPos, side)
    ray_right = Ray((1,0),startPos, side)
    ray_bottom = Ray((0,1),startPos, side)
    ray_left = Ray((-1,0),startPos, side)
    update_rays()

def pawn_ray(startPos, side):
    x, y = startPos
    yDir = -1 # White pawn
    if side != "white":
        yDir = 1
    forwardLength = 1

    # Two moves if pawn hasn't moved
    if chf.virtualBoard[y][x].timesMoved == 0:
        forwardLength = 2
    ray_top = Ray((0, yDir),startPos, side, forwardLength, 1)
    
    # Capturing rays
    ray_left = Ray((-1, yDir),startPos, side, 1, 2)
    ray_right = Ray((1, yDir),startPos, side, 1, 2)

    #
    update_rays()

def bishop_ray(startPos, side):
    ray_top_left = Ray((-1,-1),startPos, side)
    ray_top_right = Ray((1,-1),startPos, side)
    ray_bottom_left = Ray((-1,1),startPos, side)
    ray_bottom_right = Ray((1,1),startPos, side)
    update_rays()

def queen_ray(startPos, side):
    ray_top = Ray((0,-1),startPos, side)
    ray_right = Ray((1,0),startPos, side)
    ray_bottom = Ray((0,1),startPos, side)
    ray_left = Ray((-1,0),startPos,side)
    ray_top_left = Ray((-1,-1),startPos, side)
    ray_top_right = Ray((1,-1),startPos, side)
    ray_bottom_left = Ray((-1,1),startPos, side)
    ray_bottom_right = Ray((1,1),startPos, side)
    update_rays()

def king_ray(startPos, side):
    ray_top = Ray((0,-1),startPos, side, 1)
    ray_right = Ray((1,0),startPos, side, 1)
    ray_bottom = Ray((0,1),startPos, side, 1)
    ray_left = Ray((-1,0),startPos, side, 1)
    ray_top_left = Ray((-1,-1),startPos, side, 1)
    ray_top_right = Ray((1,-1),startPos, side, 1)
    ray_bottom_left = Ray((-1,1),startPos, side, 1)
    ray_bottom_right = Ray((1,1),startPos, side, 1)
    update_rays()

def knight_ray(startPos, side):
    ray_top_left = Ray((1,-2),startPos, side, 1)
    ray_top_right = Ray((-1,-2),startPos, side, 1)
    ray_right_top = Ray((2,-1),startPos, side, 1)
    ray_right_bottom = Ray((2,1),startPos, side, 1)
    ray_left_top = Ray((-2,-1),startPos, side, 1)
    ray_left_bottom = Ray((-2,1),startPos, side, 1)
    ray_bottom_left = Ray((-1,2),startPos, side, 1)
    ray_bottom_right = Ray((1,2),startPos, side, 1)
    update_rays()


# Game Functions
def get_piece_side(piece):
    if piece == " ":
        return

    whitePieces = ['♔', '♕', '♖', '♗', '♘', '♙']
    #blackPieces = ['♚', '♛', '♜', '♝', '♞', '♟']
    # If not white and not empty, then the piece is black. 

    if piece in whitePieces:
        return "white"
    return "black"

def get_piece_valid_moves(coords):
    x, y = coords
    piece = chf.virtualBoard[y][x].piece
    
    match piece:
        case "♔":
            king_ray(coords, "white")
        case "♕":
            queen_ray(coords, "white")
        case "♖":
            rook_ray(coords, "white")
        case "♗":
            bishop_ray(coords, "white")
        case "♘":
            knight_ray(coords, "white")
        case "♙":
            pawn_ray(coords, "white")
        case "♚":
            king_ray(coords, "black")
        case "♛":
            queen_ray(coords, "black")
        case "♜":
            rook_ray(coords, "black")
        case "♝":
            bishop_ray(coords, "black")
        case "♞":
            knight_ray(coords, "black")
        case "♟":
            pawn_ray(coords, "black")

# Highlighting functions
def highlight_tile(tileCoords):

    # Makes the highlight size bigger if there is a piece there
    highlightSize = c.TILE_SIZE
    tileVirtualPiece = chf.get_virtual_piece(tileCoords)
    if tileVirtualPiece == " ":
        highlightSize /= 4
    

    # Creates highlight
    highlightRect = pygame.Rect(0, 0, highlightSize, highlightSize)
    highlightRenderer = ch.RectRenderer(highlightRect, c.TILE_HIGHLIGHT_COLOR, 0)
    highlight = ch.GameObject(highlightRenderer, None, "", 1)

    # Places on tile
    targetTile = chf.allChessTiles[tileCoords[1]][tileCoords[0]]
    highlight.setPos_center(targetTile.get_center())

def unhighlight_all():
    ch.allGameObjects[1].clear()
    #for ray in allRays:
    #    ray.destroy()

