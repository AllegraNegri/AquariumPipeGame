# import all of the necessary libraries
import random
import sys, pygame
import os
from pygame.locals import *
import AquariumGraphics

game_side_padding = 25


class Food():
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.radius = 15
        self.width = 2 * self.radius
        self.height = self.width
        self.speed = random.randint(1, 5)

    def move_down(self):
        ######################################################
        # Q7: Fill in this method
        ######################################################
        self.y += self.speed


class PoisonousFood(Food):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.speed = self.speed * 2

    def move_down(self):
        self.y += self.speed


class Pipe():
    def __init__(self, x):
        self.x = x
        self.y = 100
        self.radius = 70
        # list of Food objects which have been added to this pipe
        self.food_pieces = []


    def add_food(self):
        addingfood = random.randint(1, 100)
        if addingfood <= 60:
            self.food_pieces.append(Food(self.x, 49))
        else:
            self.food_pieces.append(PoisonousFood(self.x,49))

    def move_food(self, boundary_y, player):
        ######################################################
        # Q9: Remove food from self.food_pieces if it falls outside the game
        ######################################################
        counter = 0
        for food in self.food_pieces:
            if food.y > boundary_y:
                self.food_pieces.remove(food)
            food.move_down()

            if food.x < player.width + player.x \
                    and food.width + food.x > player.x \
                    and food.y + food.height > player.y \
                    and food.y < player.y + player.height:
                self.food_pieces.remove(food)
                if isinstance(food, PoisonousFood):
                    counter -=1
                else:
                    counter += 1


        return counter


class Fish(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, aquarium_width):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_pos
        self.y = y_pos
        self.aquarium_width = aquarium_width
        self.speed = 15

        ######################################################
        # Q1: Set the height and width of the player to suitable values
        ######################################################
        self.height = 56
        self.width = 70

        # Load image for player
        # (you can open the image in the assets folder to see what it looks like)
        image_unscaledleft = pygame.image.load(os.path.join("assets", "goldfish_left.png"))
        image_unscaledright = pygame.image.load(os.path.join("assets", "goldfish_right.png"))

        # Scale the player's character have the specified height and width
        self.image_left = pygame.transform.rotate(pygame.transform.scale(
            image_unscaledleft, (self.width, self.height)), 0)

        self.rect = self.image_left.get_rect()
        self.image = self.image_left

        self.image_right = pygame.transform.rotate(pygame.transform.scale(
            image_unscaledright, (self.width, self.height)), 0)

        self.rect = self.image_right.get_rect()

    def handle_movement(self, keys_pressed):
        """
        Update player's position according to the key pressed
        """
        if keys_pressed[pygame.K_LEFT] and self.x >= 30:
            self.x -= self.speed
            self.image = self.image_left
        elif keys_pressed[pygame.K_RIGHT] and self.x <= 820:
            self.x += self.speed
            self.image = self.image_right
        else:
            return
        self.rect.x = self.x


class Aquarium():
    def __init__(self, width, height):
        ## initialise pygame
        pygame.init()
        pygame.font.init()

        self.score = 0
        self.game_running = True
        self.prob_food = 0.05
        ## game constants
        self.width = width
        self.height = height

        ## player (the fish)
        self.player = Fish(x_pos=width / 2,
                           y_pos=height * 9 / 10,
                           aquarium_width=self.width)

        ## pipe
        self.pipes = [Pipe(100), Pipe(200), Pipe(300)]


        ## interface
        self.DISPLAY = AquariumGraphics.setup_display(self.width, self.height)

        ## draw initial board
        self.draw()

    def draw(self):
        # A wrapper around the `AquariumGraphics.draw_board` function that picks all
        # the right components of `self`.
        AquariumGraphics.draw_board(self.DISPLAY, self.width, self.height, self.score,
                                    self.game_running, self.player, self.pipes)

    def game_loop(self):
        while self.game_running:
            ######################################################
            # Q6: Uncomment self.pipe.add_food()
            ######################################################
            # Add food to the pipe
            # self.pipe.add_food()
            for pipe in self.pipes:
                addingfood = random.randint(1, 100)
                if addingfood / 100 < self.prob_food:
                    pipe.add_food()

            # Process all events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

            # Check which key has been pressed (if any) and move player accordingly
            keys_pressed = pygame.key.get_pressed()
            self.player.handle_movement(keys_pressed)

            # Move food down pipe
            for pipe in self.pipes:
                counter = pipe.move_food(boundary_y=self.height + AquariumGraphics.top_offset, player=self.player)
                self.score += counter

                # Refresh the display and loop back
            self.draw()
            pygame.display.update()

            pygame.time.wait(40)

        # Once the game is finished, print the user's score and wait for the `QUIT` event.
        # Note: in its current form, this game doesn't end without the user closing the application
        # since the player can't lose. However, if you extend the game to enable the player to lose,
        # the following code will be useful.
        print('SCORE:  ', self.score)
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            pygame.time.wait(40)
