# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Connor
#
# Created:     21-01-2021
# Copyright:   (c) Connor 2021
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import pygame
import copy
from random import randint
from random import choice
from time import sleep


class Draw:
    def __init__(self, win):
        self.window = win
        self.text = ""
        self.height = win.get_height()
        self.width = win.get_width()
        self.is_paused = 0
        self.characters = ["b", "#", "@", "!", "&"]

    def draw_on_window(
        self, text, previous_boxwidth, superscript, message_total_length
    ):

        box = text.get_rect()
        box.center = (
            (1000 // 2)
            + (previous_boxwidth)
            - (message_total_length // 2)
            + text.get_width() // 2,
            (500 // 2) - (25 * superscript),
        )
        self.window.blit(text, box)
        previous_boxwidth += text.get_width()

        return previous_boxwidth

    def get_length(self, message, global_scale, window_width):
        length = 0
        superscript = False
        for i in range(len(message)):
            if message[i] != "^":
                if superscript is True:
                    textsize = 40 * global_scale
                    imgsize = 30 * global_scale
                    font = pygame.font.SysFont("times", int(100 * global_scale))
                else:
                    textsize = 80 * global_scale
                    imgsize = 40 * global_scale
                    font = pygame.font.SysFont("times", int(150 * global_scale))
                if message[i] in self.characters:
                    length += imgsize
                else:
                    text = font.render(message[i], True, (0, 0, 0))
                    length += text.get_width()
            else:
                superscript = not superscript

        if length > window_width:
            length, global_scale = self.get_length(
                message, global_scale - 0.15, window_width
            )
        return length, global_scale

    def getDimensions(self, item, scale):
        box = item.get_rect()
        dimensions = (round(item.get_width() * scale), round(item.get_height() * scale))
        return dimensions

    def write_on_window(self, message):
        self.text = message
        message_total_length, global_scale = self.get_length(
            message, 1.0, self.width - 50
        )
        font_s = pygame.font.SysFont("times", int(100 * global_scale))
        font_m = pygame.font.SysFont("times", int(150 * global_scale))
        previous_boxwidth = 0
        superscript = 0
        for i in range(len(message)):

            if message[i] != "^":

                if superscript == 1:
                    font = font_s
                    scale = 0.75 * global_scale
                else:
                    font = font_m
                    scale = 1 * global_scale

                if message[i] in self.characters:
                    fileName = str(self.characters.index(message[i])) + ".png"
                    img = pygame.image.load(fileName)
                    dimensions = self.getDimensions(img, scale)
                    img = pygame.transform.scale(img, dimensions)
                    previous_boxwidth = self.draw_on_window(
                        img, previous_boxwidth, superscript, message_total_length
                    )
                else:
                    text = font.render(message[i], True, (0, 0, 0))
                    previous_boxwidth = self.draw_on_window(
                        text, previous_boxwidth, superscript, message_total_length
                    )

            else:
                superscript = not superscript

        pygame.display.flip()

    def draw_pause_screen(self):
        s = pygame.Surface((self.width / 4, self.height))
        s.set_alpha(150)
        s.fill((40, 80, 120))
        self.window.blit(s, (0, 0))
        pygame.display.flip()

    def undraw_pause_screen(self):
        self.window.fill((255, 255, 255))
        self.write_on_window(self.text)


def new_surface(win):
    return Draw(win)
