import pygame
import random
import time

ORANGE = (255, 159, 15)
BLUE = (21, 96, 130)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (224, 15, 0)

# Store points for the graph
# Use normalized readings (0 = bottom, 1 = top) so the graph scales with window size
points = [0.5]  # start point (center)
running = True
State_axis = ORANGE
last_update = time.time()
State_LCL = WHITE
State_UCL = WHITE
new_y = 0
screen_height = None
screen_width = None

def ui_run():
    global running, last_update, State_axis, State_LCL, State_UCL, points

    running = True
    pygame.init()
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    pygame.display.set_caption("Live Sensor Graph")
    clock = pygame.time.Clock()

    SAMPLE_INTERVAL = 1.0  # seconds between readings

    while running:
        clock.tick(60)
        w, h = screen.get_size()
        screen.fill(BLUE)

        # Layout margins (percentages)
        left = int(w * 0.05)
        right = int(w * 0.05)
        top = int(h * 0.15)
        bottom = int(h * 0.10)
        graph_w = w - left - right
        graph_h = h - top - bottom

        # Control limits as proportions from top of the graph area
        UCL_rel = 0.35
        LCL_rel = 0.65
        UCL_y = top + int(UCL_rel * graph_h)
        LCL_y = top + int(LCL_rel * graph_h)

        # Update state colors based on last reading (if any)
        if points:
            last_y_norm = points[-1]
            last_pixel_y = top + int((1 - last_y_norm) * graph_h)
            if last_pixel_y > LCL_y or last_pixel_y < UCL_y:
                State_axis = RED
                State_LCL = RED
                State_UCL = RED
            else:
                State_axis = ORANGE
                State_LCL = WHITE
                State_UCL = WHITE

        # Draw axes and control lines
        pygame.draw.line(screen, State_axis, (left, top + graph_h), (left + graph_w, top + graph_h), 2)
        pygame.draw.line(screen, State_axis, (left, top), (left, top + graph_h), 2)
        pygame.draw.line(screen, State_LCL, (left, LCL_y), (left + graph_w, LCL_y), 1)
        pygame.draw.line(screen, State_UCL, (left, UCL_y), (left + graph_w, UCL_y), 1)

        # Take a new reading every SAMPLE_INTERVAL seconds
        if time.time() - last_update > SAMPLE_INTERVAL:
            new_y = random.uniform(0.1, 0.9)  # normalized reading
            points.append(new_y)
            # keep number of samples reasonable for current width
            max_samples = max(10, graph_w // 8)
            if len(points) > max_samples:
                points = points[-max_samples:]
            last_update = time.time()

        # Draw stored points as a continuous line (evenly spaced across the graph width)
        num = len(points)
        if num > 1:
            pixel_points = []
            for i, yn in enumerate(points):
                x = left + int((i / (num - 1)) * graph_w)
                y = top + int((1 - yn) * graph_h)
                pixel_points.append((x, y))
            pygame.draw.lines(screen, BLACK, False, pixel_points, 2)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            

    pygame.quit()

  
def main_ui_run(fullscreen=False, size=(800, 600), fps=60):
    if not pygame.get_init():
        pygame.init()

    global screen_height, screen_width
    screen_info = pygame.display.Info()
    screen_width = screen_width or min(size[0], screen_info.current_w)
    screen_height = screen_height or min(size[1], screen_info.current_h)

    flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
    screen = pygame.display.set_mode((screen_width, screen_height), flags)
    pygame.display.set_caption("Main UI")

    clock = pygame.time.Clock()
    running = True
    minimized = False

    try:
        while running:
            clock.tick(fps)

            events = pygame.event.get()
            if not events:
                if minimized:
                    time.sleep(0.05)
                continue

            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.w, event.h
                    screen = pygame.display.set_mode((screen_width, screen_height), flags)
                elif hasattr(pygame, 'WINDOWEVENT') and event.type == pygame.WINDOWEVENT:
                    if getattr(event, 'event', None) == pygame.WINDOWEVENT_MINIMIZED:
                        minimized = True
                    elif getattr(event, 'event', None) in (pygame.WINDOWEVENT_RESTORED, pygame.WINDOWEVENT_MAXIMIZED):
                        minimized = False

            if not minimized:
                w, h = screen.get_size()
                rect = pygame.Rect(int(w * 0.05), int(h * 0.05), int(w * 0.9), int(h * 0.05))
                screen.fill(BLUE)
                pygame.draw.rect(screen, BLACK, rect)  # filled
                pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main_ui_run()                