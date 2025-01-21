import pygame
import random

import pygame
import random

class Enemy:
    def __init__(self, game_panel):
        self.x = random.randint(0, game_panel.screen_width)
        self.y = random.randint(0, game_panel.screen_height)
        self.health = 100  # Máu hiện tại
        self.max_health = 100  # Máu tối đa
        self.speed = 1
        self.tile_size = game_panel.tile_size

        # Tải hình ảnh hoạt ảnh
        self.animations = {"down": [], "up": [], "left": [], "right": []}
        try:
            # Tải hình ảnh cho từng hướng với 2 bộ hoạt ảnh
            self.animations["down"] = [
                pygame.image.load(f"src\\entity\\Data\\enemy_down_1.png"),
                pygame.image.load(f"src\\entity\\Data\\enemy_down_2.png")
            ]
            self.animations["up"] = [
                pygame.image.load(f"src\\entity\\Data\\enemy_up_1.png"),
                pygame.image.load(f"src\\entity\\Data\\enemy_up_2.png")
            ]
            self.animations["left"] = [
                pygame.image.load(f"src\\entity\\Data\\enemy_left_1.png"),
                pygame.image.load(f"src\\entity\\Data\\enemy_left_2.png")
            ]
            self.animations["right"] = [
                pygame.image.load(f"src\\entity\\Data\\enemy_right_1.png"),
                pygame.image.load(f"src\\entity\\Data\\enemy_right_2.png")
            ]

            # Resize tất cả hình ảnh theo tile_size
            for direction in self.animations:
                self.animations[direction] = [
                    pygame.transform.scale(img, (self.tile_size, self.tile_size)) for img in self.animations[direction]
                ]
        except Exception as e:
            print("Error loading enemy images:", e)
            self.animations = {"down": [], "up": [], "left": [], "right": []}

        self.current_direction = "down"  # Hướng di chuyển ban đầu
        self.animation_index = 0  # Chỉ số hoạt ảnh
        self.animation_timer = 0  # Bộ đếm thời gian cho hoạt ảnh
        self.animation_speed = 10  # Tốc độ thay đổi khung hình

    def take_damage(self, enemies_list, damage=100):
        self.health -= damage
        if self.health <= 0:
            try:
                kill_sound = pygame.mixer.Sound("src\\game\\Data\\kill.wav")
                kill_sound.play()
            except Exception as e:
                print("Error loading kill sound:", e)
            enemies_list.remove(self)  # Xóa quái khi hết máu

    def draw_health_bar(self, screen, tile_size):
        bar_width = tile_size
        bar_height = 5
        health_ratio = self.health / self.max_health
        bar_x = self.x
        bar_y = self.y - bar_height - 5
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def update(self, player):
        # Di chuyển về phía người chơi
        if self.x < player.x:
            self.x += self.speed
            self.current_direction = "right"
        elif self.x > player.x:
            self.x -= self.speed
            self.current_direction = "left"

        if self.y < player.y:
            self.y += self.speed
            self.current_direction = "down"
        elif self.y > player.y:
            self.y -= self.speed
            self.current_direction = "up"

        # Cập nhật hoạt ảnh
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.animations[self.current_direction]:
                self.animation_index = (self.animation_index + 1) % len(self.animations[self.current_direction])

    def draw(self, screen):
        if self.animations[self.current_direction]:
            current_image = self.animations[self.current_direction][self.animation_index]
            screen.blit(current_image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.tile_size, self.tile_size))


class FastEnemy(Enemy):
    def __init__(self, game):
        super().__init__(game)
        self.speed = 2  # Tăng tốc độ di chuyển

        # Tải hoạt ảnh cho FastEnemy
        try:
            self.animations = {
                "down": [
                    pygame.image.load(f"src\\entity\\Data1\\enemy2_down_1.png"),
                    pygame.image.load(f"src\\entity\\Data1\\enemy2_down_2.png")
                ],
                "up": [
                    pygame.image.load(f"src\\entity\\Data1\\enemy2_up_1.png"),
                    pygame.image.load(f"src\\entity\\Data1\\enemy2_up_2.png")
                ],
                "left": [
                    pygame.image.load(f"src\\entity\\Data1\\enemy2_left_1.png"),
                    pygame.image.load(f"src\\entity\\Data1\\enemy2_left_2.png")
                ],
                "right": [
                    pygame.image.load(f"src\\entity\\Data1\\enemy2_right_1.png"),
                    pygame.image.load(f"src\\entity\\Data1\\enemy2_right_2.png")
                ]
            }

            # Resize tất cả hình ảnh theo tile_size
            for direction in self.animations:
                self.animations[direction] = [
                    pygame.transform.scale(img, (self.tile_size, self.tile_size)) for img in self.animations[direction]
                ]
        except Exception as e:
            print(f"Error loading FastEnemy images: {e}")
            self.animations = {"down": [], "up": [], "left": [], "right": []}


class StrongEnemy(Enemy):
    def __init__(self, game):
        super().__init__(game)
        self.health = 300  # Quái vật cần bị bắn 3 lần để tiêu diệt
        self.max_health = 300

        # Tải hoạt ảnh cho StrongEnemy
        try:
            self.animations = {
                "down": [
                    pygame.image.load(f"src\\entity\\Data1\\enemy3_down_1.png"),
                    pygame.image.load(f"src\\entity\\Data1\\enemy3_down_2.png")
                ],
                "up": [
                    pygame.image.load(f"src\\entity\\Data1\\enemy3_up_1.png"),
                    pygame.image.load(f"src\\entity\\Data1\\enemy3_up_2.png")
                ],
                "left": [
                    pygame.image.load(f"src\\entity\\Data1\\enemy3_left_1.png"),
                    pygame.image.load(f"src\\entity\\Data1\\enemy3_left_2.png")
                ],
                "right": [
                    pygame.image.load(f"src\\entity\\Data1\\enemy3_right_1.png"),
                    pygame.image.load(f"src\\entity\\Data1\\enemy3_right_2.png")
                ]
            }

            # Resize tất cả hình ảnh theo tile_size
            for direction in self.animations:
                self.animations[direction] = [
                    pygame.transform.scale(img, (self.tile_size, self.tile_size)) for img in self.animations[direction]
                ]
        except Exception as e:
            print("Error loading StrongEnemy images:", e)
            self.animations = {"down": [], "up": [], "left": [], "right": []}

    def draw(self, screen):
        # Vẽ hình ảnh hoạt ảnh nếu có
        if self.animations[self.current_direction]:
            current_image = self.animations[self.current_direction][self.animation_index]
            screen.blit(current_image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.tile_size, self.tile_size))

        # Gọi phương thức vẽ thanh máu
        self.draw_health_bar(screen, 48)
