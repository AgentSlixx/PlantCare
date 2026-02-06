import pygame

ORANGE = (255, 159, 15)
BLUE = (21, 96, 130)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (224, 15, 0)
LIGHT_GREY = (200, 200, 200)

running = True
screen_height = None
screen_width = None
graph_mode = False


# Toggle button function
def handle_graph_toggle(event, window_width, window_height, width_scale_factor, height_scale_factor):
    global graph_mode

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        mid_btn_rect = pygame.Rect(
            window_width * 0.47 * width_scale_factor,
            window_height * 0.55 * height_scale_factor,
            window_width * 0.06 * width_scale_factor,
            window_height * 0.10 * height_scale_factor
        )

        if mid_btn_rect.collidepoint(mouse_pos):
            graph_mode = not graph_mode


# Main UI draw function
def draw_graph_mode_ui(screen, window_width, window_height, width_scale_factor, height_scale_factor):
    global graph_mode

    font_title = pygame.font.Font(None, int(36 * height_scale_factor))
    font_label = pygame.font.Font(None, int(24 * height_scale_factor))
    font_small = pygame.font.Font(None, int(22 * height_scale_factor))

    # Top black bar
    top_bar_rect = pygame.Rect(
        window_width * 0.05 * width_scale_factor,
        window_height * 0.03 * height_scale_factor,
        window_width * 0.9 * width_scale_factor,
        window_height * 0.06 * height_scale_factor
    )

    pygame.draw.rect(screen, BLACK, top_bar_rect)
    title_text = font_title.render("Plant Care System", True, WHITE)
    screen.blit(title_text, (top_bar_rect.centerx - title_text.get_width() // 2, top_bar_rect.y + 10))

    # Sensor label boxes
    labels = ["Humidity", "Temperature", "Moisture", "Sunlight"]
    stat_box_y = window_height * 0.13 * height_scale_factor
    stat_box_width = window_width * 0.18 * width_scale_factor
    spacing = window_width * 0.22 * width_scale_factor

    for i in range(4):
        x = window_width * 0.07 * width_scale_factor + spacing * i
        label_rect = pygame.Rect(x, stat_box_y, stat_box_width, window_height * 0.05 * height_scale_factor)
        pygame.draw.rect(screen, WHITE, label_rect)
        label_text = font_label.render(labels[i], True, BLACK)
        screen.blit(label_text, (label_rect.x + 8, label_rect.y + 6))

    # Graph display area
    graph_area = pygame.Rect(
        window_width * 0.07 * width_scale_factor,
        window_height * 0.20 * height_scale_factor,
        window_width * 0.86 * width_scale_factor,
        window_height * 0.28 * height_scale_factor
    )

    pygame.draw.rect(screen, BLUE, graph_area, 2)

    # Graph mode
    spacing = graph_area.width / 4
    axis_height = graph_area.height * 0.75

    if graph_mode:
        for i in range(4):
            x_origin = graph_area.x + spacing * i + spacing * 0.15
            y_origin = graph_area.bottom - 15

            # Vertical axis
            pygame.draw.line(screen, WHITE, (x_origin, y_origin), (x_origin, y_origin - axis_height), 2)

            # Horizontal axis
            pygame.draw.line(screen, WHITE, (x_origin, y_origin), (x_origin + spacing * 0.6, y_origin), 2)

    # Toggle buttons
    btn_y = window_height * 0.55 * height_scale_factor
    btn_w = window_width * 0.06 * width_scale_factor
    btn_h = window_height * 0.10 * height_scale_factor

    left_btn  = pygame.Rect(window_width * 0.28 * width_scale_factor, btn_y, btn_w, btn_h)
    mid_btn   = pygame.Rect(window_width * 0.47 * width_scale_factor, btn_y, btn_w, btn_h)
    right_btn = pygame.Rect(window_width * 0.66 * width_scale_factor, btn_y, btn_w, btn_h)

    pygame.draw.rect(screen, LIGHT_GREY, left_btn)
    pygame.draw.rect(screen, LIGHT_GREY, mid_btn)
    pygame.draw.rect(screen, LIGHT_GREY, right_btn)

    # Red cross on graph mode
    if graph_mode:
        pygame.draw.line(screen, RED, mid_btn.topleft, mid_btn.bottomright, 3)
        pygame.draw.line(screen, RED, mid_btn.bottomleft, mid_btn.topright, 3)

    # Button labels
    screen.blit(font_small.render("WORK IN PROGRESS", True, WHITE), (left_btn.x - 15, left_btn.bottom + 6))
    screen.blit(font_small.render("GRAPH MODE", True, WHITE), (mid_btn.x + 8, mid_btn.bottom + 6))
    screen.blit(font_small.render("WORK IN PROGRESS", True, WHITE), (right_btn.x - 15, right_btn.bottom + 6))

    # Bottom text box
    bottom_bar_rect = pygame.Rect(
        window_width * 0.07 * width_scale_factor,
        window_height * 0.78 * height_scale_factor,
        window_width * 0.86 * width_scale_factor,
        window_height * 0.08 * height_scale_factor
    )

    pygame.draw.rect(screen, WHITE, bottom_bar_rect, border_radius=4)

    bottom_text = font_label.render(
        "TEXT PLACEHOLDER — advice will appear here later",
        True, BLACK
    )

    screen.blit(bottom_text, (bottom_bar_rect.x + 12, bottom_bar_rect.y + 18))


def main_ui_run():
    global running, screen_height, screen_width

    pygame.init()

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    window_width = screen_width
    window_height = screen_height

    screen = pygame.display.set_mode((window_width, int(window_height * 0.93)), pygame.RESIZABLE)
    pygame.display.set_caption("Main UI")

    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        width_scale_factor = screen.get_width() / screen_width
        height_scale_factor = screen.get_height() / screen_height

        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            handle_graph_toggle(event, window_width, window_height, width_scale_factor, height_scale_factor)

        draw_graph_mode_ui(screen, window_width, window_height, width_scale_factor, height_scale_factor)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main_ui_run()
