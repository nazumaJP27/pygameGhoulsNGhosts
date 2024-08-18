import pygame
import random
import string
import time
import os
import sys
from scripts.entities import PhysicsEntity, Weapon, Player, Spear, Sword, Axe, Arrow, Enemy, Zombie, Maddog, MaddogS, Ghost, Item, WeaponDrop, FireTorch
from scripts.utils import load_image, load_images, load_images_dict, show_hitbox, Animation


def main():
    opening_game = True
    if opening_game:
         Game().opening()


class Game:
    def __init__(self):
        pygame.init()

        #Create game window
        x_scale = 1.0
        WIDTH = 1200 * x_scale
        HEIGHT = 640 * x_scale
        WIDTH_d = WIDTH / 2 
        HEIGHT_d = HEIGHT / 2
        self.draw_borders = False

        pygame.display.set_caption("Pygame Ghouls 'n Ghosts") 
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        icon = pygame.image.load("assets/window_icon.png")
        pygame.display.set_icon(icon)
        
        self.display0 = pygame.Surface((WIDTH_d, HEIGHT_d))
        self.display = pygame.Surface((WIDTH_d, HEIGHT_d), pygame.SRCALPHA)

        self.screenshake = 0

        #Create a clock object to have controll over the speed witch the program runs
        self.clock = pygame.time.Clock() 

        self.chars = {
            "fontA": load_images_dict("fontA"),
            "fontB": load_images_dict("fontB"),
            "fontC": load_images_dict("fontC"),
            "fontD": load_images_dict("fontD"),
                }
        
        pygame.mixer.set_num_channels(32)

        self.sfx = {
            "capcom": pygame.mixer.Sound("assets/sfx/capcom.wav"),
            "by": pygame.mixer.Sound("assets/sfx/this_is_CS50.wav"),
            "select": pygame.mixer.Sound("assets/sfx/select.wav"),
            "change_selected": pygame.mixer.Sound("assets/sfx/change_selected.wav"),
            "controls": pygame.mixer.Sound("assets/sfx/controls.wav"),
            "game_start": pygame.mixer.Sound("assets/sfx/game_start.wav"),
            "new_horde": pygame.mixer.Sound("assets/sfx/new_horde.wav"),
            "jump": pygame.mixer.Sound("assets/sfx/jump.wav"),
            "arthur_death": pygame.mixer.Sound("assets/sfx/arthur_death.wav"),
            "arthur_hurt": pygame.mixer.Sound("assets/sfx/arthur_hurt.wav"),
            "arthur_get_hit": pygame.mixer.Sound("assets/sfx/arthur_get_hit.wav"),
            "spear_throw": pygame.mixer.Sound("assets/sfx/spear_throw.wav"),
            "axe_throw": pygame.mixer.Sound("assets/sfx/axe_throw.wav"),
            "sword_throw": pygame.mixer.Sound("assets/sfx/sword_throw.wav"),
            "pick_up": pygame.mixer.Sound("assets/sfx/pick_up.wav"),
            "enemy_hit": pygame.mixer.Sound("assets/sfx/enemy_hit.wav"),
            "enemy_killed": pygame.mixer.Sound("assets/sfx/enemy_killed.wav"),
            "ghost_killed": pygame.mixer.Sound("assets/sfx/ghost_killed.wav"),
            "ghost_swirl": pygame.mixer.Sound("assets/sfx/ghost_swirl.wav"),
            "item_drop": pygame.mixer.Sound("assets/sfx/item_drop.wav"), 
            "weapon_drop": pygame.mixer.Sound("assets/sfx/weapon_drop.wav"),
            "game_over": pygame.mixer.Sound("assets/sfx/game_over.wav"),
            "intro": pygame.mixer.Sound("assets/sfx/[INTRO]Haunted Graveyard.wav"),
            "music": pygame.mixer.Sound("assets/sfx/Haunted Graveyard.wav"),
        }
        self.sfx["game_start"].set_volume(0.2)
        self.sfx["controls"].set_volume(0.2)
        self.sfx["select"].set_volume(0.4)
        self.sfx["change_selected"].set_volume(0.3)
        self.sfx["arthur_get_hit"].set_volume(0.5)
        self.sfx["arthur_hurt"].set_volume(0.5)
        self.sfx["arthur_death"].set_volume(0.5)
        self.sfx["pick_up"].set_volume(0.9)
        self.sfx["spear_throw"].set_volume(0.2)
        self.sfx["sword_throw"].set_volume(0.2)
        self.sfx["axe_throw"].set_volume(1.0)
        self.sfx["enemy_hit"].set_volume(0.5)
        self.sfx["enemy_killed"].set_volume(0.5)
        self.sfx["ghost_killed"].set_volume(0.5)
        self.sfx["weapon_drop"].set_volume(0.6)
        self.sfx["item_drop"].set_volume(0.4)
        self.sfx["jump"].set_volume(0.5)
        self.sfx["game_over"].set_volume(0.5)
        self.sfx["intro"].set_volume(0.5)
        self.sfx["music"].set_volume(0.5)

        self.animations = {
            "enemies/ghost/wandering": Animation(load_images("enemies/ghost/attack"), img_dur= 25, loop=True),
            "enemies/ghost/attack": Animation(load_images("enemies/ghost/attack"), img_dur= 10, loop=True),
            "enemies/ghost/death": Animation(load_images("enemies/ghost/death"), img_dur=5),
            "enemies/ghost/spawning": Animation(load_images("enemies/ghost/spawning"), img_dur=10),
            "enemies/ghost/swirl": Animation(load_images("enemies/ghost/swirl"), img_dur= 10, loop=True),
            "enemies/ghost/moving_ball": Animation(load_images("enemies/ghost/moving_ball"), img_dur= 20, loop=True),
            "enemies/ghost/idle": Animation(load_images("enemies/ghost/moving_ball"), img_dur= 20, loop=True),
            "enemies/maddogS/attack": Animation(load_images("enemies/maddogS/attack"), img_dur=30),
            "enemies/maddogS/jump": Animation(load_images("enemies/maddogS/jump"), img_dur=30),
            "enemies/maddogS/falling": Animation(load_images("enemies/maddogS/falling"), img_dur=30),
            "enemies/maddogS/landing": Animation(load_images("enemies/maddogS/landing")),
            "enemies/maddogS/death": Animation(load_images("enemies/zombie/death"), img_dur=5),
            "enemies/maddogS/idle": Animation(load_images("enemies/maddogS/idle"), img_dur= 30, loop=True),
            "enemies/maddog/attack": Animation(load_images("enemies/maddog/attack"), img_dur=30),
            "enemies/maddog/jump": Animation(load_images("enemies/maddog/jump"), img_dur=30),
            "enemies/maddog/falling": Animation(load_images("enemies/maddog/falling"), img_dur=30),
            "enemies/maddog/landing": Animation(load_images("enemies/maddog/landing")),
            "enemies/maddog/death": Animation(load_images("enemies/zombie/death"), img_dur=5),
            "enemies/maddog/idle": Animation(load_images("enemies/maddog/idle"), img_dur= 30, loop=True),
            "enemies/zombie/walk": Animation(load_images("enemies/zombie/walk"), img_dur= 30, loop=True),
            "enemies/zombie/death": Animation(load_images("enemies/zombie/death"), img_dur=4),
            "enemies/zombie/idle": Animation(load_images("enemies/zombie/idle"), img_dur=30),
            "enemies/zombie/spawn_coffin": Animation(load_images("enemies/zombie/spawn_coffin"), img_dur= 20),
            "enemies/zombie/spawn_ground": Animation(load_images("enemies/zombie/spawn_ground"), img_dur= 20),
            "player/idle": Animation(load_images("player/idle")),
            "player/Bidle": Animation(load_images("player/Bidle")),
            "player/crouch": Animation(load_images("player/crouch")),
            "player/Bcrouch": Animation(load_images("player/Bcrouch")),
            "player/run0": Animation(load_images("player/run"), img_dur=9, loop=True),
            "player/run1": Animation(load_images("player/run"), img_dur=7, loop=True),
            "player/run2": Animation(load_images("player/run"), img_dur=6, loop=True),
            "player/run3": Animation(load_images("player/run"), img_dur=4, loop=True),
            "player/Brun0": Animation(load_images("player/Brun"), img_dur=9, loop=True),
            "player/Brun1": Animation(load_images("player/Brun"), img_dur=7, loop=True),
            "player/Brun2": Animation(load_images("player/Brun"), img_dur=6, loop=True),
            "player/Brun3": Animation(load_images("player/Brun"), img_dur=4, loop=True),
            "player/jump": Animation(load_images("player/jump")),
            "player/jumpD": Animation(load_images("player/jumpD"), img_dur=10),
            "player/Bjump": Animation(load_images("player/Bjump")),
            "player/BjumpD": Animation(load_images("player/BjumpD"), img_dur=10),
            "player/jump_run": Animation(load_images("player/jump_run")),
            "player/jumpD_run": Animation(load_images("player/jumpD_run"), img_dur=10),
            "player/Bjump_run": Animation(load_images("player/Bjump_run")),
            "player/BjumpD_run": Animation(load_images("player/BjumpD_run"), img_dur=10),
            "player/tuck": Animation(load_images("player/tuck")),
            "player/Btuck": Animation(load_images("player/Btuck")),
            "player/throw": Animation(load_images("player/throw")),
            "player/Bthrow": Animation(load_images("player/Bthrow")),
            "player/crouch_throw": Animation(load_images("player/crouch_throw")),
            "player/Bcrouch_throw": Animation(load_images("player/Bcrouch_throw")),
            "player/hit": Animation(load_images("player/hit"), img_dur=15),
            "player/death": Animation(load_images("player/death"), img_dur=15),
            "enemies/idle": Animation(load_images("enemies/idle")),
            "fire_collum": Animation(load_images("misc/fire-collum", scale=0.7), img_dur=8, loop=True),
        }

        self.weaponsAndItems = {
            "spear": Animation(load_images("weapons/spear")),
            "axe": Animation(load_images("weapons/axe"), img_dur=3, loop=True),
            "sword": Animation(load_images("weapons/sword")),
            "arrow": Animation(load_images("weapons/arrow")),
            "speed_up": load_image("misc/speed_up.png"),
            "damage_up": load_image("misc/damage_up.png"),
            "hp_up": load_image("misc/hp_up.png"),
            "spear_drop": load_image("hud/weapons/spear.png", scale=1.2), 
            "sword_drop": load_image("hud/weapons/sword.png", scale=1.3),
            "axe_drop": load_image("hud/weapons/axe.png", scale=1.2),
        }

        self.hud = {
            "head": load_image("hud/player/head.png"),
            "damage": load_image("hud/player/damage.png"),
            "speed": load_image("hud/player/speed.png"),
            "upgrade0": load_image("hud/player/upgrade/0.png"),
            "upgrade1": load_image("hud/player/upgrade/1.png"),
            "upgrade2": load_image("hud/player/upgrade/2.png"),
            "upgrade3": load_image("hud/player/upgrade/3.png"),
            "weapon": load_image("hud/player/weapon.png"),
            "frame": load_image("hud/weapons/frame.png"),
            "spear": load_image("hud/weapons/spear.png"),
            "sword": load_image("hud/weapons/sword.png"),
            "axe": load_image("hud/weapons/axe.png"),
        }

        self.game_enemies = ["zombie", "maddog", "maddogS", "ghost"]

        #### Variables
        self.high_scores = []
        with open("csvs/leaderboard.csv") as file:
            for line in file:
                name, score = line.rstrip().split(",")
                self.high_scores.append([name, int(score)])
        self.best_score = self.high_scores[0][1]
        self.tenth_score = self.high_scores[9][1]

        self.all_time_scores = True
        self.all_scores = []
        if self.all_time_scores:
            with open("csvs/all_scores.csv") as file:
                for line in file:
                    name, score = line.rstrip().split(",")
                    self.all_scores.append([name, int(score)])

        self.score = 0
        self.horde = 0
        self.enemies_defeated = 0

        # Time variables
        self.frames = 0
        self.seconds = 0
        self.minutes = 0

        self.game_weapons = ["spear", "axe", "sword"]
        self.weapon_roll = 10 # Variable to keep track of the times which weapon tries to drop
        self.weapon_droped = False

        self.weapons_n_kills = {"spear": 0, "axe": 0, "sword": 0}

        self.game_items = ["damage_up", "hp_up", "speed_up"]
        self.item_roll = 10
        self.hp_up_droped = False
        self.speed_up_droped = False
        self.damage_up_droped = False

        self.player = Player(self, (150, 250), (15, 30), random.choice(self.game_weapons))
        self.player_speed = 1.5 * self.player.speed
        self.movement = [False, False] #K_LEFT, K_RIGHT
        self.max_level = False

        self.player_name = "arthur"

        self.input_move = 0
        self.input_jump = 0
        self.input_shoot = 0
        self.input_crouch = 0
        self.input_swap_weapon = 0
        with open("csvs/controls.csv") as file:
            for line in file:
                action, input = line.rstrip().split(",")
                if action == "move_input":
                    self.input_move = int(input)
                elif action == "jump_input":
                    self.input_jump = int(input)
                elif action == "shoot_input":
                    self.input_shoot = int(input)
                elif action == "crouch_input":
                    self.input_crouch = int(input)
                elif action == "swap_weapon_input":
                    self.input_swap_weapon = int(input)

        self.inputs = {
            "move_left": [pygame.K_LEFT, pygame.K_a],
            "move_right": [pygame.K_RIGHT, pygame.K_d],
            "jump": [pygame.K_UP, pygame.K_w],
            "crouch": [pygame.K_DOWN, pygame.K_s],
            "shoot": [pygame.K_SPACE, pygame.K_x, pygame.K_SLASH, pygame.K_RCTRL],
            "swap_weapon": [pygame.K_c, pygame.K_q, pygame.K_RSHIFT],
        }


    def write(self, sentence, position, surf=None, font="fontA", center=False, left=False, symbol=False, scale=1.0, compensate=True): #compensate different widths
        final_sentence = {}
        char_n = 0
        string = str(sentence)
        pos = list(position) # Iterate in each char
        symbols_dict = {
            "~": "arwdown",
            "^": "arwup",
            "<": "arwl",
            ">": "arwr",
            "$": "enter",
            "[": "spacebar",
            "/": "slash",
            "!": "exclamation",
            ":": "semicolon",
            "-": "hash",
            ".": "dot",
            ",": "colon",
            "_": "hash",
        }

        if center and not symbol:
            different_widths = ["_", "hash", " ", "-", "i", "1", "3", "5", "6", "9",]
            # Get width of the first char in the string
            first_char = string[0]
            if first_char in symbols_dict:
                first_char = symbols_dict[first_char]

            if first_char in different_widths:
                x = (len(string) * 8) / 2
            else:
                first_char_img = self.chars[str(font)][first_char + ".png"]
                first_char_img = pygame.transform.scale(first_char_img, (int(first_char_img.get_width() * scale), int(first_char_img.get_height() * scale)))

                x = (len(string) * first_char_img.get_width()) / 2 # (len("attack") == 6 * the width of the chars images == 48) / 2 == 24 
            pos[0] -= x

        if left:
            x = (len(string) * 8)
            pos[0] -= x
        
        first_char_pos = pos[0]

        symbols = ["arwr", "arwl", "arwup", "arwdown", "$", ]
        # ONLY FOR THE SIMBLES IN THE FONT
        if symbol:
            if string in symbols:
                symbol_img = self.chars[str(font)][string + ".png"]
                symbol_img = pygame.transform.scale(symbol_img, (int(symbol_img.get_width() * scale), int(symbol_img.get_height() * scale)))
                symbol_rect = symbol_img.get_rect(midbottom=(pos[0], pos[1]))
                surf.blit(symbol_img, symbol_rect)
            else:
                return
        else:
            for char in string:
                if char in symbols_dict:
                    char = symbols_dict[char]
                if char == "_":
                    pos[0] += 8
                if char == " ":
                    pos[0] += 8
                else:
                    char_img = self.chars[str(font)][char + ".png"]
                    char_img = pygame.transform.scale(char_img, (int(char_img.get_width() * scale), int(char_img.get_height() * scale)))
                    if char == "enter":
                        char_rect = char_img.get_rect(bottomleft=(pos[0], pos[1] + 2))
                    elif char == "spacebar":
                        char_rect = char_img.get_rect(bottomleft=(pos[0], pos[1] - 2))
                    else:
                        char_rect = char_img.get_rect(bottomleft=(pos[0], pos[1]))
                    if char == "i" and compensate:
                        pos[0] += 4
                    elif char == "colon" and compensate:
                        pos[0] += 4
                    elif char == "dot" and compensate:
                        pos[0] += 4
                    elif char == "spacebar" and compensate:
                        pos[0] += 13
                    elif char in symbols and compensate:
                        pos[0] += 10
                    else:
                        if scale > 1.0:
                            pos[0] += 8 * scale
                        else:
                            pos[0] += 8
                    char_info = [char_img, char_rect]
                    final_sentence[char + str(char_n)] = char_info # Add the char_info to the final_sentence dictionary with char as the key
                    char_n += 1

            if surf:
                for char_info in final_sentence.values():
                    surf.blit(char_info[0], char_info[1])
            
            last_char_pos = pos[0]

        return [position[0], position[1], first_char_pos, last_char_pos, final_sentence.keys()]


    def reset_variables(self):
        self.score = 0
        self.horde = 0
        self.enemies_defeated = 0

        # Time variables
        self.frames = 0
        self.seconds = 0
        self.minutes = 0

        self.game_items = ["damage_up", "hp_up", "speed_up"]
        self.game_weapons = ["spear", "axe", "sword"]
        self.weapon_roll = 20 # Variable to keep track of the times which weapon tries to drop
        self.weapon_droped = False

        self.weapons_n_kills = {"spear": 0, "axe": 0, "sword": 0}

        self.item_roll = 15
        self.hp_up_droped = False
        self.speed_up_droped = False
        self.damage_up_droped = False

        self.player = Player(self, (285, 250), (15, 30), random.choice(self.game_weapons))
        self.movement = [False, False] #K_LEFT, K_RIGHT
        self.player_name = "arthur"


    def render_hud(self, surf):
        # Render the frame sprite in the top left of the surf
        weapons_pos = self.write("weapons", (300, 15), self.display, center=True)
        # Render the current weapon sprite in the middle of the frame sprite
        if len(self.player.weapons_held) == 1:
            positionOfWeaponSprites = [(weapons_pos[0], 32)]
        elif len(self.player.weapons_held) == 2:
            positionOfWeaponSprites = [(weapons_pos[0] - 15, 32), (weapons_pos[0] + 15, 32)]
        elif len(self.player.weapons_held) == 3:
            positionOfWeaponSprites = [(weapons_pos[0] - 30, 32), (weapons_pos[0], 32), (weapons_pos[0] + 30, 32)]

        for i in range(len(self.player.weapons_held)):
            weapon_sprite = self.hud[self.player.weapons_held[i]]
            weapon_hold_rect = weapon_sprite.get_rect(center=positionOfWeaponSprites[i])
            surf.blit(weapon_sprite, weapon_hold_rect)

        current_weapon_pos = positionOfWeaponSprites[self.player.current_weapon]
        frame_rect = self.hud["frame"].get_rect(center=current_weapon_pos)
        surf.blit(self.hud["frame"], frame_rect)

        # Render players damage and speed level
        self.write("player", (27, 15), self.display, center=True)

        damage_rect = self.hud["damage"].get_rect(center=(27, 31))
        surf.blit(self.hud["damage"], damage_rect)
        damage_level_rect = self.hud["upgrade3"].get_rect(center=(60, 31))
        surf.blit(self.hud["upgrade" + str(self.player.damage_level)], damage_level_rect)

        speed_rect = self.hud["speed"].get_rect(center=(27, 61))
        surf.blit(self.hud["speed"], speed_rect)
        speed_level_rect = self.hud["upgrade3"].get_rect(center=(60, 61))
        surf.blit(self.hud["upgrade" + str(self.player.speed_level)], speed_level_rect)

        # Score
        score = self.score * 10
        self.write("score", (598, 15), self.display, left=True)
        self.write(score, (598, 30), self.display, font="fontB", left=True)

        # Update the display
        pygame.display.flip()


    def item_drop(self, enemy_pos):
        if not self.weapon_droped: # Handle weapon drops
            if len(self.game_weapons) > 0:
                weapon_drop = None
                if self.score > 50 and len(self.game_weapons) == 2:
                    weapon_drop = self.weapon_drop(enemy_pos)
                elif self.score > 200 and len(self.game_weapons) == 1:
                    weapon_drop = self.weapon_drop(enemy_pos)
                if weapon_drop:
                    print("Weapon droped")
                    self.weapon_droped = True
                    return weapon_drop
            if len(self.game_items) > 0 or len(self.game_weapons) == 0 or not weapon_drop:
                upgrade_drop = self.upgrade_drop(enemy_pos)
                if upgrade_drop:
                    print("upgrade droped")
                return upgrade_drop


    def weapon_drop(self, enemy_pos):
        if self.weapon_roll <= 0:
            random_drop = 1
        else:
            numbers = list(range(-8, 2)) # 1/10 chance
            random_drop = random.choice(numbers)

        if random_drop > 0:
            self.weapon_roll = 20
            self.sfx["weapon_drop"].play()
            return WeaponDrop(self, random.choice(self.game_weapons) + "_drop", enemy_pos)
        else:
            self.weapon_roll -= 1
            return None


    def upgrade_drop(self, enemy_pos): # DamageUp and SpeedUp
        if self.item_roll <= 0:
            random_drop = 1
        else:
            numbers = list(range(-5, 2)) # 1/7 chance
            random_drop = random.choice(numbers)
        if random_drop > 0:
            self.item_roll = 15
            if len(self.game_items) > 0: # If there are items to drop
                self.sfx["item_drop"].play()
                return Item(self, random.choice(self.game_items), enemy_pos)
            else:
                pass
        else:
            self.item_roll -= 1
            return None


    def update_itemsToDrop(self, player, drops):
        # Update items that can be droped
        if "hp_up" in self.game_items and player.hp > 1:
            self.game_items.remove("hp_up")
        elif "hp_up" not in self.game_items and player.hp < 2:
            self.game_items.append("hp_up")

        if not self.max_level:
            player_levels = {"speed": [player.speed_level, "speed_up"], "damage": [player.damage_level, "damage_up"]}
            if player.speed_level > 2 or player.damage_level > 2:
                for level in player_levels.values():
                    if level[1] in self.game_items and level[0] == 3: # If upgrade item ("###_up") in the list of items to drop
                        self.game_items.remove(level[1])
                        if self.player.max_level:
                            self.max_level = True
            
            elif not drops:
                if player.hp < 2 and "hp_up" not in self.game_items:
                    self.game_items.append("hp_up")
                for level in player_levels.values():
                    if level[1] not in self.game_items and level[0] < 3: # If upgrade item ("###_up") in the list of items to drop
                        self.game_items.append(level[1])

            elif drops:
                for drop in drops:
                    if drop.type in self.game_items:
                        self.game_items.remove(drop.type)

        # Update the list of weapons that can be droped
        if len(self.game_weapons) > 0:
            for weapon in player.weapons_held:
                if weapon in self.game_weapons:
                    self.game_weapons.remove(weapon)


    def create_horde(self, score, horde, player_pos):
        total_enemies = 0 # Number of enemies in the horde
        type_enemies = []
        new_horde = []
        enemy_index = 0
        enemy_class = {"zombie": Zombie, "maddog": Maddog, "maddogS": MaddogS, "ghost": Ghost}

        ### Handle setting number and type of enemies
        total_enemies = min(30, round(random.choice([1, 1.33, 1.66, 1.99, 2.33, 2.66])) * horde)
        print(f"Total enemies: {total_enemies}")
        if 0 <= score <= 60:
            enemy_limits = {"zombie": random.choice(range(1, 4)), "maddog": random.choice(range(1, 3)), "maddogS": 0, "ghost": 0}  # Set limits for each enemy type
        elif 61 <= score <= 150:
            enemy_limits = {"zombie": random.choice(range(2, 5)), "maddog": random.choice(range(2, 4)), "maddogS": 0, "ghost": 0}  # Set limits for each enemy type
        elif 151 <= score <= 250:
            enemy_limits = {"zombie": 4, "maddog": 3, "maddogS": 1, "ghost": 5}  # Set limits for each enemy type
        elif 251 <= score <= 500:
            enemy_limits = {"zombie": 4, "maddog": 2, "maddogS": 2, "ghost": random.choice(range(5, 8))}  # Set limits for each enemy type
        elif score > 500:
            enemy_limits = {"zombie": 5, "maddog": 2, "maddogS": 4, "ghost": random.choice(range(10, 16))}  # Set limits for each enemy type

        n_enemiesInNewHorde = {"zombie": 0, "maddog": 0, "maddogS": 0, "ghost": 0}

        # Set the enemies that can be in the new horde
        if 0 <= horde <= 3:
            enemy_index = 1
        elif 4 <= horde <= 6:
            enemy_index = 2
        elif 7 <= horde <= 8:
            enemy_index = 3
        elif horde > 9:
            enemy_index = 4

        for i in range(enemy_index):
            type_enemies.append(self.game_enemies[i]) # 0: zombie, 1: maddog ...

        for _ in range(total_enemies):
            if not type_enemies:
                break
            for enemy in type_enemies:
                    if n_enemiesInNewHorde[enemy] >= enemy_limits[enemy]:
                        if len(type_enemies) >= 1:
                            type_enemies.remove(enemy)
                        else:
                            break
            if not type_enemies:
                break
            enemy_type = random.choice(type_enemies)
            n_enemiesInNewHorde[enemy_type] += 1
            # Recalculate spawn location for each enemy
            if enemy_type == "zombie":
                spawn_x = random.choice(range(5, 566))
                spawn_y = random.choice([0, 290])
            elif enemy_type == "maddog" or enemy_type == "maddogS":
                spawn_x = random.choice(range(2, 561))
                spawn_y = 0
            elif enemy_type == "ghost":
                spawn_x = random.choice(range(0, 600))
                spawn_y = random.choice(range(0, 300))
            enemy = enemy_class[enemy_type](self, (spawn_x, spawn_y), player_pos)
            new_horde.append(enemy)
        
        return new_horde


    def opening(self):
        nazumaLogo = load_image("opening/nazuma-nobg.png")
        nazumaLogo_size = list(nazumaLogo.get_size())
        size_adjust = 3.0
        nazumaLogo = pygame.transform.scale(nazumaLogo, (nazumaLogo_size[0] / size_adjust, nazumaLogo_size[1] / size_adjust))  # Adjust size if needed
        logo_rect = nazumaLogo.get_rect(center=(300, 150))

        presents = load_image("opening/presents.png")
        presents_rect = presents.get_rect(center=(300, 210))

        # Initial black screen
        self.display.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()
        pygame.time.delay(1500)  # Wait for 1.5 second

        # Function to fade in and out
        def fade_in_and_out(image, image1, rect, rect1):
            capcom_length = round(self.sfx["capcom"].get_length() * 60)
            alpha = 0
            fade_in = True
            fade_out = False
            start_time = pygame.time.get_ticks()
            duration = 2500  # Duration of the fade effect

            while True:
                capcom_length -= 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            self.opening()

                self.display.fill((0, 0, 0))

                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - start_time

                if fade_in:
                    alpha += 5  # Adjust the speed of fade in
                    if alpha >= 255:
                        alpha = 255
                        fade_in = False
                        pygame.time.delay(2500)  # Wait for 2.5 seconds after fade in
                        fade_out = True

                if fade_out:
                    alpha -= 5  # Adjust the speed of fade out
                    if alpha <= 0:
                        alpha = 0
                        self.sfx["by"].play()
                        break

                # Apply alpha to the logo
                image.set_alpha(alpha)
                self.display.blit(image, rect)

                # Apply alpha to the presents
                image1.set_alpha(alpha)
                self.display.blit(image1, rect1)

                # Drawing borders
                display_borders = [
                    pygame.Rect(0, 1, 1, 318),  # left_border
                    pygame.Rect(599, 1, 1, 318),  # right_border
                    pygame.Rect(1, 0, 598, 1),  # top_border
                    pygame.Rect(1, 319, 598, 1)  # bottom_border
                ]
                if self.draw_borders:
                    for border in display_borders:
                        pygame.draw.rect(self.display, (255, 255, 255), border)

                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                pygame.display.update()
                self.clock.tick(60)  # Frame rate control

        # Start the sequence
        self.sfx["capcom"].play()
        fade_in_and_out(nazumaLogo, presents, logo_rect, presents_rect)

        # Final black screen
        self.display.fill((0, 0, 0))
        self.write("by j. paulo seibt", (303, 180), self.display, center=True, scale=1.0)

        display_borders = [
                    pygame.Rect(0, 1, 1, 318),  # left_border
                    pygame.Rect(599, 1, 1, 318),  # right_border
                    pygame.Rect(1, 0, 598, 1),  # top_border
                    pygame.Rect(1, 319, 598, 1),  # bottom_border
                    pygame.Rect(299, 1, 1, 318), #center
                ]
        if self.draw_borders:
            for border in display_borders:
                pygame.draw.rect(self.display, (255, 255, 255), border)

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()

        pygame.time.delay(2000)

        self.main_menu()


    def main_menu(self):
        logo_img = load_image("misc/logo-snake.png", scale=1.3)
        logo_rect = logo_img.get_rect(center=(300, 100))

        game_start_img = load_image("misc/game start.png")
        game_start_pos = (300, 200)
        game_start_rect = game_start_img.get_rect(center=game_start_pos)

        option_mode_img = load_image("misc/option mode.png")
        option_mode_pos = (300, 220)
        option_mode_rect = game_start_img.get_rect(center=option_mode_pos)

        select = 0
        selectSpearPosition = [(0, 0)] 
        select_spear_img = load_image("misc/select spear.png")
        select_spear_rect = select_spear_img.get_rect(center=selectSpearPosition[select])

        images = {
            "logo": [logo_img, logo_rect],
            "game_start": [game_start_img, game_start_rect],
            "option_mode": [option_mode_img, option_mode_rect],
            "select_spear": [select_spear_img, select_spear_rect]
        }

        while True:
            self.display.fill((0, 0, 0))

            arws_ud_help = self.write("~/^", (28, 290), self.display, font="fontB", center=True)
            self.write("move cursor", (arws_ud_help[0] + 26, arws_ud_help[1] - 1), self.display, font="fontA", center=False, scale=0.8)

            select_help = self.write("[/$", (28, 305), self.display, font="fontB", center=True)
            self.write("select", (select_help[0] + 26, select_help[1] - 1), self.display, font="fontA", center=False, scale=0.8)

            credits = self.write("# nazuma 2024", (314, 260), self.display, center=True, font="fontA", scale=1.0)
            self.write("fan project by j. paulo seibt", (305, credits[1] + 15), self.display, center=True, font="fontA", scale=1.0)
            self.write("# nazuma brazil r.s. 2024", (207, credits[1] + 30), self.display, center=False, font="fontA", scale=1.0)
            self.write("licenced by crescendo", (303, credits[1] + 45), self.display, center=True, font="fontA", scale=1.0)

            selectSpearPosition = [
                (game_start_pos[0] - 63, game_start_pos[1] - 4),
                (option_mode_pos[0] - 63, option_mode_pos[1] - 4),
                                ]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_UP:
                        self.sfx["select"].play()
                        select += 1
                    if event.key == pygame.K_DOWN:
                        self.sfx["select"].play()
                        select += 1
                    if event.key == pygame.K_RETURN:
                        if select == 0:
                            self.sfx["game_start"].play()
                            pygame.time.delay(1000)
                            self.run()
                        elif select == 1:
                            self.sfx["controls"].play()
                            pygame.time.delay(1000)
                            self.controls_screen()
                    if event.key == pygame.K_SPACE:
                        if select == 0:
                            self.sfx["game_start"].play()
                            pygame.time.delay(1000)
                            self.run()
                        elif select == 1:
                            self.sfx["controls"].play()
                            pygame.time.delay(1000)
                            self.controls_screen()
                        return
                    if event.key == pygame.K_F1:
                        self.opening()
                    if event.key == pygame.K_F2:
                        self.game_over()

            display_borders = [ # Only to show the boundaries of the final window size
                pygame.Rect(0, 1, 1, 318), #left_border
                pygame.Rect(599, 1, 1, 318), #right_border
                pygame.Rect(1, 0, 598, 1), #top_border
                pygame.Rect(1, 319, 598, 1), #bottom_border
                pygame.Rect(299, 1, 1, 318), #center
            ]
            if self.draw_borders:
                for border in display_borders:
                    pygame.draw.rect(self.display, (255, 255, 255), border)

            if select > 1:
                select = 0
            # Update the position of select_spear_rect
            select_spear_rect = select_spear_img.get_rect(topleft=selectSpearPosition[select])
            images["select_spear"][1] = select_spear_rect

            for img in images.values():
                self.display.blit(img[0], img[1])

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


    def controls_screen(self):
        game_start_img = load_image("misc/game start.png")
        game_start_pos = (540, 300)
        game_start_rect = game_start_img.get_rect(center=game_start_pos)

        select = 0
        selectSpearPosition = [game_start_pos]
        select_spear_img = load_image("misc/select spear.png")
        select_spear_rect = select_spear_img.get_rect(center=selectSpearPosition[select])

        # Changes font when the object is selected
        move_selected = "B"
        jump_selected = "B"
        shoot_selected = "B"

        images = {
            "game_start": [game_start_img, game_start_rect],
            "select_spear": [select_spear_img, select_spear_rect]
        }

        inputs = {
            "move_input": ["< >", "a d"],
            "jump_input": ["^", "w"],
            "crouch_input": ["~", "s"],
            "shoot_input": ["[", "x", "/", "right ctrl", "left mouse"],
            "swap_weapon_input": ["c", "q", "right shift", "right mouse"],
        }

        move_input_select = self.input_move
        jump_input_select = self.input_jump
        crouch_input_select = self.input_crouch
        shoot_input_select = self.input_shoot
        swap_weapon_input_select = self.input_swap_weapon

        while True:
            self.display.fill((0, 0, 0))

            controls_options_pos = self.write("control options", (300, 20), self.display, font="fontD", center=True)

            if select == 0:
                move_selected = "C"
                jump_selected = "B"
                crouch_selected = "B"
                shoot_selected = "B"
                swap_weapon_selected = "B"
            elif select == 1:
                move_selected = "B"
                jump_selected = "C"
                crouch_selected = "B"
                shoot_selected = "B"
                swap_weapon_selected = "B"
            elif select == 2:
                move_selected = "B"
                jump_selected = "B"
                crouch_selected = "C"
                shoot_selected = "B"
                swap_weapon_selected = "B"
            elif select == 3:
                move_selected = "B"
                jump_selected = "B"
                crouch_selected = "B"
                shoot_selected = "C"
                swap_weapon_selected = "B"
            elif select == 4:
                move_selected = "B"
                jump_selected = "B"
                crouch_selected = "B"
                shoot_selected = "B"
                swap_weapon_selected = "C"
            elif select == 5:
                move_selected = "B"
                jump_selected = "B"
                crouch_selected = "B"
                shoot_selected = "B"
                swap_weapon_selected = "B"

            move_input_pos = self.write("move", (300, controls_options_pos[1] + 30), self.display, font="fontA", center=True)
            self.write(inputs["move_input"][move_input_select], (300, move_input_pos[1] + 20), self.display, font="font" + move_selected, center=True)

            jump_input_pos = self.write("jump", (300, move_input_pos[1] + 50), self.display, font="fontA", center=True)
            self.write(inputs["jump_input"][jump_input_select], (300, jump_input_pos[1] + 20), self.display, font="font" + jump_selected, center=True)

            crouch_input_pos = self.write("crouch", (300, jump_input_pos[1] + 50), self.display, font="fontA", center=True)
            self.write(inputs["crouch_input"][crouch_input_select], (300, crouch_input_pos[1] + 20), self.display, font="font" + crouch_selected, center=True)

            shoot_input_pos = self.write("shoot", (300, crouch_input_pos[1] + 50), self.display, font="fontA", center=True)
            self.write(inputs["shoot_input"][shoot_input_select], (300, shoot_input_pos[1] + 20), self.display, font="font" + shoot_selected, center=True)
           
            swap_weapon_input_pos = self.write("swap weapon", (300, shoot_input_pos[1] + 50), self.display, font="fontA", center=True)
            self.write(inputs["swap_weapon_input"][swap_weapon_input_select], (300, swap_weapon_input_pos[1] + 20), self.display, font="font" + swap_weapon_selected, center=True)

            arws_ud_help = self.write("~/^", (28, controls_options_pos[1] + 270), self.display, font="fontB", center=True)
            self.write("move cursor", (arws_ud_help[0] + 22, arws_ud_help[1] - 1), self.display, font="fontA", center=False, scale=0.8)

            arws_lr_help = self.write("</>", (28, controls_options_pos[1] + 285), self.display, font="fontB", center=True)
            self.write("change action", (arws_lr_help[0] + 22, arws_lr_help[1] - 1), self.display, font="fontA", center=False, scale=0.8)

            if select != 5:
                self.write("$", (485, controls_options_pos[1] + 285), self.display, font="fontB", center=True)

            selectSpearPosition = [
                (move_input_pos[2] - 23, move_input_pos[1] - 8),
                (jump_input_pos[2] - 23, jump_input_pos[1] - 8),
                (crouch_input_pos[2] - 23, crouch_input_pos[1] - 8),
                (shoot_input_pos[2] - 23, shoot_input_pos[1] - 8),
                (swap_weapon_input_pos[2] - 23, swap_weapon_input_pos[1] - 8),
                (game_start_pos[0] - 63, game_start_pos[1] - 4),
                                   ]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if select != 5:
                            self.sfx["change_selected"].play()
                        if select == 0:
                            if move_input_select == 0:
                                move_input_select = 1
                            else:
                                move_input_select -= 1
                        elif select == 1:
                            if jump_input_select == 0:
                                jump_input_select = 1
                            else:
                                jump_input_select -= 1
                        elif select == 2:
                            if crouch_input_select == 0:
                                crouch_input_select = 1
                            else:
                                crouch_input_select -= 1
                        elif select == 3:
                            if shoot_input_select == 0:
                                shoot_input_select = 4
                            else:
                                shoot_input_select -= 1
                        elif select == 4:
                            if swap_weapon_input_select == 0:
                                swap_weapon_input_select = 3
                            else:
                                swap_weapon_input_select -= 1
                    if event.key == pygame.K_RIGHT:
                        if select != 5:
                            self.sfx["change_selected"].play()
                        if select == 0:
                            if move_input_select == 1:
                                move_input_select = 0
                            else:
                                move_input_select += 1
                        elif select == 1:
                            if jump_input_select == 1:
                                jump_input_select = 0
                            else:
                                jump_input_select += 1
                        elif select == 2:
                            if crouch_input_select == 1:
                                crouch_input_select = 0
                            else:
                                crouch_input_select += 1
                        elif select == 3:
                            if shoot_input_select == 4:
                                shoot_input_select = 0
                            else:
                                shoot_input_select += 1
                        elif select == 4:
                            if swap_weapon_input_select == 3:
                                swap_weapon_input_select = 0
                            else:
                                swap_weapon_input_select += 1
                    if event.key == pygame.K_UP:
                        self.sfx["select"].play()
                        if select == 0:
                            select = 5
                        else:
                            select -= 1
                    if event.key == pygame.K_DOWN:
                        self.sfx["select"].play()
                        if select == 5:
                            select = 0
                        else:
                            select += 1
                    if event.key == pygame.K_RETURN:
                        with open("csvs/controls.csv", "w") as file:
                            for input in inputs.keys():
                                if input == "move_input":
                                    selected_input = move_input_select
                                elif input == "jump_input":
                                    selected_input = jump_input_select
                                elif input == "crouch_input":
                                    selected_input = crouch_input_select
                                elif input == "shoot_input":
                                    selected_input = shoot_input_select
                                elif input == "swap_weapon_input":
                                    selected_input = swap_weapon_input_select
                                file.write(f"{input},{selected_input}\n")
                        # Game Start
                        self.input_move = move_input_select
                        self.input_jump = jump_input_select
                        self.input_crouch = crouch_input_select
                        self.input_shoot = shoot_input_select
                        self.input_swap_weapon = swap_weapon_input_select
                        self.sfx["game_start"].play()
                        pygame.time.delay(1000)
                        self.run()
                    if event.key == pygame.K_SPACE:
                        self.sfx["change_selected"].play()
                        if select == 0:
                            if move_input_select == 1:
                                move_input_select = 0
                            else:
                                move_input_select += 1
                        elif select == 1:
                            if jump_input_select == 1:
                                jump_input_select = 0
                            else:
                                jump_input_select += 1
                        elif select == 2:
                            if crouch_input_select == 1:
                                crouch_input_select = 0
                            else:
                                crouch_input_select += 1
                        elif select == 3:
                            if shoot_input_select == 4:
                                shoot_input_select = 0
                            else:
                                shoot_input_select += 1
                        elif select == 4:
                            if swap_weapon_input_select == 3:
                                swap_weapon_input_select = 0
                            else:
                                swap_weapon_input_select += 1
                        # Game Start
                        elif select == 5:
                            with open("csvs/controls.csv", "w") as file:
                                for input in inputs.keys():
                                    if input == "move_input":
                                        selected_input = move_input_select
                                    elif input == "jump_input":
                                        selected_input = jump_input_select
                                    elif input == "crouch_input":
                                        selected_input = crouch_input_select
                                    elif input == "shoot_input":
                                        selected_input = shoot_input_select
                                    elif input == "swap_weapon_input":
                                        selected_input = swap_weapon_input_select
                                    file.write(f"{input},{selected_input}\n")
                            # Game Start
                            self.input_move = move_input_select
                            self.input_jump = jump_input_select
                            self.input_crouch = crouch_input_select
                            self.input_shoot = shoot_input_select
                            self.input_swap_weapon = swap_weapon_input_select
                            self.sfx["game_start"].play()
                            pygame.time.delay(1000)
                            self.run()
                    if event.key == pygame.K_F1:
                        self.opening()
                    if event.key == pygame.K_F2:
                        self.game_over()

            #self.render_hud(self.display)
            display_borders = [ # Only to show the boundaries of the final window size
                pygame.Rect(0, 1, 1, 318), #left_border
                pygame.Rect(599, 1, 1, 318), #right_border
                pygame.Rect(1, 0, 598, 1), #top_border
                pygame.Rect(1, 319, 598, 1), #bottom_border
                pygame.Rect(299, 1, 1, 318), #center
            ]
            if self.draw_borders:
                for border in display_borders:
                    pygame.draw.rect(self.display, (255, 255, 255), border)

            if select > 5:
                select = 0
            # Update the position of select_spear_rect
            select_spear_rect = select_spear_img.get_rect(topleft=selectSpearPosition[select])
            images["select_spear"][1] = select_spear_rect

            for img in images.values():
                self.display.blit(img[0], img[1])

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


    def count_time(self):
        self.frames += 1
        if self.frames == 61:
            self.seconds += 1
            self.frames = 0
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0


    def run(self):
        pygame.mixer.fadeout(1000) # To stop the game over music
        
        ### Variables and functions for name prompt:
        name_prompt = False
        input_prompt_delay = 90
        input_your_name = False

        select = 0
        selectSpearPosition = [(300, 150)]
        select_spear_img = load_image("misc/select spear.png")
        select_spear_rect = select_spear_img.get_rect(center=selectSpearPosition[select])

        images = {
            "select_spear": [select_spear_img, select_spear_rect]
        }

        keyboard_type = False

        chars = "abcdefghijklmnopqrstuvwxyz[$"
        selected_char = 0
        scroll = [False, False]
        scroll_timer = 10

        name = ""
        char_cursor_Xpos = 0
        enter = False

        n_name_chars = 13
        for _ in range(n_name_chars): #create a string with n chars
            name += "_"
        char_in_name = 0

        def confirm_char(name, char_in_name, char_cursor_Xpos, n_name_chars, enter, selected_char, chars=chars):
            if n_name_chars == 0 or enter == True:
                self.sfx["select"].play()
                self.player_name = final_name
                pygame.time.delay(500)
                self.game_over()
            else:
                self.sfx["pick_up"].play()
                new_name = ""
                i = 0
                for char in name:
                    if i == char_in_name:
                        if chars[selected_char] == "[":
                            new_name += " "
                        else:
                            new_name += chars[selected_char]
                    else:
                        new_name += char
                    i += 1
            name = new_name
            char_in_name += 1
            char_cursor_Xpos += 8
            n_name_chars -= 1
            return name, char_in_name, char_cursor_Xpos, n_name_chars
        
        def add_space_to_name(name, char_in_name, char_cursor_Xpos, n_name_chars):
            self.sfx["pick_up"].play()
            new_name = ""
            i = 0
            for char in name:
                if i == char_in_name:
                    new_name += " "
                else:
                    new_name += char
                i += 1
            name = new_name
            char_in_name += 1
            char_cursor_Xpos += 8
            n_name_chars -= 1
            return name, char_in_name, char_cursor_Xpos, n_name_chars
        ### Variables for name prompt^

        intro_length = round(self.sfx["intro"].get_length() * 60)
        intro = self.sfx["intro"].play()
        music = None
        music_loop = False

        self.reset_variables()

        enemies = []
        items = []

        # Animated torch fires in the map
        fires = [
            FireTorch(self, (58, 244), flip=True),  # First collum 
            FireTorch(self, (341, 146), flip=False),  # Collum above platform
            FireTorch(self, (243, 232), flip=False),  # Platform left
            FireTorch(self, (400, 232), flip=True),  # Platform right
            FireTorch(self, (478, 228), flip=True),  # Last collum
            ]
        
        show_hitbox_v = False
        weapon_class = {"spear": Spear, "sword": Sword, "axe": Axe, "arrow": Arrow}
        weapons = []
        self.score = 0
        hordeN_timer = 0

        back0 = load_image("map/back0(night).png")
        back1 = load_image("map/back1(blacks).png")

        ground_img = load_image("map/Ground.png", scale=0.97)

        tiles_img = load_image("map/tiles(blacks).png", key=(0,0,0), scale=0.97)

        castle_img = load_image("map/castle(night).png", scale=0.95)
        mountains_img = load_image("map/mountains(night).png", scale=0.95)
        mountains_img = load_image("map/mountainsP(night).png", scale=0.80)

        while True:
            if intro_length > 27:
                intro_length -= 1
            elif not music_loop:
                intro = None
                music = self.sfx["music"].play(-1)
                music_loop = True
            #print(intro_length)
            fps = self.clock.get_fps()
            #print(f"Current FPS: {fps}")

            # Update the list of items and weapons that can be droped
            self.update_itemsToDrop(self.player, items)

            # Background and map images
            self.display.fill((0, 0, 0, 0))
            self.display0.fill((0, 0, 0))
            self.display0.blit(mountains_img, (130, 50))
            self.display0.blit(mountains_img, (-350, 50))
            self.display0.blit(castle_img, (0, 60))
            self.display0.blit(back0, (0, 20))
            self.display0.blit(back1, (0, 20))
            self.display0.blit(tiles_img, (0, 28))
            self.display0.blit(ground_img, (0, 28))

            if hordeN_timer > 0:
                self.write("horde", (300, 85), self.display, font="fontC", center=True, scale=1.2)
                self.write(self.horde, (300, 97), self.display, font="fontC", center=True, scale=1.2)
                hordeN_timer -= 1

            platforms = [
                pygame.Rect(50, 242, 23, 10), #first collum
                pygame.Rect(87, 155, 17, 10), #tree
                pygame.Rect(243, 195, 165, 10), #platform
                pygame.Rect(334, 145, 23, 10), #collum above platform
                pygame.Rect(469, 227, 23, 10), #right collum
                pygame.Rect(561, 190, 10, 10), #skull spitter
                #pygame.Rect(0, 300, 600, 10), #bottom floor
                #pygame.Rect(200, 80, 200, 10), #upgrade platform
                ]

            boundaries = [
                pygame.Rect(0, 1, 1, 318), #left_border
                pygame.Rect(599, 1, 1, 318), #right_border
                pygame.Rect(0, 290, 600, 10), #bottom platform
            ]

            if show_hitbox_v:
                self.player.show_hitbox(self.display)
                for weapon in weapons:
                    weapon.show_hitbox(self.display, color=(0, 0, 200))
                for enemy in enemies:
                    enemy.show_hitbox(self.display, color=(200, 0, 0))
                for item in items:
                    item.show_hitbox(self.display)
                for platform in platforms:
                    pygame.draw.rect(self.display, (255, 255, 255), platform)
                for boundary in boundaries:
                    pygame.draw.rect(self.display, (25, 25, 25), boundary)

            # Player update
            if self.player.dead == True:
                if intro:
                    intro.stop()
                    intro = False
                elif music:
                    music.stop()
                    music = False
                self.player.update((0, 0), tiles=boundaries)
                name_prompt = True
            elif self.player.damaged == True:
                self.screenshake = max(20, self.screenshake)
                self.player.update((0, 0), tiles=platforms, boundaries=boundaries)
            elif self.player.damaged == False and self.player.hit_cooldown != False:
                self.player.update(((self.movement[1] - self.movement[0]) * self.player.speed, 0), tiles=platforms, boundaries=boundaries)
            elif not self.player.dead:
                # write() on the display when the player gets an item
                if self.player.pick_up_timer > 0:
                    write_pos = [self.player.pos[0] + 5, self.player.pos[1] - 7]
                    write_pick_up = self.player.item_taken_write.split()
                    if len(write_pick_up) == 1:
                        if write_pick_up == "axe":
                            write_pos[0] += 8
                        self.write(write_pick_up[0], write_pos, self.display, center=True, font="fontC")
                    else:  # Write in two lines
                        if "speed" in write_pick_up:
                            font = "fontB"
                        else:
                            font = "fontD"
                        self.write(write_pick_up[0], (write_pos[0], write_pos[1] - 12), self.display, center=True, font=font)
                        self.write(write_pick_up[1], write_pos, self.display, center=True, font="fontC")
                self.count_time()
                self.player.update(((self.movement[1] - self.movement[0]) * self.player.speed, 0), tiles=platforms, boundaries=boundaries, entities=enemies)

            # Create enemy horde:
            if len(enemies) < 1:
                self.sfx["new_horde"].play()
                self.horde += 1
                hordeN_timer = 90
                enemy_horde = self.create_horde(self.score, self.horde, self.player.pos)
                for enemy in enemy_horde:
                    enemies.append(enemy)
                
            # Update enemies
            elif enemies:
                for enemy in enemies:
                    if enemy.damage_timer > 0:
                        if not self.screenshake:
                            self.screenshake = min(15, enemy.damage_taken_write * 1.5)
                        damage_number, after_dot = str(enemy.damage_taken_write).split(".")
                        self.write(damage_number + after_dot[0], (enemy.pos[0], enemy.pos[1] - 5), self.display, font="fontD")
                for enemy in enemies:
                    if enemy.enemy_type != "ghost":
                        enemy.update(tiles=platforms, boundaries=boundaries, entities=weapons)
                    elif enemy.enemy_type == "ghost":
                        if enemy.spawn == False:
                            enemy.update(tiles=None, entities=None)
                        else:
                            enemy.update(tiles=None, entities=weapons)
                    enemy.render(self.display)
                    if enemy.die == True and enemy.animation.done == True:
                        self.score += enemy.points
                        self.enemies_defeated += 1
                        self.weapons_n_kills[enemy.hit_weapon] += 1
                        print(f"Score: {self.score}")
                        if self.player.hp < 2 or not self.player.max_level:
                            item = self.item_drop(enemy.pos) # Handle weapons and upgrade drops
                        if item:
                            items.append(item)
                        enemies.remove(enemy)
                    elif enemy.delete == True:
                        enemies.remove(enemy)

            # Update and render weapons
            if weapons:
                for weapon in weapons:
                    weapon.render(self.display)
                    weapon.update(tiles=boundaries, entities=enemies)
                    if weapon.delete == True and weapon.hit_animation_dur == 0:
                        weapons.remove(weapon)
            
            if items:
                for item in items:
                    item.render(self.display)
                    item.update(self.player, tiles=boundaries)
                    if item.delete == True:
                        if item.__class__ == WeaponDrop:
                            self.weapon_droped = False
                        elif item.type == "hp_up":
                            self.hp_up_droped = False
                        items.remove(item)

            # Render entities
            self.player.render(self.display)

            # Update fire animations
            for fire in fires:
                fire.render(self.display0)
                fire.update()

            ### NAME PROMPT
            if name_prompt:
                if not input_your_name:
                    input_prompt_delay -= 1
                    if input_prompt_delay < 1:
                        input_your_name = True
                else:
                    final_name = name.strip("_").lstrip().rstrip()
                    if not enter:
                        name_pos = self.write(name, (327, 130), self.display, center=True, scale=1.0, compensate=False)
                    elif enter:
                        if final_name == "":
                            final_name = self.player_name
                        name_pos = self.write(final_name, (327, 130), self.display, font="fontD", center=True, scale=1.0)
                        char_input = self.write("$", (name_pos[3] + 5, name_pos[1] - 1), self.display, font="fontB", scale=0.9)

                    help_input_your_name = self.write("input your name", (300, 100), self.display, font="fontC", center=True) #name_pos[2] == first char
                    player_name = self.write("player:", (name_pos[2], name_pos[1]), self.display, left=True)

                    ###HELP###
                    if not keyboard_type:
                        #Arrows
                        change_help = self.write("</>/^/~:", (help_input_your_name[0] - 280, 20), self.display, font="fontB", scale=0.9)
                        self.write("change", (change_help[3] + 5, change_help[1] - 1), self.display, font="fontA", center=False, scale=0.9)
                        #Spacebar
                        spacebar = self.write("[", (change_help[0] + 49, change_help[1] + 15), self.display, font="fontB", scale=1.0)
                        select_help = self.write(":", (spacebar[3] + 2, spacebar[1]), self.display, font="fontB", scale=0.9)
                        self.write("select", (select_help[3] + 5, select_help[1] - 1), self.display, font="fontA", center=False, scale=0.9)
                        #Backspace
                        erase_help = self.write("backspace:", (change_help[0] - 8, select_help[1] + 15), self.display, font="fontB", scale=0.9)
                        self.write("erase", (erase_help[3] + 5, erase_help[1] - 1), self.display, font="fontA", center=False, scale=0.9)
                        #Enter
                        enter_key = self.write("$", (change_help[0] + 51, erase_help[1] + 15), self.display, font="fontB", scale=0.9)
                        confirm_help = self.write(":", (enter_key[3] + 5, enter_key[1]), self.display, font="fontB", scale=0.9)
                        self.write("confirm", (confirm_help[3] + 5, confirm_help[1] - 1), self.display, font="fontA", center=False, scale=0.9)
                        #Insert
                        insert_key = self.write("insert:", (change_help[0] + 20, enter_key[1] + 15), self.display, font="fontB", scale=0.9)
                        self.write("keyboard type", (insert_key[3] + 5, insert_key[1] - 1), self.display, font="fontA", center=False, scale=0.9)
                    else:
                        #Backspace
                        erase_help = self.write("backspace:", (change_help[0] - 8, 20), self.display, font="fontB", scale=0.9)
                        self.write("erase", (erase_help[3] + 5, erase_help[1] - 1), self.display, font="fontA", center=False, scale=0.9)
                        #Enter
                        enter_key = self.write("$", (change_help[0] + 51, erase_help[1] + 15), self.display, font="fontB", scale=0.9)
                        confirm_help = self.write(":", (enter_key[3] + 5, enter_key[1]), self.display, font="fontB", scale=0.9)
                        self.write("confirm", (confirm_help[3] + 5, confirm_help[1] - 1), self.display, font="fontA", center=False, scale=0.9)
                        #Insert
                        insert_key = self.write("insert:", (change_help[0] + 20, enter_key[1] + 15), self.display, font="fontB", scale=0.9)
                        self.write("default input", (insert_key[3] + 5, insert_key[1] - 1), self.display, font="fontA", center=False, scale=0.9)

                    if scroll[0]:
                        scroll_timer -= 1
                        if scroll_timer <= 0:
                            self.sfx["change_selected"].play()
                            if selected_char == 0:
                                selected_char = len(chars) - 1
                            else:
                                selected_char -= 1
                            scroll_timer = 7
                    if scroll[1]:
                        scroll_timer -= 1
                        if scroll_timer <= 0:
                            self.sfx["change_selected"].play()
                            if selected_char == len(chars) - 1:
                                selected_char = 0
                            else:
                                selected_char += 1
                            scroll_timer = 7

                    if n_name_chars > 0:
                        scale = 1.0
                        char_selected = chars[selected_char]
                        if char_selected == "$":
                            enter = True
                        elif char_selected == "[":
                            enter = False
                            adjust_bar = -2
                            char_input = self.write(chars[selected_char], (char_cursor_Xpos + adjust_bar, name_pos[1] + 4), self.display, font="fontB", scale=scale)
                        else:
                            enter = False
                            char_input = self.write(chars[selected_char], (char_cursor_Xpos, name_pos[1] - 2), self.display, font="fontB", scale=scale)
                    else:
                        enter = True
                    if not char_cursor_Xpos:
                        char_cursor_Xpos = name_pos[2] - 0.5 # Gets the first char pos

            mask = pygame.mask.from_surface(self.display)
            outline = mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
            for line in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display0.blit(outline, line)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == self.inputs["move_left"][self.input_move]: 
                        if input_your_name and not keyboard_type:
                            self.sfx["change_selected"].play()
                            if selected_char == 0:
                                selected_char = len(chars) - 1
                            else:
                                selected_char -= 1
                            scroll_timer = 20
                            scroll[0] = True
                        else:
                            self.movement[0] = True
                    if event.key == self.inputs["move_right"][self.input_move]:
                        if input_your_name and not keyboard_type:
                            self.sfx["change_selected"].play()
                            if selected_char == len(chars) - 1:
                                selected_char = 0
                            else:
                                selected_char += 1
                            scroll_timer = 20
                            scroll[1] = True
                        else:
                            self.movement[1] = True
                    if event.key == self.inputs["jump"][self.input_jump]:
                        if input_your_name and not keyboard_type:
                            self.sfx["change_selected"].play()
                            if selected_char == 0:
                                selected_char = len(chars) - 1
                            else:
                                selected_char -= 1
                            scroll_timer = 20
                            scroll[0] = True
                        else:
                            if self.player.jump():
                                self.sfx["jump"].play()
                    if event.key == self.inputs["crouch"][self.input_crouch]:
                        if input_your_name and not keyboard_type:
                            self.sfx["change_selected"].play()
                            if selected_char == len(chars) - 1:
                                selected_char = 0
                            else:
                                selected_char += 1
                            scroll_timer = 20
                            scroll[1] = True
                        else:
                            if not self.player.dead:
                                self.player.crouch = True
                    if self.input_shoot < 4: #If is not mouse
                        if event.key == self.inputs["shoot"][self.input_shoot]:
                            if input_your_name and not keyboard_type and self.input_shoot > 0: # If the spacebar are not been used to shoot
                                name, char_in_name, char_cursor_Xpos, n_name_chars = confirm_char(
                                    name, char_in_name, char_cursor_Xpos, n_name_chars, enter, selected_char
                                )
                            else:
                                if not self.player.throw and not self.player.dead:
                                    self.player.attack()
                                    if self.player.throw:
                                        # Pick the class of the weapon that the player is currently helding
                                        weapon = weapon_class[self.player.weapon](self, self.player.pos, self.player.flip, self.player.damage)
                                        weapons.append(weapon)
                    if self.input_swap_weapon < 3: #If is not mouse
                        if event.key == self.inputs["swap_weapon"][self.input_swap_weapon]:
                            self.player.weapon_swap()
                    if event.key == pygame.K_LALT:
                        if not show_hitbox_v:
                            show_hitbox_v = True
                        else:
                            show_hitbox_v = False
                    if event.key == pygame.K_F1:
                        self.opening()
                    ### ONLY FOR NAME PROMPT:
                    if input_your_name:
                        if not keyboard_type:
                            if event.key == pygame.K_LEFT:
                                if self.input_move > 0: # If the arrows are not been used to move
                                    self.sfx["change_selected"].play()
                                    if selected_char == 0:
                                        selected_char = len(chars) - 1
                                    else:
                                        selected_char -= 1
                                    scroll_timer = 20
                                    scroll[0] = True
                            if event.key == pygame.K_RIGHT:
                                if self.input_move > 0: # If the arrows are not been used to move
                                    self.sfx["change_selected"].play()
                                    if selected_char == len(chars) - 1:
                                        selected_char = 0
                                    else:
                                        selected_char += 1
                                    scroll_timer = 20
                                    scroll[1] = True
                            if event.key == pygame.K_UP:
                                if self.input_jump > 0: # If the up arrow are not been used to jump
                                    self.sfx["change_selected"].play()
                                    if selected_char == 0:
                                        selected_char = len(chars) - 1
                                    else:
                                        selected_char -= 1
                                    scroll_timer = 20
                                    scroll[0] = True
                            if event.key == pygame.K_DOWN:
                                if self.input_crouch > 0: # If the down arrow are not been used to crouch
                                    self.sfx["change_selected"].play()
                                    if selected_char == len(chars) - 1:
                                        selected_char = 0
                                    else:
                                        selected_char += 1
                                    scroll_timer = 20
                                    scroll[1] = True
                        if event.key == pygame.K_SPACE:
                            if keyboard_type:
                                name, char_in_name, char_cursor_Xpos, n_name_chars = add_space_to_name(name, char_in_name, char_cursor_Xpos, n_name_chars)
                            else:
                                name, char_in_name, char_cursor_Xpos, n_name_chars = confirm_char(
                                    name, char_in_name, char_cursor_Xpos, n_name_chars, enter, selected_char
                                )
                        if event.key == pygame.K_BACKSPACE: #ERASER
                            if enter:
                                enter = False

                            selected_char = len(chars) - 2 if keyboard_type else 0

                            if n_name_chars != 13:
                                char_in_name -= 1
                                new_name = ""
                                i = 0
                                for char in name:
                                    if i == char_in_name:
                                        new_name += "_"
                                    else:
                                        new_name += char
                                    i += 1
                                name = new_name
                                char_cursor_Xpos -= 8
                                n_name_chars += 1
                        if event.key == pygame.K_RETURN:
                            if not enter:
                                selected_char = len(chars) - 1 # Should == "$"
                            else:
                                self.sfx["select"].play()
                                if final_name == "":
                                    final_name = self.player_name
                                self.player_name = final_name
                                pygame.time.delay(500)
                                self.game_over()
                        if event.key == pygame.K_INSERT:
                            if not keyboard_type:
                                keyboard_type = True
                                selected_char = selected_char = len(chars) - 2 #"["
                            else:
                                keyboard_type = False
                                selected_char = 0 #"a"
                        else: # For the keyboard type
                            letter = event.unicode
                            if keyboard_type and n_name_chars > 0 and not enter: # Keyboard support
                                letter = letter.lower()
                                if not letter:
                                    pass
                                elif letter in chars:
                                    self.sfx["pick_up"].play()
                                    new_name = ""
                                    i = 0
                                    for char in name:
                                        if i == char_in_name:
                                            new_name += letter
                                        else:
                                            new_name += char
                                        i += 1
                                    name = new_name
                                    char_in_name += 1
                                    char_cursor_Xpos += 8
                                    n_name_chars -= 1
                if event.type == pygame.KEYUP:
                    if event.key == self.inputs["move_left"][self.input_move]:
                        if input_your_name:
                            scroll[0] = False
                        else:
                            self.movement[0] = False
                    if event.key == self.inputs["move_right"][self.input_move]:
                        if input_your_name:
                            scroll[1] = False
                        else:
                            self.movement[1] = False
                    if event.key == self.inputs["jump"][self.input_jump]:
                        if input_your_name:
                            scroll[0] = False
                    if event.key == self.inputs["crouch"][self.input_crouch]:
                        if input_your_name:
                            scroll[1] = False
                        else:
                            self.player.crouch = False
                    if event.key == pygame.K_LEFT:
                        if input_your_name:
                            scroll[0] = False
                    if event.key == pygame.K_RIGHT:
                        if input_your_name:
                            scroll[1] = False
                    if event.key == pygame.K_UP:
                        if input_your_name:
                            scroll[0] = False
                    if event.key == pygame.K_DOWN:
                        if input_your_name:
                            scroll[1] = False
                if self.input_shoot == 4 or self.input_swap_weapon == 3: # If one of the mouse bindings was choosed by the player
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT and self.input_shoot == 4:
                            if not self.player.throw and not self.player.dead:
                                self.player.attack()
                                if self.player.throw:
                                    # Pick the class of the weapon that the player is currently helding
                                    weapon = weapon_class[self.player.weapon](self, self.player.pos, self.player.flip, self.player.damage)
                                    weapons.append(weapon)
                        if event.button == pygame.BUTTON_RIGHT and self.input_swap_weapon == 3:
                            self.player.weapon_swap()
                    
            if not name_prompt:
                self.render_hud(self.display)
                
            display_borders = [ # Only to show the boundaries of the final window size
                pygame.Rect(0, 1, 1, 318), #left_border
                pygame.Rect(599, 1, 1, 318), #right_border
                pygame.Rect(1, 0, 598, 1), #top_border
                pygame.Rect(1, 319, 598, 1), #bottom_border
                pygame.Rect(299, 1, 1, 318), #center
            ]
            if self.draw_borders:
                for border in display_borders:
                    pygame.draw.rect(self.display, (255, 255, 255), border)

            self.display0.blit(self.display, (0, 0))

            self.screenshake = max(0, self.screenshake - 7)

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display0, self.screen.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)


    def game_over(self):
        self.sfx["game_over"].play()

        game_over_img = load_image("game_over/5.png")
        game_over_rect = game_over_img.get_rect(center=(300, 115))

        game_start_img = load_image("misc/game start.png")
        game_start_pos = (300, 260)
        game_start_rect = game_start_img.get_rect(center=game_start_pos)

        option_mode_img = load_image("misc/option mode.png")
        option_mode_pos = (300, 280)
        option_mode_rect = game_start_img.get_rect(center=option_mode_pos)

        select = 0
        adjust_pos = 9
        selectSpearPosition = [(245, game_start_pos[1]), (245, option_mode_pos[1]),]
        select_spear_img = load_image("misc/select spear.png")
        select_spear_rect = select_spear_img.get_rect(center=selectSpearPosition[select])

        images = {
            "game_over": [game_over_img, game_over_rect],
            "game_start": [game_start_img, game_start_rect],
            "option_mode": [option_mode_img, option_mode_rect],
            "select_spear": [select_spear_img, select_spear_rect]
        }

        ### All time scores begins
        if self.all_time_scores: # If add to all_scores.csv True
            if self.score > 19: # If the run score is >= 200, the player's name and score go to `all_scores.csv`
                print("YEAH")
                run_score_in_all_scores = False
                new_all_scores = []

                for score in self.all_scores:
                    if self.score > score[1] and not run_score_in_all_scores:
                        new_all_scores.append([self.player_name, self.score])
                        run_score_in_all_scores = True
                    # Checks again if the leaderboard already have 10 scores
                    new_all_scores.append(score)

                if not run_score_in_all_scores:
                    new_all_scores.append([self.player_name, self.score])

                all_scores = new_all_scores # New list of scores

                with open("csvs/all_scores.csv", "w") as file:
                    for score in all_scores:
                        file.write(f"{score[0]},{score[1]}\n")
                        ### All time scores end
        
        # Variables for new high score
        run_score_in_leaderboard = None
        run_score_flame = None
        flame_pos_idx = None

        if self.score > self.tenth_score:
            run_score_in_leaderboard = False
            new_scores = []
            run_score_flame = FireTorch(self, (0,0), flip=True)
            for score in self.high_scores:
                if len(new_scores) < 10:
                    if self.score > score[1] and not run_score_in_leaderboard:
                        new_scores.append([self.player_name, self.score])
                        run_score_in_leaderboard = True
                        flame_pos_idx = self.high_scores.index(score)
                    # Checks again if the leaderboard already have 10 scores
                    if len(new_scores) < 10:
                        new_scores.append(score)
            self.high_scores = new_scores # New list of scores
            self.best_score = self.high_scores[0][1]
            self.last_score = self.high_scores[9][1]
            with open("csvs/leaderboard.csv", "w") as file:
                for score in self.high_scores:
                    file.write(f"{score[0]},{score[1]}\n")

        hordes_cleared = max(0, self.horde - 1)
        run_score_value = self.score * 10
        ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        while True:
            self.display.fill((0, 0, 0))

            # Adjust the Xpos of the stats table based on the n_chars that will be in Enemies Defeated
            e_d_XposA = 0 #enemies_defeated_Xpos_adjust
            if 100 > self.enemies_defeated > 9:
                e_d_XposA = -8
            elif 1000 > self.enemies_defeated > 99:
                e_d_XposA = -17

            head_rect = self.hud["head"].get_rect(center=(75 + e_d_XposA, 18))
            self.display.blit(self.hud["head"], head_rect)

            # Player and stats
            player_pos = self.write("player", (118 + e_d_XposA, 25), self.display, font="fontA", center=True, scale=1.2)
            stats = self.write("stats of the run", (112 + e_d_XposA, player_pos[1] + 15), self.display, font="fontA", center=True, scale=0.9)

            #name
            name_pos = self.write("name:", (stats[0] - 37, stats[1] + 20), self.display, font="fontC", center=False, scale=1.0)
            self.write(self.player_name, (name_pos[3], name_pos[1]), self.display, font="fontA", scale=1.0)
            #score
            score_pos = self.write("score:", (name_pos[0], name_pos[1] + 20), self.display, font="fontC", scale=1.0)
            self.write(run_score_value, (score_pos[3], score_pos[1]), self.display, font="fontA", scale=1.0)
            #horde
            horde_pos = self.write("hordes cleared:", (score_pos[0], score_pos[1] + 20), self.display, font="fontC", scale=1.0)
            self.write(hordes_cleared, (horde_pos[3], horde_pos[1]), self.display, font="fontA", scale=1.0)
            #enemies
            enemies_pos = self.write("enemies defeated:", (horde_pos[0], horde_pos[1] + 20), self.display, font="fontC", scale=1.0)
            self.write(self.enemies_defeated, (enemies_pos[3], enemies_pos[1]), self.display, font="fontA", scale=1.0)
            #damage
            damage_pos = self.write("damage level:", (enemies_pos[0], enemies_pos[1] + 20), self.display, font="fontC", scale=1.0)
            self.write(self.player.damage_level, (damage_pos[3], damage_pos[1]), self.display, font="fontA", scale=1.0)
            #speed
            speed_pos = self.write("speed level:", (damage_pos[0], damage_pos[1] + 20), self.display, font="fontC", scale=1.0)
            self.write(self.player.speed_level, (speed_pos[3], speed_pos[1]), self.display, font="fontA", scale=1.0)
            #spear
            spear_pos = self.write("spear kills:", (speed_pos[0], speed_pos[1] + 20), self.display, font="fontC", scale=1.0)
            self.write(self.weapons_n_kills["spear"], (spear_pos[3], spear_pos[1]), self.display, font="fontA", scale=1.0)
            #sword
            sword_pos = self.write("sword kills:", (spear_pos[0], spear_pos[1] + 20), self.display, font="fontC", scale=1.0)
            self.write(self.weapons_n_kills["sword"], (sword_pos[3], sword_pos[1]), self.display, font="fontA", scale=1.0)
            #axe
            axe_pos = self.write("axe kills:", (sword_pos[0], sword_pos[1] + 20), self.display, font="fontC", scale=1.0)
            self.write(self.weapons_n_kills["axe"], (axe_pos[3], axe_pos[1]), self.display, font="fontA", scale=1.0)
            #time
            time_pos = self.write("time:", (axe_pos[0], axe_pos[1] + 20), self.display, font="fontC", scale=1.0)
            minutes = self.write(f"{self.minutes:02}:", (time_pos[3], time_pos[1]), self.display, font="fontA", scale=1.0)
            seconds = self.write(f"{self.seconds:02}", (minutes[3], minutes[1]), self.display, font="fontA", scale=1.0)


            #high scores
            best_score_value = self.best_score * 10
            leaderboard_pos = self.write("leaderboard", (411, 25), self.display, font="fontA", scale=1.2)

            first_row = leaderboard_pos[1] + 15
            rank_collum = self.write("rank", (390, first_row), self.display, font="fontA", scale=0.9)
            score_collum = self.write("score", (432, first_row), self.display, font="fontA", scale=0.9)
            name_collum = self.write("player", (490, first_row), self.display, font="fontA", scale=0.9)

            rank_row_pos = first_row + 20
            score_row_pos = first_row + 20
            name_row_pos = first_row + 20

            rank_collum_Xpos = rank_collum[0]
            score_collum_Xpos = score_collum[0]
            name_collum_Xpos = name_collum[0]

            for rank in ranks:
                if rank == 1:
                    font = "fontA"
                elif rank == 2:
                    font = "fontB"
                elif rank == 3:
                    font = "fontD"
                else:
                    font = "fontC"
                n_rank = self.write(rank, (rank_collum_Xpos, rank_row_pos), self.display, font=font)
                if rank == 1:
                    self.write("st", (n_rank[3] - 3, rank_row_pos), self.display, font="fontA")
                elif rank == 2:
                    self.write("nd", (n_rank[3], rank_row_pos), self.display, font="fontB")
                elif rank == 3:
                    self.write("rd", (n_rank[3], rank_row_pos), self.display, font="fontD")
                else:
                    self.write("th", (n_rank[3], rank_row_pos), self.display, font="fontC")
                # FireTorch object next to new high score
                if run_score_in_leaderboard and flame_pos_idx + 1 == rank:
                    x = 20
                    if rank == 10:
                        x += 8
                    run_score_flame.pos = (n_rank[3] - x, n_rank[1] - 20)
                    run_score_flame.update()
                    run_score_flame.render(self.display)
                rank_row_pos += 20

            for index, score in enumerate(self.high_scores): #Index: 0, score: ["player name", player score]
                score_value = score[1] * 10
                if index == 0:
                    font = "fontA"
                elif index == 1:
                    font = "fontB"
                elif index == 2:
                    font = "fontD"
                else:
                    font = "fontC"
                self.write(score_value, (score_collum_Xpos, score_row_pos), self.display, font=font, center=False, scale=1.0)
                score_row_pos += 20

            # Names
            for index, score in enumerate(self.high_scores):
                if index == 0:
                    font = "fontA"
                elif index == 1:
                    font = "fontB"
                elif index == 2:
                    font = "fontD"
                else:
                    font = "fontC"
                self.write(score[0], (name_collum_Xpos, name_row_pos), self.display, font=font)
                name_row_pos += 20
            #self.write(best_score_value, (arrow[0], arrow[1] + 13), self.display, font="fontC", center=True)

            arws_ud_help = self.write("~/^", (28, 290), self.display, font="fontB", center=True)
            self.write("move cursor", (arws_ud_help[0] + 26, arws_ud_help[1] - 1), self.display, font="fontA", center=False, scale=0.8)

            select_help = self.write("[/$", (28, 305), self.display, font="fontB", center=True)
            self.write("select", (select_help[0] + 26, select_help[1] - 1), self.display, font="fontA", center=False, scale=0.8)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_UP:
                        self.sfx["select"].play()
                        select += 1
                    if event.key == pygame.K_DOWN:
                        self.sfx["select"].play()
                        select += 1
                    if event.key == pygame.K_RETURN:
                        if select == 0:
                            self.sfx["game_start"].play()
                            pygame.time.delay(1000)
                            self.run()
                        elif select == 1:
                            self.sfx["controls"].play()
                            pygame.time.delay(1000)
                            self.controls_screen()
                    if event.key == pygame.K_SPACE:
                        if select == 0:
                            self.sfx["game_start"].play()
                            pygame.time.delay(1000)
                            self.run()
                        elif select == 1:
                            self.sfx["controls"].play()
                            pygame.time.delay(1000)
                            self.controls_screen()
                        return
                    if event.key == pygame.K_F1:
                        self.opening()

            display_borders = [ # Only to show the boundaries of the final window size
                pygame.Rect(0, 1, 1, 318), #left_border
                pygame.Rect(599, 1, 1, 318), #right_border
                pygame.Rect(1, 0, 598, 1), #top_border
                pygame.Rect(1, 319, 598, 1), #bottom_border
                pygame.Rect(299, 1, 1, 318), #center
            ]
            if self.draw_borders:
                for border in display_borders:
                    pygame.draw.rect(self.display, (255, 255, 255), border)

            selectSpearPosition = [
                (game_start_pos[0] - 63, game_start_pos[1] - 4),
                (option_mode_pos[0] - 63, option_mode_pos[1] - 4),
                                  ]

            if select > 1:
                select = 0
            # Update the position of select_spear_rect
            select_spear_rect = select_spear_img.get_rect(topleft=selectSpearPosition[select])
            images["select_spear"][1] = select_spear_rect

            for img in images.values():
                self.display.blit(img[0], img[1])

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main()