import pygame
import random
from scripts.utils import load_image, load_images, show_hitbox, Animation


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

        self.collisions = {"top": False, "bottom": False, "right": False, "left": False}
        self.hit = {"top": False, "bottom": False, "right": False, "left": False}

        # Set animations
        self.flip = False
        self.action = ""
        self.set_action("idle")

        self.bottom_tiles = []

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.animations[self.type + "/" + self.action].copy()

    def show_hitbox(self, surf, color=(0, 200, 0)):
        pygame.draw.rect(surf, color, self.rect())

    def gravity(self, x=0.1):
        self.velocity[1] += x
        return True

    def update(self, movement=(0, 0), tiles=None, boundaries=None, entities=None):
        self.collisions = {"top": False, "bottom": False, "right": False, "left": False}
        self.hit = {"top": False, "bottom": False, "right": False, "left": False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()

        if entities:
            for entity in entities:
                collision_entity_rect = entity.rect()

                if entity_rect.colliderect(collision_entity_rect):
                    # Check collision with the right side
                    right_side = pygame.Rect(entity_rect.right, entity_rect.top, 1, entity_rect.height)
                    if right_side.colliderect(collision_entity_rect):
                        self.hit["right"] = True

                    # Check collision with the left side
                    left_side = pygame.Rect(entity_rect.left, entity_rect.top, 1, entity_rect.height)
                    if left_side.colliderect(collision_entity_rect):
                        self.hit["left"] = True

                    # Check collision with the top side
                    top_side = pygame.Rect(entity_rect.left, entity_rect.top, entity_rect.width, 1)
                    if top_side.colliderect(collision_entity_rect):
                        self.hit["top"] = True

                    # Check collision with the bottom side
                    bottom_side = pygame.Rect(entity_rect.left, entity_rect.bottom, entity_rect.width, 1)
                    if bottom_side.colliderect(collision_entity_rect):
                        self.hit["bottom"] = True

        collision_tiles = []
        if tiles:
            for tile in tiles:
                if tile not in self.bottom_tiles and (self.pos[1] + self.size[1]) < tile[1]:
                    self.bottom_tiles.append(tile)
                elif tile in self.bottom_tiles and self.pos[1] > tile[1]:
                    self.bottom_tiles.remove(tile)

                for tile in self.bottom_tiles:
                    collision_tiles.append(tile)
                if boundaries:
                    for tile in boundaries:
                        collision_tiles.append(tile)

            for collision_tile in collision_tiles:
                if entity_rect.colliderect(collision_tile):
                    if frame_movement[0] > 0:
                        entity_rect.right = collision_tile.left
                        self.collisions["right"] = True
                    if frame_movement[0] < 0:
                        entity_rect.left = collision_tile.right
                        self.collisions["left"] = True
                    self.pos[0] = entity_rect.x

            self.pos[1] += frame_movement[1]
            entity_rect = self.rect()

            for collision_tile in collision_tiles:
                if entity_rect.colliderect(collision_tile):
                    if frame_movement[1] > 0:
                        entity_rect.bottom = collision_tile.top
                        self.collisions["bottom"] = True
                    if frame_movement[1] < 0:
                        entity_rect.top = collision_tile.bottom
                        self.collisions["top"] = True
                    self.pos[1] = entity_rect.y
            
            if self.collisions["bottom"] == True:
                self.velocity[1] = 0
            if self.collisions["top"] == True:
                self.velocity[1] = 0
        else:
            self.pos[1] += frame_movement[1]

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.animation.update()

    def render(self, surf):
        surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.pos[0], self.pos[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size, weapon):
        self.damage_level = 0
        self.damage_upgrade = {0: 1.0, 1: 1.2, 2: 1.7, 3: 3.2}
        self.damage = self.damage_upgrade[self.damage_level]

        self.speed_level = 0
        self.speed_upgrade = {0: 1.2, 1: 1.5, 2: 1.8, 3: 2.2}
        self.speed = self.speed_upgrade[self.speed_level]

        self.max_level = False # True if speed and damage levels get 3
        self.hp = 1
        self.dead = False

        self.crouch = False

        self.pick_up = False
        self.item_taken = ""
        self.pick_up_timer = 0
        self.item_taken_write = ""

        self.weapon = weapon
        self.weapons_held = [weapon,]
        self.current_weapon = 0
        self.cooldown = {"spear": 30, "sword": 15, "axe": 60, "arrow": 15} # Cooldown of each weapon
        super().__init__(game, "player", pos, size)
        self.renderPos_x = 0  # Adjust the render Xposition of the sprite
        self.renderPos_y = 0  # Adjust the render Yposition of the sprite

        self.in_air = 0
        self.n_jumps = 2
        self.current_jump_animation = ""
        self.current_jumpD_animation = ""

        self.throw = False
        self.throw_animation_cooldown = 13
        self.throw_cooldown = self.cooldown[weapon] # Cooldown of the current weapon
        self.tuck = False
        self.tuck_dur = 8
        self.n_tucks = 1

        self.knock_back = 0
        self.hit_animation_dur = 0
        self.hit_cooldown = 0
        self.damaged = False
    
    def set_action(self, action):
        if self.hp == 1 and action != "hit":
            action = "B" + action
        elif self.dead:
            action = "death"
            if 0 < self.animation.frame < 5:
                self.size = self.animation.sprite().get_size()
        super().set_action(action)

    def update(self, movement=(0, 0), tiles=None, boundaries=None, entities=None):
        super().update(movement=movement, tiles=tiles, boundaries=boundaries, entities=entities)
        
        self.renderPos_x = -4
        self.renderPos_y = -5

        if self.speed_level == 3 and self.damage_level == 3:
            self.max_level = True

        if self.pick_up:
            self.pick_up_timer = 50
            self.game.sfx["pick_up"].play()
            self.upgrade(self.item_taken)
            self.pick_up = False
            self.item_taken = ""  # Reset item taken

        if self.hp < 1 and not self.dead:
            self.game.sfx["arthur_death"].play()
            self.dead = True

        self.gravity()
        frame_size = self.animation.sprite().get_size()
        size = (15, 30)

        if self.pick_up_timer > 0:
            self.pick_up_timer -= 1

        # Remove entity when out of bounds
        if self.pos[0] > 610 or self.pos[0] < -10 or self.pos[1] > 330 or self.pos[1] < -60:
            self.hp = 0

        if self.knock_back > 0:
            self.knock_back = max(0, self.knock_back - 5)
        elif self.knock_back < 0:
            self.knock_back = min(0, self.knock_back + 5)
        self.velocity[0] = self.knock_back * 0.15
        
        if self.throw_cooldown < self.cooldown[self.weapon]:
            self.throw_cooldown += 1
        else:
            self.throw_cooldown = self.cooldown[self.weapon]

        self.in_air += 1
        if self.collisions["bottom"]:
            self.n_tucks = 1
            self.n_jumps = 2
            self.in_air = 0
            self.current_jump_animation = ""
            self.current_jumpD_animation = ""

        if entities:
            for entity in entities:
                enemy_rect = entity.rect()
                if self.rect().colliderect(enemy_rect) and entity.spawn == True and not entity.die:
                     if any(self.hit.values()) == True:
                        self.game.sfx["arthur_get_hit"].play()
                        self.damaged = True
                        self.knockback()
                        print(self.hit)
                        print(self.pos)
        
        if self.crouch and not self.throw and self.in_air < 5 and movement[0] == 0:
            self.set_action("crouch")
            self.pos[1] += self.size[1] - 18
            self.size = (18, 18)
        elif not self.crouch or movement[0] != 0:
            if not self.dead:
                self.pos[1] -= 30 - self.size[1]
                self.size = size
            
        if self.throw == True:
            action = "throw"
            if self.crouch and movement[0] == 0:
                action = "crouch_" + action
            self.set_action(action)
            self.throw_animation_cooldown -= 1
            if self.throw_animation_cooldown <= 0:
                self.throw_animation_cooldown = 13
                self.throw = False
                if self.n_jumps < 1 and self.n_tucks > 0:
                    self.tuck = True
        
        elif self.tuck == True:
            self.set_action("tuck")
            self.tuck_dur -= 1
            if self.tuck_dur <= 0:
                self.tuck_dur = 8
                self.tuck = False
                self.n_tucks -= 1

        # Set double jump animation
        elif self.in_air > 5 and self.n_jumps < 1:
            if not self.current_jumpD_animation:
                if movement[0] != 0:
                    self.current_jumpD_animation = "jumpD_run"
                else:
                    self.current_jumpD_animation = "jumpD"
                self.set_action(self.current_jumpD_animation)
                self.n_jumps -= 1
            else:
                self.set_action(self.current_jumpD_animation)
        # Set first jump animation
        elif self.in_air > 5:
            self.n_jumps = 1
            if not self.current_jump_animation:
                if movement[0] != 0:
                    self.current_jump_animation = "jump_run" #self.set_action("jump_run")
                else:
                    self.current_jump_animation = "jump" #self.set_action("jump")
            else:
                self.set_action(self.current_jump_animation)

        elif movement[0] != 0:
            if self.speed_level == 0:
                self.set_action("run0")
            elif self.speed_level == 1:
                self.set_action("run1")
            elif self.speed_level == 2:
                self.set_action("run2")
            elif self.speed_level == 3:
                self.set_action("run3")
        elif movement[0] == 0 and not self.crouch:
            self.set_action("idle")

        if self.damaged:
            self.hit_animation_dur += 1
            self.set_action("hit")
            if self.hit_animation_dur >= 20:
                self.hp -= 1
                self.hit_cooldown = 90
                self.hit_animation_dur = 0
                self.damaged = False
                self.size = size
                self.pos[1] -= 15
                if self.hp > 0:
                    self.game.sfx["arthur_hurt"].play()

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
            return True
        elif self.hit_cooldown == 0:
            return False
        
    def attack(self):
        if self.throw_cooldown == self.cooldown[self.weapon] and not self.throw and not self.tuck:
            self.throw = True
            self.throw_cooldown = 0
            return True
        return False

    def jump(self):
        if self.n_jumps > 0 and self.hp > 0:
            self.velocity[1] = -3
            if self.n_jumps == 1:
                self.n_jumps -= 1
            return True

    def knockback(self):
        self.pos[1] -= 15
        if not self.knock_back:
            if self.hit["right"]:
                self.knock_back = -45
                if self.flip:
                    self.flip = False
            elif self.hit["left"]:
                self.knock_back = 45
                if not self.flip:
                    self.flip = True

    def weapon_swap(self):
        weapons_index = {"spear": 1, "sword":2, "axe":3, "arrow": 4}

        next_weapon = self.current_weapon + 1
        self.current_weapon += 1

        if next_weapon > len(self.weapons_held) - 1:
            self.weapon = self.weapons_held[0]
            self.current_weapon = 0
        else:
            self.weapon = self.weapons_held[next_weapon]

        self.throw_cooldown = self.cooldown[self.weapon] # Update the cooldown of the current weapon

        print("Weapon equip:" + self.weapon)
        print("Weapon cooldown:" + str(self.throw_cooldown))
    
    def damage_up(self):
        if self.damage_level < 3:
            self.damage_level += 1
            self.damage = self.damage_upgrade[self.damage_level]
            print(self.damage_level)

    def speed_up(self):
        if self.speed_level < 3:
            self.speed_level += 1
            self.speed = self.speed_upgrade[self.speed_level]
            print(self.speed_level)
    
    def hp_up(self):
        if self.hp < 2:
            self.hp += 1
    
    def upgrade(self, upgrade_item):
        weapons = {
            "spear_drop": "spear",
            "axe_drop": "axe",
            "sword_drop": "sword"}
        items = {
            "damage_up": self.damage_up,
            "speed_up": self.speed_up,
            "hp_up": self.hp_up,
            }

        if upgrade_item in weapons:
            weapon = weapons[upgrade_item]
            if weapon not in self.weapons_held:
                self.weapons_held.append(weapon)
                self.item_taken_write = weapon

        elif upgrade_item in items:
            self.item_taken_write = self.item_taken.replace("_", " ")
            if "hp" in self.item_taken_write:
                self.item_taken_write = "armor"
            else:
                self.item_taken_write = self.item_taken_write.replace("up", "upgrade")
            items[upgrade_item]()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def render(self, surf):
        if self.hit_cooldown > 0 and self.action != "death":
            if self.hit_cooldown % 10 < 5:
            # Only render the player sprite half of the time during hit cooldown
                surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.rect()[0] - 5, self.rect()[1] - 6))
        elif self.action == "death":
            surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.rect()[0], self.rect()[1]))
        elif self.in_air > 5:#self.action == "jump" or "jumpD" or "jump_run" or "jumpD_run":
            surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.rect()[0] - 8, self.rect()[1] + 2))
        else:
            surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.rect()[0] + self.renderPos_x, self.rect()[1] + self.renderPos_y))


class Enemy(PhysicsEntity):
    def __init__(self, game, enemy_type, pos, hp, size):
        super().__init__(game, f"enemies/{enemy_type}", pos, size)
        self.renderPos_x = 0  # Adjust the render Xposition of the sprite
        self.renderPos_y = 0  # Adjust the render Yposition of the sprite
        self.damage_timer = 0
        self.damage_taken_write = 0
        self.blink_timer = 0

        self.enemy_type = enemy_type
        self.hp = hp

        self.spawn = False
        self.moving = False
        self.move_direction = 0  # 0 for not moving, positive for right, negative for left

        self.hit_weapon = None
        self.damage_taken = 0
        self.damaged = False
        self.die = False
        self.delete = False
        self.activate_knockback = True  # Adress a potencial bug with entities changing size while in knockback
        self.knockback_taken = 0
        self.knock_back = 0
        self.hit_direction_right = False

    def set_action(self, action):
        super().set_action(action)

    def update(self, movement=(0, 0), tiles=None, boundaries=None, entities=None):
        super().update(movement=movement, tiles=tiles, boundaries=boundaries, entities=entities)
        if self.damage_timer < 1:
            self.damage_taken_write = 0

        if self.hp <= 0:
            self.die = True

        if self.damage_taken:
            if self.spawn:
                self.damaged = True
            else:
                self.damage_taken = 0

        if self.spawn and self.damaged:
            self.game.sfx["enemy_hit"].play()
            self.damage_timer = 15
            self.damage_taken_write = self.damage_taken
            if self.activate_knockback == True:
                self.knockback(self.knockback_taken)
            self.hp -= self.damage_taken
            self.damage_taken = 0
            self.damaged = False
            '''if not self.die:
                print("AAAAAAH")
                self.hit_weapon = None'''

        if self.spawn == True:
            if self.moving == False:
                pass

        if self.knock_back > 0:
            self.knock_back = max(0, self.knock_back - 5)
        if self.knock_back < 0:
            self.knock_back = min(0, self.knock_back + 5) 
        self.velocity[0] = self.knock_back * 0.15

        if self.hp <= 0 and not self.die and self.type != "ghost":
            self.game.sfx["enemy_killed"].play()

        # Remove entity when out of bounds
        if self.pos[0] > 610 or self.pos[0] < -10 or self.pos[1] > 330 or self.pos[1] < -100:
            self.delete = True

    def knockback(self, knockback_amount):
        if not self.knock_back:
            if self.hit["right"]:
                self.knock_back = -knockback_amount
                self.velocity[1] = -0.5
                self.hit_direction_right = True # Set hit direction
            elif self.hit["left"]:
                self.knock_back = knockback_amount
                self.velocity[1] = -0.5
                self.hit_direction_right = False # Set hit direction

    def render(self, surf):
        if self.action == "death":
            # Check hit direction to flip the death animation
            self.flip = self.hit_direction_right
            surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.rect()[0] + self.renderPos_x, self.rect()[1] + self.renderPos_y))
        elif self.spawn == False and self.action != "death":
            self.blink_timer += 1
            blink_interval = 8
            if self.blink_timer % blink_interval < blink_interval // 2:
                surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.rect()[0] + self.renderPos_x, self.rect()[1] + self.renderPos_y))
        elif self.damaged == True or self.damage_timer >= 0:
            self.damage_timer -= 1
            sprite = self.animation.sprite().copy()
            sprite.fill((255, 170, 170, 255), special_flags=pygame.BLEND_RGBA_MULT)
            surf.blit(pygame.transform.flip(sprite, self.flip, False), (self.rect()[0] + self.renderPos_x, self.rect()[1] + self.renderPos_y))
        else:
            surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.rect()[0] + self.renderPos_x, self.rect()[1] + self.renderPos_y))


class Zombie(Enemy):
    def __init__(self, game, pos, player_pos):
        self.player_pos = player_pos
        self.enemy_type = "zombie"
        self.points = 5
        super().__init__(game, self.enemy_type, pos, hp=6.4, size=(15, 34))
        if self.pos[1] > 280:
            self.set_action("spawn_ground")
        else:
            self.set_action("spawn_coffin")

    def update(self, tiles=None, boundaries=None, entities=None):
        frame_size = self.animation.sprite().get_size()
        super().update(movement=(self.move_direction * 1, 0), tiles=tiles, boundaries=boundaries, entities=entities)
        if not self.die and self.spawn:
            self.gravity()

        if self.spawn == False:
            self.gravity(0.05)
            self.renderPos_y = 0
        else:
            self.renderPos_y = -3
            self.renderPos_x = -5

        if self.spawn == True:
            self.size = (15, 34)
            if self.die == True:
                self.move_direction = 0
                self.set_action("death")
            elif self.moving == False and self.die == False:
                self.move_direction = random.choice([0.5, -0.5])  # Randomly choose left or right
                self.moving = True
                self.set_action("walk")
            elif self.collisions["right"] and self.move_direction > 0:
                self.move_direction = 0
                self.move_direction = -0.5
            elif self.collisions["left"]:
                self.move_direction = 0
                self.move_direction = 0.5

        elif self.action == "spawn_ground" or "spawn_coffin":
            if self.animation.done == True:
                self.spawn = True
            elif self.animation.frame <= 9:
                self.size = frame_size
            else:
                self.size = self.size


class Maddog(Enemy):
    def __init__(self, game, pos, player_pos):
        self.player_pos = player_pos
        self.enemy_type = "maddog"
        self.points = 10
        self.in_air = 0
        self.attack_timer = 60

        self.jump_timer = 60
        self.jump = False
        super().__init__(game, self.enemy_type, pos, hp=7.5, size=(22, 22))
        self.activate_knockback = False

    def update(self, tiles=None, boundaries=None, entities=None):
        frame_size = self.animation.sprite().get_size()
        super().update(movement=(self.move_direction * 1, 0), tiles=tiles, boundaries=boundaries, entities=entities)
        self.renderPos_y = -2
        if not self.flip:
            self.renderPos_x = -1
        elif self.flip:
            self.renderPos_x = -5
        self.spawn = True
        self.in_air += 1

        if not self.die:
            self.gravity()

            if self.in_air > 10 and not self.die:
                if self.velocity[1] < 0:
                    self.set_action("jump")
                elif self.velocity[1] > 1.5:
                    self.set_action("falling")
                    self.size = (18, 40)
                    self.renderPos_y = -8
                    self.renderPos_x = -2
            if self.in_air > 5 and not self.die:
                if not self.flip:
                    self.velocity[0] += 1
                elif self.flip:
                    self.velocity[0] -= 1
                    
            if self.jump == True and not self.die:
                self.velocity[1] = -5
                self.jump = False
                self.attack_timer = random.choice([60, 90, 120])

            elif self.attack_timer < 0 and not self.jump:
                self.set_action("attack")
            
            if self.action == "attack" and not self.jump:
                if self.pos[0] > self.player_pos[0]:
                    self.flip = True
                else:
                    self.flip = False
                self.jump_timer -= 1
                
            if self.jump_timer < 0 and self.jump == False:
                self.activate_knockback = False
                self.jump = True
                self.jump_timer = 60

            elif self.collisions["bottom"]:
                if self.in_air > 5:
                    self.pos[1] += self.size[1] - 30
                    self.size = (18, 30)
                    self.set_action("landing")
                self.in_air = 0
                if self.animation.done:
                    self.pos[1] += self.size[1] - 22
                    self.size = (18, 22)
                    self.set_action("idle")
                    self.activate_knockback = True
                if self.attack_timer >= 0:
                    self.attack_timer -= 1
        else:
            self.velocity[1] = 0
            self.set_action("death")
            self.renderPos_y = -5


class MaddogS(Enemy):
    def __init__(self, game, pos, player_pos):
        self.player_pos = player_pos
        self.enemy_type = "maddogS"
        self.points = 15
        self.in_air = 0
        self.attack_timer = 30

        self.jump_timer = 30
        self.jump = False
        super().__init__(game, self.enemy_type, pos, hp=19, size=(22, 22))
        self.activate_knockback = False

    def update(self, tiles=None, boundaries=None, entities=None):
        frame_size = self.animation.sprite().get_size()
        super().update(movement=(self.move_direction * 1, 0), tiles=tiles, boundaries=boundaries, entities=entities)
        self.renderPos_y = -2
        if not self.flip:
            self.renderPos_x = -1
        elif self.flip:
            self.renderPos_x = -5
        self.spawn = True
        self.in_air += 1

        if not self.die:
            self.gravity()

            if self.in_air > 10 and not self.die:
                if self.velocity[1] < 0:
                    self.set_action("jump")
                elif self.velocity[1] > 1.5:
                    self.set_action("falling")
                    self.size = (18, 40)
                    self.renderPos_y = -8
                    self.renderPos_x = -2
            if self.in_air > 5 and not self.die:
                if self.player_pos[1] - self.pos[1] > 80 or self.player_pos[0] - self.pos[0] < 30 or self.player_pos[0] - self.pos[0] > 30:
                    if self.player_pos[0] > self.pos[0]:
                        self.velocity[0] += 1
                    elif self.player_pos[0] < self.pos[0]:
                        self.velocity[0] -= 1

            if self.jump == True and not self.die:
                self.velocity[1] = -5
                self.jump = False
                self.attack_timer = random.choice([30, 60, 90])

            elif self.attack_timer < 0 and not self.jump:
                self.set_action("attack")
            
            if self.action == "attack" and not self.jump:
                if self.pos[0] > self.player_pos[0]:
                    self.flip = True
                else:
                    self.flip = False
                self.jump_timer -= 1
                
            if self.jump_timer < 0 and self.jump == False:
                self.activate_knockback = False
                self.jump = True
                self.jump_timer = 30

            elif self.collisions["bottom"]:
                if self.in_air > 5:
                    self.pos[1] += self.size[1] - 30
                    self.size = (18, 30)
                    self.set_action("landing")
                self.in_air = 0
                if self.animation.done:
                    self.pos[1] += self.size[1] - 22
                    self.size = (18, 22)
                    self.set_action("idle")
                    self.activate_knockback = True
                if self.attack_timer >= 0:
                    self.attack_timer -= 1
        else:
            self.velocity[1] = 0
            self.set_action("death")
            self.renderPos_y = -5


class Ghost(Enemy):
    def __init__(self, game, pos, player_pos):
        self.player_pos = player_pos
        self.enemy_type = "ghost"
        self.points = 7
        self.movingX_timer = 0
        self.movingY_timer = 0
        self.Nswirls = 60
        super().__init__(game, self.enemy_type, pos, hp=6.4, size=(26, 30))
        self.default_size = (26, 30)
        self.spawn_timer = random.choice([600, 800, 1000, 1200, 1400, 1600])
        self.set_action("moving_ball")
    def update(self, tiles=None, boundaries=None, entities=None):
        frame_size = self.animation.sprite().get_size()
        super().update(movement=(self.move_direction * 1, 0), tiles=tiles, boundaries=boundaries, entities=entities)

        if self.action == "moving_ball" and self.hit == True:
            self.spawn_timer = 0

        if not self.spawn and self.action != "spawning":
            if not self.spawn and self.spawn_timer > 0:
                self.spawn_timer -= 1
            elif self.spawn_timer <= 0:
                self.set_action("swirl")
                if self.action == "swirl":
                    self.move_direction = 0
                    self.velocity[1] = 0
                    self.Nswirls -= 1

            if self.Nswirls <= 0 and self.action != "spawning":
                self.set_action("spawning")
        
        if self.action == "spawning":
            if self.animation.done:
                self.spawn = True

        if self.action == "moving_ball":
            self.size = frame_size
            self.random_movement(speed=random.choice([0.8, 1.2, 1.6, 2.0]))

        if self.spawn == True and not self.die:
            self.size = self.default_size
            self.renderPos_y = -0
            self.renderPos_x = -5
            if (self.player_pos[0] - self.pos[0]) < -120 or (self.player_pos[0] - self.pos[0]) > 120 or (self.player_pos[1] - self.pos[1]) > 120 or (self.player_pos[1] - self.pos[1]) < -120:
                self.set_action("wandering")
                self.random_movement(speed=random.choice([0.6, 0.8, 1.0]))
            else:
                self.set_action("attack")
                if self.player_pos[0] < self.pos[0] - 10:
                    self.move_direction = -0.7 
                elif self.player_pos[0] > self.pos[0] + 10:
                    self.move_direction = 0.7

                if self.player_pos[1] < self.pos[1] - 10:
                    self.velocity[1] = -0.5
                elif self.player_pos[1] > self.pos[1] + 10:
                    self.velocity[1] = 0.5
        
        if self.die == True:
            self.move_direction = 0
            self.velocity[1] = 0
            self.set_action("death")
            self.renderPos_y = -5
        
        if self.hp <= 0 and not self.die:
            self.game.sfx["ghost_killed"].play()

    def random_movement(self, speed=1.0):
        # Up and down
        if self.pos[1] > 319:
            self.velocity[1] = -0.5
        elif self.pos[1] < 1:
            self.velocity[1] = 0.5
        elif self.movingY_timer <= 0:
            self.velocity[1] = random.choice([0.3 * speed, -0.3 * speed]) # Randomly choose up or down
            self.movingY_timer = random.choice([60, 80, 100, 120])
        if self.movingY_timer > 0:
            self.movingY_timer -= 1

        # Left and right
        if self.pos[0] > 599:
            self.move_direction = -1
        elif self.pos[0] < 1:
            self.move_direction = 1
        elif self.movingX_timer <= 0:
            self.move_direction = random.choice([0.7 * speed, -0.7 * speed])  # Randomly choose left or right
            self.movingX_timer = random.choice([60, 80, 100, 120])
        if self.movingX_timer > 0:
            self.movingX_timer -= 1

    def render(self, surf):
        super().render(surf)
        if self.spawn == False and self.action != "death":
            self.blink_timer += 1
            blink_interval = 15
            if self.blink_timer % blink_interval < blink_interval // 2:
                surf.blit(pygame.transform.flip(self.animation.sprite(), self.flip, False), (self.rect()[0] + self.renderPos_x, self.rect()[1] + self.renderPos_y))


class Weapon:
    def __init__(self, game, w_type, pos, flip, player_damage):
        self.game = game
        self.type = w_type
        self.weapons_damage = {"spear": [2.0, 25], "sword": [1.5, 15], "axe": [4.5, 30], "arrow": 1.0}
        self.damage_power = self.weapons_damage[w_type][0] * player_damage
        self.knockback_damage = min(60, self.weapons_damage[w_type][1] * player_damage)
        self.pos = list(pos)
        self.pos_adjust = False
        self.size = (0, 0)
        self.velocity = [0, 0]

        self.collisions = False
        self.hit = False
        self.hit_delay = 1
        self.Nhits = 0
        self.delete = False

        # Set animations
        self.flip = flip
        self.weapon = ""
        self.set_weapon(self.type)

        self.hitFalse_animation = Animation(load_images("weapons/hit_False")).copy()
        self.hitTrue_animation = Animation(load_images("weapons/hit_True")).copy()
        self.hit_animation_dur = 12

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_weapon(self, weapon):
        if weapon != self.weapon:
            self.weapon = weapon
            self.weapon = self.game.weaponsAndItems[self.type].copy()

    def show_hitbox(self, surf, color=(0, 0, 200)):
        pygame.draw.rect(surf, color, self.rect())

    def gravity(self, x=0.1):
        self.velocity[1] += x
        return True
    
    def update(self, movement=(0, 0), tiles=None, entities=None):
        if not self.pos_adjust:
            if self.flip:
                self.pos[0] -= 10
            else:
                self.pos[0] += 10
            self.pos_adjust = True
    
        self.size = self.weapon.sprite().get_size()
        self.collisions = False
        self.hit = False

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        weapon_rect = self.rect()

        if entities:
            for entity in entities:
                enemy_rect = entity.rect()
                if weapon_rect.colliderect(enemy_rect) and entity.die == False and not self.delete:
                    if entity.damaged == True:
                        self.delete = True
                    elif entity.damage_taken > 0:
                        self.delete = True
                    elif entity.enemy_type == "ghost" and entity.spawn == False:
                        self.hit = False
                    else:
                        self.hit = True
                        entity.hit_weapon = self.type
                        entity.damage_taken = round(self.damage_power, ndigits=3)
                        entity.knockback_taken = self.knockback_damage
                        self.Nhits += 1
                        self.hit_delay -= 1
                        
        if self.Nhits >= 1:
            self.damage_power = 0
        
        if self.hit_delay < 0:
            self.delete = True
        elif self.hit_delay == 0:
            self.hit_delay -= 1

        if tiles:
            for tile in tiles:
                if weapon_rect.colliderect(tile):
                    self.weapon = self.hitFalse_animation
                    self.collisions = True

        self.weapon.update() # Update animations, if any

        if self.pos[0] > 610 or self.pos[0] < -10 or self.pos[1] > 340 or self.pos[1] < -60 or self.collisions:
            self.weapon = self.hitFalse_animation
            self.delete = True
        
        if self.delete:
            self.velocity[0] = 0
            self.velocity[1] = 0
            if self.hit:
                self.weapon = self.hitTrue_animation
            elif not self.hit:
                self.weapon = self.hitFalse_animation
            self.hit_animation_dur -= 1
            self.weapon.update()

    def render(self, surf):
        surf.blit(pygame.transform.flip(self.weapon.sprite(), self.flip, False), (self.pos[0], self.pos[1]))


class Spear(Weapon):
    def __init__(self, game, pos, flip, player_damage):
        self.index = 1
        self.damage_power = 2.0
        super().__init__(game, "spear", pos, flip, player_damage)
        self.game.sfx[self.type + "_throw"].play()

    def update(self, tiles=None, entities=None):
        super().update(tiles=tiles, entities=entities)
        
        if not self.delete:
            if self.flip == False:
                self.velocity[0] = 4
            if self.flip == True:
                self.velocity[0] = -4
            
        # Adjust the position for the hit sprite
        if self.hit_animation_dur == 11:
            if not self.flip:
                self.pos[0] += 20
            else:
                self.pos[0] -= 10
            self.pos[1] -= 10


class Sword(Weapon):
    def __init__(self, game, pos, flip, player_damage):
        self.index = 2
        self.damage_power = 1.5
        super().__init__(game, "sword", pos, flip, player_damage)
        self.game.sfx[self.type + "_throw"].play()

    def update(self, tiles=None, entities=None):
        super().update(tiles=tiles, entities=entities)

        if not self.delete:
            if self.flip == False:
                self.velocity[0] = 5
            if self.flip == True:
                self.velocity[0] = -5
            
        # Adjust the position for the hit sprite
        if self.hit_animation_dur == 11:
            if not self.flip:
                self.pos[0] += 5
            else:
                self.pos[0] -= 2.5
            self.pos[1] -= 10


class Axe(Weapon):
    def __init__(self, game, pos, flip, player_damage):
        self.index = 3
        self.damage_power = 4.5
        super().__init__(game, "axe", pos, flip, player_damage)
        self.velocity[1] = -5
        self.game.sfx[self.type + "_throw"].play()
    
    def update(self, tiles=None, entities=None):
        super().update(tiles=tiles, entities=entities)
        
        if not self.delete:
            if self.flip == False:
                self.velocity[0] = 3
            if self.flip == True:
                self.velocity[0] = -3
        
        # Adjust the position for the hit sprite
        if self.hit_animation_dur == 11:
            if not self.flip:
                self.pos[0] += 10
            else:
                self.pos[0] -= 5

        self.gravity(x=0.2)

    def gravity(self, x=0.1):
        self.velocity[1] += x
        return True


class Arrow(Weapon):
    def __init__(self, game, pos, flip, player_damage):
        self.index = 4
        self.damage_power = 1.0 
        super().__init__(game, "arrow", pos, flip, player_damage)
    
    def update(self, tiles=None, entities=None):
        super().update(tiles=tiles, entities=entities)
        self.velocity[1] = -0.8

        if self.flip == False:
            self.velocity[0] = 3.5
        if self.flip == True:
            self.velocity[0] = -3.5


class Item:
    def __init__(self, game, item_type, pos):
        self.game = game
        self.type = item_type
        self.pos = list(pos)
        self.size = (20, 20)
        self.velocity = [0, 0]

        self.collisions = False

        self.drop = False
        self.pick_up = False
        self.delete = False

        # Set animations
        self.item = ""
        self.set_item(self.type)
        self.renderPos_x = 0  # Adjust the render Xposition of the sprite
        self.renderPos_y = 0  # Adjust the render Yposition of the sprite
        self.blink_timer = 0
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def show_hitbox(self, surf, color=(200, 0, 100)):
        pygame.draw.rect(surf, color, self.rect())
    
    def set_item(self, item):
        if item != self.item:
            self.item = item
            self.item = self.game.weaponsAndItems[self.type].copy()
    
    def gravity(self, x=0.1):
        self.pos[1] += x
        return True

    def update(self, player, tiles=None):
        if self.type == "hp_up":
            self.size = (17, 26)
        self.drop = True

        item_rect = self.rect()
        if not self.collisions:
            self.gravity()

        if tiles:
            for tile in tiles:
                if item_rect.colliderect(tile):
                    self.collisions = True

        player_rect = player.rect()
        if item_rect.colliderect(player_rect) and player.dead == False and not self.delete:
            player.item_taken = self.type
            player.pick_up = True
            self.pick_up = True
        
        if self.pick_up:
            self.delete = True

        if self.pos[0] > 590:
            self.pos[0] = 585
        elif self.pos[0] < 10:
            self.pos[0] = 15
        if self.pos[1] > 300:
            self.pos[1] = 295
        # Remove item when out of bounds
        if self.pos[0] > 610 or self.pos[0] < -10 or self.pos[1] > 330 or self.pos[1] < -100:
            self.delete = True
    
    def render(self, surf):
        if self.drop == True:
            self.blink_timer += 1
            blink_interval = 15
            if self.blink_timer % blink_interval < blink_interval // 2:
                surf.blit(self.item, (self.rect()[0] + self.renderPos_x, self.rect()[1] + self.renderPos_y))


class WeaponDrop(Item):
    def __init__(self, game, weapon_type, pos):
        super().__init__(game, weapon_type, pos)
        self.renderPos_x = -6  # The sprite doesn't render in the center, because of the different size of the image
        self.renderPos_y = -6
    
    def update(self, player, tiles=None):
        super().update(player, tiles=tiles)


class FireTorch:
    def __init__(self, game, pos, flip=False):
        self.game = game
        self.pos = list(pos)

        # Set animations
        self.flip = flip
        self.fire = self.game.animations["fire_collum"].copy()
    
    def update(self):
        self.fire.update()
    
    def render(self, surf):
        surf.blit(pygame.transform.flip(self.fire.sprite(), self.flip, False), (self.pos[0], self.pos[1]))