import pygame



class WhiteKing:
    def __init__(self, sq_sz, surface):
        self.sprite = pygame.image.load("sprites/whiteKing.png")
        self.sq_sz = sq_sz
        self.surface = surface
        self.col = 0
        self.row = 0
        self.offset = (sq_sz - self.sprite.get_width()) // 2

    def init(self, white):
        if white:
            self.col = 4
            self.row = 7
            return self.surface.blit(self.sprite, (self.col * self.sq_sz + self.offset, 
                self.row * self.sq_sz + self.offset))
        else:
            self.col = 3
            self.row = 0
            return self.surface.blit(self.sprite, (self.col * self.sq_sz + self.offset,
                self.row * self.sq_sz + self.offset))

    def draw_piece(self):
        return self.surface.blit(self.sprite, (self.col * self.sq_sz + self.offset,
            self.row * self.sq_sz + self.offset))


class WhiteBishop:
    def __init__(self, sq_sz, surface):
        self.sprite = pygame.image.load("sprites/whiteBishop.png")
        self.sq_sz = sq_sz
        self.col = 2
        self.row = 7
        self.offset = (sq_sz - self.sprite.get_width()) // 2
        self.surface = surface

    def draw_piece(self):
        return self.surface.blit(self.sprite, (self.col * self.sq_sz + self.offset,
            self.row * self.sq_sz + self.offset))

class WhitePawn:        
    def __init__(self, sq_sz, surface):
        self.sprite = pygame.image.load("sprites/whitePawn.png")
        self.sq_sz = sq_sz
        self.col = 0
        self.row = 0
        self.offset = (sq_sz - self.sprite.get_width()) // 2
        self.surface = surface

class BlackKing:
    def __init__(self, sq_sz, surface):
        self.sprite = pygame.image.load("sprites/blackKing.png")
        self.sq_sz = sq_sz
        self.col = 0
        self.row = 0
        self.offset = (sq_sz - self.sprite.get_width()) // 2
        self.surface = surface

    def init(self, white):
        if white:
            self.col = 4
            self.row = 0
            return self.surface.blit(self.sprite, (self.col * self.sq_sz + self.offset, 
                self.row * self.sq_sz + self.offset))
        else:
            self.col = 3
            self.row = 7
            return self.surface.blit(self.sprite, (self.col * self.sq_sz + self.offset,
                self.row * self.sq_sz + self.offset))

    def draw_piece(self):
        return self.surface.blit(self.sprite, (self.col * self.sq_sz + self.offset,
            self.row * self.sq_sz + self.offset))
