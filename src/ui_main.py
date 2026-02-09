import pygame

ORANGE = (255, 159, 15)
BLUE = (21, 96, 130)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (224, 15, 0)
LIGHT_GREY = (200, 200, 200)


def handle_button_toggles():
    # Toggle button function
    pass

#rename function to something less boring    
def main_ui_function(screen, window_width, window_height, width_scale_factor, height_scale_factor):
    pygame.init()
    global graph_mode

    # Creates the main window
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Plant Care System")
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_toggles()

        # Clear the screen
        screen.fill(BLUE)

        # Draw UI elements here (buttons, graphs, etc.)

        top_bar_rect = pygame.Rect(
        window_width * 0.05 * width_scale_factor,
        window_height * 0.03 * height_scale_factor,
        window_width * 0.9 * width_scale_factor,
        window_height * 0.06 * height_scale_factor
    )

        # Update the display
        pygame.display.flip()

      