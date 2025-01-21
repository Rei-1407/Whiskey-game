import pygame
import math
from Bullet import Bullet

class Player:
    def __init__(self, game_panel):
        self.game_panel = game_panel  # Lưu trữ game_panel vào thuộc tính self.game_panel
        self.x = self.game_panel.screen_width // 2
        self.y = self.game_panel.screen_height // 2
        self.speed = 5
        self.ammo = 10
        self.bullets = []
        self.tile_size = self.game_panel.tile_size
        self.current_frame = 0  # Biến theo dõi frame hiện tại của animation
        self.last_frame_time = pygame.time.get_ticks()  # Thời gian lần cập nhật frame trước đó
        self.frame_interval = 100  # Interval (ms) giữa các lần thay đổi frame (tốc độ di chuyển)

        # Load ảnh động cho các hướng
        self.images_up = [pygame.image.load("src\\entity\\Data1\\boy_up_1.png"),
                          pygame.image.load("src\\entity\\Data1\\boy_up_2.png")]
        self.images_down = [pygame.image.load("src\\entity\\Data1\\boy_down_1.png"),
                            pygame.image.load("src\\entity\\Data1\\boy_down_2.png")]
        self.images_left = [pygame.image.load("src\\entity\\Data1\\boy_left_1.png"),
                            pygame.image.load("src\\entity\\Data1\\boy_left_2.png")]
        self.images_right = [pygame.image.load("src\\entity\\Data1\\boy_right_1.png"),
                             pygame.image.load("src\\entity\\Data1\\boy_right_2.png")]

        # Chuyển ảnh thành kích thước phù hợp
        self.images_up = [pygame.transform.scale(img, (self.tile_size, self.tile_size)) for img in self.images_up]
        self.images_down = [pygame.transform.scale(img, (self.tile_size, self.tile_size)) for img in self.images_down]
        self.images_left = [pygame.transform.scale(img, (self.tile_size, self.tile_size)) for img in self.images_left]
        self.images_right = [pygame.transform.scale(img, (self.tile_size, self.tile_size)) for img in self.images_right]

        # Gán ảnh mặc định (ví dụ: di chuyển xuống)
        self.image = self.images_down[0]

    def move(self, keys):
        current_time = pygame.time.get_ticks()  # Thời gian hiện tại
        
        # Cập nhật frame mỗi khoảng thời gian nhất định
        if current_time - self.last_frame_time >= self.frame_interval:
            self.current_frame = (self.current_frame + 1) % len(self.images_up)  # Thay đổi frame
            self.last_frame_time = current_time  # Cập nhật thời gian

        # Kiểm tra di chuyển chéo (cả lên/xuống và trái/phải)
        if keys[pygame.K_w] and keys[pygame.K_a] and self.x > 0 and self.y > 0:  # Di chuyển lên trái
            self.image = self.images_left[self.current_frame]
            self.x -= self.speed
            self.y -= self.speed
        elif keys[pygame.K_w] and keys[pygame.K_d] and self.x < self.game_panel.screen_width - self.tile_size and self.y > 0:  # Di chuyển lên phải
            self.image = self.images_right[self.current_frame]
            self.x += self.speed
            self.y -= self.speed
        elif keys[pygame.K_s] and keys[pygame.K_a] and self.x > 0 and self.y < self.game_panel.screen_height - self.tile_size:  # Di chuyển xuống trái
            self.image = self.images_left[self.current_frame]
            self.x -= self.speed
            self.y += self.speed
        elif keys[pygame.K_s] and keys[pygame.K_d] and self.x < self.game_panel.screen_width - self.tile_size and self.y < self.game_panel.screen_height - self.tile_size:  # Di chuyển xuống phải
            self.image = self.images_right[self.current_frame]
            self.x += self.speed
            self.y += self.speed

        # Di chuyển theo từng hướng đơn lẻ nếu không di chuyển chéo
        elif keys[pygame.K_w] and self.y > 0:  # Di chuyển lên
            self.image = self.images_up[self.current_frame]
            self.y -= self.speed
        elif keys[pygame.K_s] and self.y < self.game_panel.screen_height - self.tile_size:  # Di chuyển xuống
            self.image = self.images_down[self.current_frame]
            self.y += self.speed
        elif keys[pygame.K_a] and self.x > 0:  # Di chuyển trái
            self.image = self.images_left[self.current_frame]
            self.x -= self.speed
        elif keys[pygame.K_d] and self.x < self.game_panel.screen_width - self.tile_size:  # Di chuyển phải
            self.image = self.images_right[self.current_frame]
            self.x += self.speed

    def shoot(self, mouse_x, mouse_y):
        if self.ammo > 0:  # Only shoot if there's ammo
            # Calculate direction of bullet based on mouse click
            direction_x = mouse_x - self.x
            direction_y = mouse_y - self.y
            length = math.sqrt(direction_x**2 + direction_y**2)  # Get the distance to normalize
            direction_x /= length  # Normalize the vector
            direction_y /= length  # Normalize the vector

            # Create a new bullet
            bullet = Bullet(self.x + self.tile_size // 2, self.y + self.tile_size // 2, direction_x, direction_y)
            self.bullets.append(bullet)
            self.ammo -= 1  # Reduce ammo when shooting

    def draw(self, screen):
        # Draw the player image (animated)
        screen.blit(self.image, (self.x, self.y))

        # Draw the bullets
        for bullet in self.bullets:
            bullet.draw(screen)
