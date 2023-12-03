import os
import random
import time

import cv2
import pygame

pygame.init()

dir_path = os.path.dirname(__file__)
shapes_dir = os.path.join(dir_path, "demo_images/shapes")
actions_dir = os.path.join(dir_path, "demo_images/actions")


class ShapeColourSimDemo:

    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.colour = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.shape_num = 0
        self.shapes = ["blue-circle.png","blue-square.png","green-circle.png","green-triangle.png","red-square.png","red-triangle.png"]
        self.actions_library = {"blue-circle.png":"squish",'green-circle.png':'stretch','green-triangle.png':'distort','blue-square.png':'squeeze','red-square.png':'shrink','red-triangle.png':'disappear'}
        self.squish_images = ["squish_01.png","squish_02.png","squish_03.png","squish_04.png","squish_05.png","squish_06.png","squish_07.png"]
        self.stretch_images = ["stretch_01.png","stretch_02.png","stretch_03.png","stretch_04.png","stretch_05.png","stretch_06.png","stretch_07.png"]
        self.shrink_images = ["shrink_01.png","shrink_02.png","shrink_03.png","shrink_04.png","shrink_05.png","shrink_06.png","shrink_07.png"]
        self.disappear_images = ["disappear_01.png","disappear_02.png","disappear_03.png","disappear_04.png","disappear_05.png","disappear_06.png","disappear_07.png"]
        self.squeeze_images = ["squeeze_01.png","squeeze_02.png","squeeze_03.png","squeeze_04.png","squeeze_05.png","squeeze_06.png","squeeze_07.png"]
        self.distort_images = ["distort_01.png","distort_02.png","distort_03.png","distort_04.png","distort_05.png","distort_06.png","distort_07.png"]

    def step(self,action):

        if not action == "":
            if action == self.actions_library.get(self.shapes[self.shape_num]):
                if action == "squeeze":
                    self.animate(self.squeeze_images,action)
                elif action == "stretch":
                    self.animate(self.stretch_images,action)
                elif action == "disappear":
                    self.animate(self.disappear_images,action)
                elif action == "distort":
                    self.animate(self.distort_images,action)
                elif action == "shrink":
                    self.animate(self.shrink_images,action)
                elif action == "squish":
                    self.animate(self.squish_images,action)
            else:
                shape = pygame.image.load(os.path.join(dir_path,"demo_images/actions/error.png"))
                shape = pygame.transform.scale_by(shape,0.5)
                self.display_image(shape)
            
            if self.shape_num >= len(self.shapes) - 1:
                self.shape_num = 0
            else:
                self.shape_num += 1

        time.sleep(1)
        cv2_image,py_shape = self.get_array_image_filename(self.shape_num)
        self.display_image(py_shape)
        time.sleep(1)
  
        return cv2_image

    def display_image(self,shape):
        shape_pos = shape.get_rect()  # default position is topleft = (0,0)
        shape_pos.center = (self.WIDTH / 2, self.HEIGHT / 2)
        self.screen.fill(self.colour)  # Without this, the previous signs appear on the screen.
        self.screen.blit(shape, shape_pos)  # Draws the image on the screen
        pygame.display.flip()  # Update & draw the game screen

    def animate(self,image_list,action):
        for image in image_list:
            shape = pygame.image.load(os.path.join(dir_path,f"demo_images/actions/{action}/{image}"))
            shape = pygame.transform.scale_by(shape,0.5)
            self.display_image(shape)
            time.sleep(0.1)

    def get_array_image_filename(self,shape_num):
        filename = os.path.join(shapes_dir,self.shapes[shape_num])  # Out of range error, need to address this.
        image = cv2.imread(filename)
        shape = pygame.image.load(filename)
        return image,shape
