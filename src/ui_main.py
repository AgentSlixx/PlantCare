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
user_input = ""
output_lines = []  
MAX_OUTPUT_LINES = 20

def log_output(message): #Makes sure that the terminal in the UI doesn't exceed 20 lines of code
    global output_lines
    output_lines.append(str(message))
    if len(output_lines) > MAX_OUTPUT_LINES:
        output_lines.pop(0)


# Toggle button function 
def handle_graph_toggle(event, window_width, window_height, width_scale_factor, height_scale_factor):
    global graph_mode

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        graph_btn_rect = pygame.Rect(
            window_width * 0.07 * width_scale_factor,
            window_height * 0.55 * height_scale_factor,
            window_width * 0.06 * width_scale_factor,
            window_height * 0.10 * height_scale_factor
        )

        if graph_btn_rect.collidepoint(mouse_pos):
            graph_mode = not graph_mode


# Main UI draw function
def draw_graph_mode_ui(screen, window_width, window_height, width_scale_factor, height_scale_factor):
    global graph_mode

    font_title = pygame.font.Font(None, int(36 * height_scale_factor))
    font_generic = pygame.font.Font(None, int(24 * height_scale_factor))
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
        label_text = font_generic.render(labels[i], True, BLACK)
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

    # Toggle button (graph mode) on left
    btn_y = window_height * 0.55 * height_scale_factor
    btn_w = window_width * 0.06 * width_scale_factor
    btn_h = window_height * 0.10 * height_scale_factor

    graph_btn = pygame.Rect(window_width * 0.07 * width_scale_factor, btn_y, btn_w, btn_h)
    pygame.draw.rect(screen, LIGHT_GREY, graph_btn)

    # Red cross when active
    if graph_mode:
        pygame.draw.line(screen, RED, graph_btn.topleft, graph_btn.bottomright, 3)
        pygame.draw.line(screen, RED, graph_btn.bottomleft, graph_btn.topright, 3)
    else:
        for i in range(4):
            x = graph_area.x + spacing * i + spacing * 0.15
            value_rect = pygame.Rect(x, graph_area.bottom - axis_height, spacing * 0.6, 30)
            pygame.draw.rect(screen, LIGHT_GREY, value_rect)
            value_text = font_small.render("Value: --", True, BLACK)
            screen.blit(value_text, (value_rect.x + 8, value_rect.y + 6))

    # Button label
    screen.blit(font_small.render("GRAPH MODE", True, WHITE), (graph_btn.x , graph_btn.bottom + 6))

    # Terminal/output area to the right of button
    term_rect = pygame.Rect(
        window_width * 0.25 * width_scale_factor,
        window_height * 0.52 * height_scale_factor,
        window_width * 0.68 * width_scale_factor,
        btn_h * 1.5
    )
    pygame.draw.rect(screen, BLACK, term_rect)

    # render recent output lines inside the terminal box
    line_height = font_small.get_height()
    max_lines = int(term_rect.height // line_height) - 1
    for i, line in enumerate(output_lines[-max_lines:]):
        text_surf = font_small.render(line, True, WHITE)
        screen.blit(text_surf, (term_rect.x + 5, term_rect.y + 5 + i * line_height))

    # Bottom input box
    bottom_bar_rect = pygame.Rect(
        window_width * 0.07 * width_scale_factor,
        window_height * 0.78 * height_scale_factor,
        window_width * 0.4 * width_scale_factor,
        window_height * 0.08 * height_scale_factor
    )

    pygame.draw.rect(screen, WHITE, bottom_bar_rect, border_radius=4)

    if user_input:
        input_text = font_generic.render(user_input, True, BLACK)
    else:
        input_text = font_generic.render("Enter commands here ", True, BLACK)
    
    screen.blit(input_text, (bottom_bar_rect.x + 12, bottom_bar_rect.y + 18))

    # Help box
    command_box_rect = pygame.Rect(
        window_width * 0.52 * width_scale_factor,
        window_height * 0.78 * height_scale_factor,
        window_width * 0.4 * width_scale_factor,
        window_height * 0.08 * height_scale_factor
    )
    pygame.draw.rect(screen, WHITE, command_box_rect, border_radius=4)
    screen.blit(font_generic.render("Guide: ", True, BLACK), (command_box_rect.x + 12, command_box_rect.y + 18))
    screen.blit(font_small.render("- Type commands in the left box", True, BLACK), (command_box_rect.x + 12, command_box_rect.y + 40))
    screen.blit(font_small.render("- Click 'Graph Mode' to toggle graph display", True, BLACK), (command_box_rect.x + 12, command_box_rect.y + 60))

    # Command list box
    command_list_rect = pygame.Rect(
        window_width * 0.07 * width_scale_factor,
        window_height * 0.88 * height_scale_factor,
        window_width * 0.4 * width_scale_factor,
        window_height * 0.10 * height_scale_factor
    )
    pygame.draw.rect(screen, WHITE, command_list_rect, border_radius=4)
    commands = [
        "Command List:",
        "water <ml>",
        "sunlight <lux>",
        "temperature <C>",
        "humidity <%>"
    ]
    line_y = command_list_rect.y + 8
    for cmd in commands:
        cmd_text = font_small.render(cmd, True, BLACK)
        screen.blit(cmd_text, (command_list_rect.x + 12, line_y))
        line_y += 18

def main_ui_run():
    global running, screen_height, screen_width, user_input, graph_mode

    running = True
    user_input = ""
    graph_mode = False

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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN: 
                    if user_input.strip() != "":
                        log_output(f"> {user_input}")  
                        if user_input.lower() == "help":
                            log_output("Available commands: help, water, sunlight, status")
                        elif user_input.lower() == "status":
                            log_output("Plant status: Humidity=--, Moisture=--, Sunlight=--, Temperature=--")
                        else:
                            log_output("Unknown command")
                    user_input = ""  
                elif event.unicode.isprintable():
                    user_input += event.unicode #appends only if it's a valid character

            handle_graph_toggle(event, window_width, window_height, width_scale_factor, height_scale_factor)

        draw_graph_mode_ui(screen, window_width, window_height, width_scale_factor, height_scale_factor)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main_ui_run()
