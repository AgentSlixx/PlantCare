import pygame
import random
import time

ORANGE = (255, 159, 15)
BLUE = (35, 155, 247)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (224, 15, 0)

# Store points for the graph
points = [(50, 200)]  # start point
running = True
State_axis = ORANGE
last_update = time.time()
State_LCL = WHITE
State_UCL = WHITE
new_y = 0


def ui_run():
    global running, new_y, last_update, State_axis, State_LCL, State_UCL
    
    running = True  
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Live Sensor Graph")
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(90)  #Stops the program from running > 90 frames per second
        screen.fill(BLUE)
        
        # Update state colors based on new_y
        if new_y > 260 or new_y < 140:
            State_axis = RED
            State_LCL = RED
            State_UCL = RED
        else:
            State_axis = ORANGE
            State_LCL = WHITE
            State_UCL = WHITE    
        
        # Draw axes
        pygame.draw.line(screen, State_axis, (50, 350), (550, 350), 2)  # x-axis of graph
        pygame.draw.line(screen, State_axis, (50, 50), (50, 350), 2)    # y-axis of graph
        pygame.draw.line(screen, State_LCL, (50, 260), (550, 260), 1)  # LCL
        pygame.draw.line(screen, State_UCL, (50, 140), (550, 140), 1)  # UCL
        
        # Take a new reading every 1 second
        if time.time() - last_update > 1:
            last_point = points[-1]
            new_x = last_point[0] + 10
            new_y = random.randint(50, 350)
            points.append((new_x, new_y))
            last_update = time.time()
        
        # Draw all stored points as a continuous line
        if len(points) > 1:
            pygame.draw.lines(screen, BLACK, False, points, 4)

        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

    pygame.quit()

  
print("hello")