import os
import pygame

BASE_IMG_PATH = "assets/img/"

def load_image(path, key=(0, 0, 0), scale=1.0):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey(key)
    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images


def load_images_dict(path):
    images = {}
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images[str(img_name)] = load_image(path + "/" + img_name)
        #images.append(load_image(path + "/" + img_name))
    return images


def show_hitbox(entity, screen):
        rect = pygame.Rect(entity.pos[0], entity.pos[1], entity.size[0], entity.size[1])
        pygame.draw.rect(screen, (0, 200, 0), rect)


class Animation:
    def __init__(self, images, img_dur=8, loop=False, done=False):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = done
        self.frame = 0
        self.animation_Nframes = len(self.images) - 1
        self.time = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop, done=self.done)

    def update(self):
        self.time += 1
        if self.loop:
            if self.time >= self.img_duration:
                self.frame += 1
                self.time = 0
            if self.frame >= len(self.images):
                self.frame = 0
                self.time = 0
        else:
            if self.frame == self.animation_Nframes and self.time >= self.img_duration:
                self.done = True
                self.time = 0
            elif self.done == False:
                if self.time >= self.img_duration:
                    self.frame += 1
                    self.time = 0

    def sprite(self):
        return self.images[self.frame]
