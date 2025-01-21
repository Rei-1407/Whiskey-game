import pygame
import random
import tkinter as tk
from tkinter import messagebox
import sys
import os
import math
from PIL import Image, ImageTk
from Leaderboard import Leaderboard
from Player import Player
from Bullet import Bullet
from Enemy import Enemy, StrongEnemy, FastEnemy
from AmmoBox import AmmoBox

class GamePanel:
    def update(self):
        self.elapsed_time += 1 / self.FPS  # Cập nhật thời gian trôi qua
        # Cập nhật đạn, kẻ địch, và kiểm tra va chạm
        for bullet in self.player.bullets:
            bullet.update()

        for enemy in self.enemies:
            enemy.update(self.player)

        # Kiểm tra va chạm giữa đạn và kẻ địch
        surviving_bullets = []  # Create a new list to store bullets that survived collisions
        for bullet in self.player.bullets:
            bullet_collided = False
            for enemy in self.enemies[:]:
                if abs(bullet.x - enemy.x) < self.tile_size and abs(bullet.y - enemy.y) < self.tile_size:
                    enemy.take_damage(self.enemies)  
                    self.score += 1  # Tăng điểm
                    bullet_collided = True
                    break  # Không cần kiểm tra các quái khác

            if not bullet_collided:
                surviving_bullets.append(bullet)

        self.player.bullets = surviving_bullets  # Update the player's bullets with the surviving bullets

        # Kiểm tra va chạm giữa người chơi và hộp đạn
        for ammo_box in self.ammo_boxes[:]:
            if ammo_box.is_picked_up(self.player):
                self.ammo_boxes.remove(ammo_box)
                self.pick_sound.play()
                self.player.ammo += 5  # Thêm 5 viên đạn khi nhặt được hộp đạn

        # Tạo hộp đạn mới sau mỗi khoảng thời gian
        self.ammo_box_timer += 1
        if self.ammo_box_timer >= self.ammo_box_spawn_rate:
            self.ammo_boxes.append(AmmoBox(self))
            self.ammo_box_timer = 0  # Reset timer

        # Sinh ra kẻ địch mới sau mỗi khoảng thời gian
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_rate:
            if self.score >= 30:
                enemy_type = random.choice(['normal', 'fast', 'strong'])  # Chọn loại quái ngẫu nhiên
                while True:
                    if enemy_type == 'normal':
                        new_enemy = Enemy(self)
                    elif enemy_type == 'fast':
                        new_enemy = FastEnemy(self)
                    elif enemy_type == 'strong':
                        new_enemy = StrongEnemy(self)

                    # Kiểm tra khoảng cách với người chơi
                    if abs(new_enemy.x - self.player.x) >= self.tile_size * 2 and abs(new_enemy.y - self.player.y) >= self.tile_size * 2:
                        self.enemies.append(new_enemy)
                        break  # Thoát vòng lặp khi vị trí hợp lệ
            elif self.score >= 10:
                enemy_type = random.choice(['normal', 'fast'])  # Chọn loại quái ngẫu nhiên
                while True:
                    if enemy_type == 'normal':
                        new_enemy = Enemy(self)
                    elif enemy_type == 'fast':
                        new_enemy = FastEnemy(self)

                    # Kiểm tra khoảng cách với người chơi
                    if abs(new_enemy.x - self.player.x) >= self.tile_size * 2 and abs(new_enemy.y - self.player.y) >= self.tile_size * 2:
                        self.enemies.append(new_enemy)
                        break  # Thoát vòng lặp khi vị trí hợp lệ
            
            else:
                while True:
                    new_enemy = Enemy(self)

                    # Kiểm tra khoảng cách với người chơi
                    if abs(new_enemy.x - self.player.x) >= self.tile_size * 2 and abs(new_enemy.y - self.player.y) >= self.tile_size * 2:
                        self.enemies.append(new_enemy)
                        break  # Thoát vòng lặp khi vị trí hợp lệ

            self.enemy_spawn_timer = 0  # Reset timer
            self.enemy_spawn_rate = max(50, self.enemy_spawn_rate - 5)  # Giảm thời gian giữa các lần sinh

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        self.player.draw(self.screen)
        for enemy in self.enemies:
            if isinstance(enemy, StrongEnemy) and self.strong_enemy_image:
                self.screen.blit(self.strong_enemy_image, (enemy.x, enemy.y))
            elif isinstance(enemy, FastEnemy) and self.fast_enemy_image:
                self.screen.blit(self.fast_enemy_image, (enemy.x, enemy.y))
            else:
                enemy.draw(self.screen)

        for ammo_box in self.ammo_boxes:
            ammo_box.draw(self.screen)

        # Draw background for score and ammo info
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, 220, 90))
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, 220, 90), 2)

        font = pygame.font.SysFont('Nunito', 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        ammo_text = font.render(f"Ammo: {self.player.ammo}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(ammo_text, (20, 50))

        # Draw background for time info
        time_bg_width = 200
        time_bg_height = 60
        time_bg_x = (self.screen_width - time_bg_width) // 2
        time_bg_y = 10
        pygame.draw.rect(self.screen, (0, 0, 0), (time_bg_x, time_bg_y, time_bg_width, time_bg_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (time_bg_x, time_bg_y, time_bg_width, time_bg_height), 2)

        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        time_text = f"{minutes:02}:{seconds:02}"
        time_font = pygame.font.SysFont('Nunito', 36)
        time_surface = time_font.render(time_text, True, (255, 255, 255))
        self.screen.blit(time_surface, (time_bg_x + (time_bg_width - time_surface.get_width()) // 2, time_bg_y + 10))

        pygame.display.flip()

    def __init__(self, main_menu):
        pygame.init()
        self.main_menu = main_menu
        self.leaderboard = Leaderboard()
        self.original_tile_size = 16
        self.scale = 3
        self.tile_size = self.original_tile_size * self.scale
        self.max_screen_col = 32
        self.max_screen_row = 18
        self.screen_width = self.tile_size * self.max_screen_col
        self.screen_height = self.tile_size * self.max_screen_row
        self.FPS = 60
        self.enemies = []  # Đặt lên đây trước khi sử dụng
        self.ammo_boxes = []  # Đặt lên đây trước khi sử dụng
        self.random = random.Random()
        self.frame_count = 0
        self.score = 0
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False  # Trạng thái tạm dừng
        self.elapsed_time = 0  # Thời gian đã trôi qua tính bằng giây

        # Initialize player
        self.player = Player(self)

        # Load background
        try:
            self.background = pygame.image.load("src\\game\\Data\\bg.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            print("Error loading background image")
            self.background = None

        # Load and start background sound
        pygame.mixer.init()
        try:
            self.background_sound = pygame.mixer.Sound("src\\game\\Data\\background.wav")
            self.background_sound.play(-1)  # -1 for loop
        except:
            print("Error loading background sound")

        # Load and start skill sound
        try:
            self.skill_sound = pygame.mixer.Sound("src\\game\\Data\\skill.WAV")
        except:
            print("Error loading skill sound")
            self.skill_sound = None

        # Load and start pick sound
        try:
            self.pick_sound = pygame.mixer.Sound("src\\game\\Data\\pick.wav")
        except:
            print("Error loading pick sound")
            self.pick_sound = None

        # Initialize game over dialog (Tkinter)
        self.root = tk.Tk()
        self.root.withdraw()  # Hide Tkinter window initially


        # Tạo kẻ địch ban đầu
        self.enemies.append(Enemy(self))  # Đặt sau khi đã khởi tạo self.enemies

        # Tạo hộp đạn ban đầu
        self.ammo_boxes.append(AmmoBox(self))  # Đặt sau khi đã khởi tạo self.ammo_boxes

        # Initialize ammo box timer and spawn rate
        self.ammo_box_timer = 0
        self.ammo_box_spawn_rate = 200  # Adjust spawn rate as needed (in frames)

        # Initialize enemy spawn timer and spawn rate
        self.enemy_spawn_timer = 0
        self.enemy_spawn_rate = 100  # Adjust spawn rate as needed (in frames)  # Thời gian đếm để sinh kẻ địch mới

        try:
            self.strong_enemy_image = pygame.image.load("src\\game\\Data\\strong_enemy.png")
            self.strong_enemy_image = pygame.transform.scale(self.strong_enemy_image, (self.tile_size, self.tile_size))
        except:
            print("Error loading strong enemy image")
            self.strong_enemy_image = None

        try:
            self.fast_enemy_image = pygame.image.load("src\\game\\Data\\fast_enemy.png")
            self.fast_enemy_image = pygame.transform.scale(self.fast_enemy_image, (self.tile_size, self.tile_size))
        except:
            print("Error loading fast enemy image")
            self.fast_enemy_image = None

    def start_game(self):
        while self.running:
            self.handle_events()  # Xử lý sự kiện

            if not self.paused:  # Chỉ cập nhật và vẽ nếu không tạm dừng
                self.update()         # Cập nhật logic trò chơi
                self.draw()           # Vẽ màn hình
                self.check_collision_with_enemy()  # Kiểm tra va chạm
            else:
                self.draw_pause_screen()  # Vẽ màn hình tạm dừng

            self.clock.tick(self.FPS)
        
    def draw_pause_screen(self):    
        pause_surface = self.screen.copy()  # Chụp lại màn hình hiện tại
        font = pygame.font.SysFont('Nunito', 48)

        question_text = font.render("Do you want to exit?", True, (255, 255, 255))
        self.screen.blit(pause_surface, (0, 0))
        self.screen.blit(question_text, ((self.screen_width - question_text.get_width()) // 2, self.screen_height // 3))

        yes_button = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2, 100, 50)
        no_button = pygame.Rect(self.screen_width // 2 + 20, self.screen_height // 2, 100, 50)

        pygame.draw.rect(self.screen, (0, 255, 0), yes_button)
        pygame.draw.rect(self.screen, (255, 0, 0), no_button)

        button_font = pygame.font.SysFont('Nunito', 36)
        yes_text = button_font.render("YES", True, (0, 0, 0))
        no_text = button_font.render("NO", True, (0, 0, 0))

        self.screen.blit(yes_text, (yes_button.x + (yes_button.width - yes_text.get_width()) // 2,
                                    yes_button.y + (yes_button.height - yes_text.get_height()) // 2))
        self.screen.blit(no_text, (no_button.x + (no_button.width - no_text.get_width()) // 2,
                                   no_button.y + (no_button.height - no_text.get_height()) // 2))

        pygame.display.flip()

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.paused = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(event.pos):
                        self.running = False
                        self.paused = False
                        sys.exit()
                        return
                    elif no_button.collidepoint(event.pos):
                        self.paused = False
                        return


    def handle_events(self):
        keys = pygame.key.get_pressed()  # Lấy trạng thái của tất cả các phím

        # Gọi phương thức move từ Player để di chuyển nhân vật (nếu không bị tạm dừng)
        if not self.paused:
            self.player.move(keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Nếu bấm phím Esc
                    self.paused = not self.paused  # Chuyển đổi trạng thái tạm dừng

            # Kiểm tra sự kiện click chuột trái (chỉ khi không tạm dừng)
            if not self.paused and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 là mã nút cho chuột trái
                    self.skill_sound.play()
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí chuột trên màn hình
                    self.player.shoot(mouse_x, mouse_y)  # Truyền tọa độ chuột vào phương thức shoot

    def check_collision_with_enemy(self):
        # Đặt tỉ lệ phần trăm mà quái vật cần đè lên người chơi để game over
        collision_threshold = 0.6  # 1 - collision_threshold phần của kẻ địch

        # Duyệt qua tất cả kẻ địch và kiểm tra va chạm
        for enemy in self.enemies:
            # Kiểm tra nếu một phần của quái vật chạm vào người chơi
            if (abs(self.player.x - enemy.x) < self.tile_size * collision_threshold and
                abs(self.player.y - enemy.y) < self.tile_size * collision_threshold):
                self.game_over()  # Kết thúc trò chơi khi va chạm xảy ra

    def show_game_over_message(self):
        # Hiển thị hộp thoại Game Over
        messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
        sys.exit()  # Thoát chương trình hoàn toàn sau khi người dùng nhấn "OK"


    def game_over(self):
        # Hiển thị thông báo Game Over
        player_name = self.main_menu.player_name or "Unknown"
        player_code = self.main_menu.player_code or "0000"
        self.leaderboard.save_score(self.score, player_name, player_code)
        self.running = False
        #self.main_menu.deiconify()
        self.show_game_over_message()

        self.running = False  # Kết thúc vòng lặp game hiện tại
        # Ẩn cửa sổ game và quay lại menu chính
        
        

    def back_to_main_menu(self):
        # Trở lại menu chính
        print("Returning to Main Menu...")
        self.running = False  # Kết thúc vòng lặp game hiện tại

if __name__ == "__main__":
    # Khởi tạo GamePanel và bắt đầu trò chơi
    game_panel = GamePanel(None)  # Không cần menu chính và cửa sổ Tkinter
    game_panel.start_game()
