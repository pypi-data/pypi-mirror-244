from pygame import sprite, draw, font, Rect


class Button(sprite.Sprite):
    def __init__(self, screen, position, text, size, colors, buttons):
        super().__init__()
        self.colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        self.font = font.SysFont("comicsans", size)
        self.text_render = self.font.render(text, 1, self.fg)
        self.text = text
        self.image = self.text_render
        self.x, self.y, self.w, self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.position = position
        self.update(screen)
        buttons.add(self)

    def update(self, screen):
        self.fg, self.bg = self.colors.split(" on ")
        margin = 15
        margin_y = 4
        draw.line(screen, (150, 150, 150), (self.x - margin, self.y - margin_y),
                  (self.x + margin + self.w, self.y - margin_y), 5)
        draw.line(screen, (150, 150, 150), (self.x - margin, self.y - margin_y),
                  (self.x - margin, self.y + margin_y + self.h), 5)
        draw.line(screen, (50, 50, 50), (self.x - margin, self.y + margin_y + self.h),
                  (self.x + margin + self.w, self.y + margin_y + self.h), 3)
        draw.line(screen, (50, 50, 50), (self.x + margin + self.w, self.y - margin_y),
                  (self.x + margin + self.w, self.y + margin_y + self.h), 3)
        draw.rect(screen, self.bg, (self.x - margin, self.y - margin_y, margin * 2 + self.w, 2 * margin_y + self.h))
        self.image = self.font.render(self.text, 1, self.fg)

