import pygame

class Bullet:
    def __init__(self, x, y, speed_x, speed_y, size=(30, 30)):
        self.x = x
        self.y = y
        self.speed_x = speed_x  # Tốc độ di chuyển theo hướng X
        self.speed_y = speed_y  # Tốc độ di chuyển theo hướng Y
        self.image = pygame.image.load('src\\entity\\Data1\\skill.png')
        
        # Thay đổi kích thước ảnh
        self.image = pygame.transform.scale(self.image, size)  # Giảm kích thước ảnh
        self.rect = self.image.get_rect(center=(x, y))  # Cập nhật vị trí của ảnh

    def update(self):
        # Di chuyển theo hướng X và Y
        self.x += self.speed_x * 10  # 10 là tốc độ bắn
        self.y += self.speed_y * 10  # 10 là tốc độ bắn
        self.rect.center = (self.x, self.y)  # Cập nhật vị trí của rect

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)
