import pygame
# import numpy as np

# Variables
size = 1000
rows = 5
t = 100
border = size / (2 + rows)
border_rounded = size // (2 + rows)
margin = border_rounded // 10

bg_color = pygame.Color("black")
color_line = pygame.Color("grey")
border_color = pygame.Color("grey")
player_color = pygame.Color("red")
rewardColor = pygame.Color("green")

actionUp = 0
actionDown = 1
actionLeft = 2
actionRight = 3

pygame.init()

# Draw the scenario
screen = pygame.display.set_mode((size, size))

# Filling the background
screen.fill(bg_color)

# Set title and key icon
pygame.display.set_caption("Gym-minigrid")
key_icon = pygame.image.load('key.png')
pygame.display.set_icon(key_icon)


def draw_base(goal):
    # Drawing the border
    pygame.draw.rect(screen, border_color, pygame.Rect((0, 0), (size, border)))
    pygame.draw.rect(screen, border_color, pygame.Rect((0, 0), (border, size)))
    pygame.draw.rect(screen, border_color, pygame.Rect((0, size - border_rounded), (size, border)))
    pygame.draw.rect(screen, border_color, pygame.Rect((size - border_rounded, 0), (border, size)))

    pygame.draw.rect(screen, border_color, pygame.Rect((3 * border, border), (border + 1, 2 * border + 1)))
    pygame.draw.rect(screen, border_color, pygame.Rect((3 * border, 4 * border), (border + 1, 3 * border)))
    pygame.draw.rect(screen, rewardColor,
                     pygame.Rect((goal[0] * border + border, goal[1] * border + border), (border, border)))


def grid():
    # Formulate grid by drawing separated lines
    distance_btw_rows = border
    x = 0
    y = 0
    for i in range(rows - 1):
        # increment x and y to separate lines
        x += distance_btw_rows
        y += distance_btw_rows
        # vertical lines
        pygame.draw.line(screen, color_line, (x + border, border),
                         (x + border, size - border))
        # horizontal lines
        pygame.draw.line(screen, color_line, (border, y + border),
                         (size - border, y + border))    


# Define the classes
class Player:

    def __init__(self, initial_state, action):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.x3 = 0
        self.y3 = 0
        self.state2coordinate(initial_state, action)

    def show(self, color):
        global screen
        pygame.draw.polygon(screen, color, ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)))

    def state2coordinate(self, state, action):
        horizontal = state[1] * border + border + margin
        vertical = state[0] * border + border + margin
        side = border - 2 * margin

        if action == actionLeft:
            self.x1 = horizontal + side
            self.y1 = vertical + side
            self.x2 = horizontal
            self.y2 = vertical + side / 2
            self.x3 = horizontal + side
            self.y3 = vertical
        if action == actionRight:
            self.x1 = horizontal
            self.y1 = vertical
            self.x2 = horizontal + side
            self.y2 = vertical + side / 2
            self.x3 = horizontal
            self.y3 = vertical + side
        if action == actionUp:
            self.x1 = horizontal
            self.y1 = vertical + side
            self.x2 = horizontal + side / 2
            self.y2 = vertical
            self.x3 = horizontal + side
            self.y3 = vertical + side
        if action == actionDown:
            self.x1 = horizontal + side
            self.y1 = vertical
            self.x2 = horizontal + side / 2
            self.y2 = vertical + side
            self.x3 = horizontal
            self.y3 = vertical

    def update(self, state, action):
        self.show(bg_color)
        self.state2coordinate(state, action)
        self.show(player_color)


# update display
def redraw(goal, player, state, action):
    draw_base(goal)
    grid()
    player.update(state, action)
    pygame.display.flip()
    pygame.time.wait(t)


def animate(T, goal, action):
    # Create Objects
    player = Player(T[:, 0], action[0])  # initial state
    player.show(player_color)
    pygame.time.wait(3000)
    for i in range(T.shape[1]):
        state = T[:, i]
        print(state)
        redraw(goal, player, state, action[i - 1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quit")
                pygame.display.quit()
                pygame.quit()
                exit()

    running = True
    while running:
        # redraw the surface and update it repeatedly
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("quit")
                pygame.display.quit()
                pygame.quit()
                exit()


# if __name__ == "__main__":
#     T = np.array([[0, 1, 2, 2, 2, 2, 3, 4, 4], [0, 0, 0, 1, 2, 3, 3, 3, 4]])
#     animate(T)
