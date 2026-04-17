import time
import pygame
import simulator

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
commands = [
    "water <ml> - Add water to increase moisture",
    "sunlight <lux> - Add artificial sunlight",
    "temperature <C> - Adjust temperature",
    "humidity <%> - Increase humidity",
    "help - Show this command list",
    "clear - Clear the console output",
    "quit - Exit the program",
]

def log_output(message):
    global output_lines
    output_lines.append(str(message))
    if len(output_lines) > MAX_OUTPUT_LINES:
        output_lines.pop(0)

def clear_output():
    global output_lines
    output_lines = []

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

def draw_graph_mode_ui(screen, window_width, window_height, width_scale_factor, height_scale_factor):
    global graph_mode, user_input, output_lines

    font_title = pygame.font.Font(None, int(36 * height_scale_factor))
    font_generic = pygame.font.Font(None, int(24 * height_scale_factor))        
    font_small = pygame.font.Font(None, int(22 * height_scale_factor))

    # Top bar
    top_bar_rect = pygame.Rect(
        window_width * 0.05 * width_scale_factor,
        window_height * 0.03 * height_scale_factor,
        window_width * 0.9 * width_scale_factor,
        window_height * 0.06 * height_scale_factor
    )
    pygame.draw.rect(screen, BLACK, top_bar_rect)
    title_text = font_title.render("Plant Care System", True, WHITE)
    screen.blit(title_text, (top_bar_rect.centerx - title_text.get_width() // 2, top_bar_rect.y + 10))

    # Display selected plant name
    if simulator.selected_plant:
        plant_name = simulator.selected_plant['name']
        plant_text = font_generic.render(f"Selected Plant: {plant_name}", True, WHITE)
        screen.blit(plant_text, (top_bar_rect.x + 10, top_bar_rect.y + top_bar_rect.height + 10))

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

    spacing = graph_area.width / 4
    axis_height = graph_area.height * 0.75

    if graph_mode:
        for i in range(4):
            x_origin = graph_area.x + spacing * i + spacing * 0.15
            y_origin = graph_area.bottom - 15
            pygame.draw.line(screen, WHITE, (x_origin, y_origin), (x_origin, y_origin - axis_height), 2)
            pygame.draw.line(screen, WHITE, (x_origin, y_origin), (x_origin + spacing * 0.6, y_origin), 2)

        # Add UCL/LCL lines and axis labels if plant selected
        if simulator.selected_plant:
            plant = simulator.selected_plant
            keys = ['humidity', 'temperature', 'moisture', 'sunlight']
            limits_mapping = {
                'humidity': 'humidity_limits',
                'temperature': 'temperature_limits',
                'moisture': 'moisture_limits',
                'sunlight': 'light_limits'
            }
            for i, key in enumerate(keys):
                bounds = simulator.Physical_bounds[key]
                min_val, max_val = bounds
                plant_limits = plant[limits_mapping[key]]
                plant_min, plant_max = plant_limits
                x_origin = graph_area.x + spacing * i + spacing * 0.15
                y_origin = graph_area.bottom - 15
                axis_height = graph_area.height * 0.75

                def y_pos(v):
                    if max_val == min_val:
                        return y_origin
                    return y_origin - ((v - min_val) / (max_val - min_val)) * axis_height

                # Draw UCL and LCL lines
                ucl_y = y_pos(plant_max)
                lcl_y = y_pos(plant_min)
                line_start_x = x_origin
                line_end_x = x_origin + spacing * 0.6
                pygame.draw.line(screen, RED, (line_start_x, ucl_y), (line_end_x, ucl_y), 2)
                pygame.draw.line(screen, RED, (line_start_x, lcl_y), (line_end_x, lcl_y), 2)

                # Add axis labels
                min_label = font_small.render(f'{min_val}', True, WHITE)
                max_label = font_small.render(f'{max_val}', True, WHITE)
                screen.blit(min_label, (x_origin - 40, y_origin - 10))
                screen.blit(max_label, (x_origin - 40, y_origin - axis_height - 10))

                # Draw current value marker
                if simulator.selected_plant:
                    value = simulator.selected_plant.get(key, 0)
                    plant_limits = simulator.selected_plant[limits_mapping[key]]
                    min_limit, max_limit = plant_limits
                    color = RED if value < min_limit or value > max_limit else WHITE
                    y_val = y_pos(value)
                    pygame.draw.line(screen, color, (x_origin, y_val), (x_origin + spacing * 0.6, y_val), 3)

    # Graph toggle button
    btn_y = window_height * 0.55 * height_scale_factor
    btn_w = window_width * 0.06 * width_scale_factor
    btn_h = window_height * 0.10 * height_scale_factor
    graph_btn = pygame.Rect(window_width * 0.07 * width_scale_factor, btn_y, btn_w, btn_h)
    pygame.draw.rect(screen, LIGHT_GREY, graph_btn)

    if graph_mode:
        pygame.draw.line(screen, RED, graph_btn.topleft, graph_btn.bottomright, 3)
        pygame.draw.line(screen, RED, graph_btn.bottomleft, graph_btn.topright, 3)
    else:
        for i in range(4):
            x = graph_area.x + spacing * i + spacing * 0.15
            value_rect = pygame.Rect(x, graph_area.bottom - axis_height, spacing * 0.6, 30)
            pygame.draw.rect(screen, LIGHT_GREY, value_rect)
            if simulator.selected_plant:
                key = ['humidity', 'temperature', 'moisture', 'sunlight'][i]
                value = simulator.selected_plant.get(key, 0)
                limits_key = 'light_limits' if key == 'sunlight' else f'{key}_limits'
                min_limit, max_limit = simulator.selected_plant[limits_key]
                color = RED if value < min_limit or value > max_limit else BLACK
                value_text = font_small.render(f"{value:.1f}", True, color)
            else:
                value_text = font_small.render("--", True, BLACK)
            screen.blit(value_text, (value_rect.x + 8, value_rect.y + 6))       

    screen.blit(font_small.render("GRAPH MODE", True, WHITE), (graph_btn.x, graph_btn.bottom + 6))

    # Directions box
    directions_rect = pygame.Rect(
        window_width * 0.55 * width_scale_factor,
        window_height * 0.84 * height_scale_factor,
        window_width * 0.38 * width_scale_factor,
        window_height * 0.15 * height_scale_factor
    )
    pygame.draw.rect(screen, WHITE, directions_rect, border_radius=4)
    screen.blit(font_generic.render("Plant Care Directions:", True, BLACK), (directions_rect.x + 10, directions_rect.y + 5))

    directions = []
    if simulator.selected_plant:
        plant = simulator.selected_plant_object()
        readings = simulator.current_readings()
        if plant:
            score = round(simulator.current_health_score, 1)
            category = simulator.current_health_category()
            directions.append(f"Health: {score}/100 ({category})")
            directions.extend(plant.care_advice(readings))
    
    if not directions:
        directions.append("Plant conditions are optimal!")

    for i, dir_text in enumerate(directions[:3]):  # Now can fit 3
        screen.blit(font_small.render(dir_text, True, BLACK), (directions_rect.x + 10, directions_rect.y + 25 + i * 18))

    # Terminal/output area
    term_rect = pygame.Rect(
        window_width * 0.25 * width_scale_factor,
        window_height * 0.52 * height_scale_factor,
        window_width * 0.68 * width_scale_factor,
        btn_h * 1.5
    )
    pygame.draw.rect(screen, BLACK, term_rect)
    line_height = font_small.get_height()
    max_lines = int(term_rect.height // line_height) - 1
    for i, line in enumerate(output_lines[-max_lines:]):
        text_surf = font_small.render(line, True, WHITE)
        screen.blit(text_surf, (term_rect.x + 5, term_rect.y + 5 + i * line_height))

    # Bottom input box
    bottom_bar_rect = pygame.Rect(
        window_width * 0.07 * width_scale_factor,
        window_height * 0.68 * height_scale_factor,
        window_width * 0.4 * width_scale_factor,
        window_height * 0.12 * height_scale_factor
    )
    pygame.draw.rect(screen, WHITE, bottom_bar_rect, border_radius=4)
    input_text = user_input if user_input else "Enter commands here "
    screen.blit(font_generic.render(input_text, True, BLACK), (bottom_bar_rect.x + 12, bottom_bar_rect.y + 16))

    # Help box
    command_box_rect = pygame.Rect(
        window_width * 0.52 * width_scale_factor,
        window_height * 0.68 * height_scale_factor,
        window_width * 0.4 * width_scale_factor,
        window_height * 0.12 * height_scale_factor
    )
    pygame.draw.rect(screen, WHITE, command_box_rect, border_radius=4)
    screen.blit(font_generic.render("Guide: ", True, BLACK), (command_box_rect.x + 12 * width_scale_factor, command_box_rect.y + 12 * height_scale_factor))     
    screen.blit(font_small.render("- Type commands in the left box - 'help' to display commands", True, BLACK), (command_box_rect.x + 12 * width_scale_factor, command_box_rect.y + 38 * height_scale_factor))
    screen.blit(font_small.render("- Click 'Graph Mode' to toggle graph display", True, BLACK), (command_box_rect.x + 12 * width_scale_factor, command_box_rect.y + 60 * height_scale_factor))

    # Command list
    command_list_rect = pygame.Rect(
        window_width * 0.07 * width_scale_factor,
        window_height * 0.84 * height_scale_factor,
        window_width * 0.4 * width_scale_factor,
        window_height * 0.15 * height_scale_factor
    )
    pygame.draw.rect(screen, WHITE, command_list_rect, border_radius=4)
    commands = [
        "Available Commands:",
        "water <ml> - Add water to increase moisture",
        "sunlight <lux> - Add artificial sunlight",
        "temperature <C> - Adjust temperature",
        "humidity <%> - Increase humidity",
        "help - Show this command list",
        "clear - Clear the console output",
        "quit - Exit the program"
    ]
    line_y = command_list_rect.y + 8 * height_scale_factor
    for i in commands:
        screen.blit(font_small.render(i, True, BLACK), (command_list_rect.x + 12 * width_scale_factor, line_y))
        line_y += 18 * height_scale_factor

def main_ui_run():
    global running, screen_height, screen_width, user_input, graph_mode
    plant_selected = False
    selected_plant = None
    simulation_speed = None

    while not plant_selected:
        selected_plant = simulator.user_choose_plant()
        if selected_plant == 'back':
            plant_selected = True
            selected_plant = None
        elif selected_plant:
            plant_selected = True
            simulator.selected_plant = selected_plant

    while simulation_speed is None:
        simulation_speed = simulator.speed_of_simulation()
        if simulation_speed is None:
            print("Please enter a valid simulation speed.")

    if selected_plant is None:
        running = False
        return

    # Initialize current plant data
    simulator.selected_plant.update(simulator.starting_plant_data)
    simulator.reset_health_score()
    simulator.last_history_log = 0

    running = True
    user_input = ""
    graph_mode = False

    pygame.init()

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    window_width = screen_width
    window_height = screen_height

    screen = pygame.display.set_mode(
        (window_width, int(window_height * 0.93)), pygame.RESIZABLE
    )
    pygame.display.set_caption("Main UI")

    clock = pygame.time.Clock()
    last_update = time.time()

    while running:
        clock.tick(60)
        width_scale_factor = screen.get_width() / screen_width
        height_scale_factor = screen.get_height() / screen_height

        # Update simulation data periodically
        current_time = time.time()
        if current_time - last_update > 0.5 / simulation_speed:
            simulator.time_counter += 0.1  # Slower time progression for realistic cycles
            simulator.water_change()
            simulator.humidity_change()
            simulator.temperature_change()
            simulator.sunlight_change()
            simulator.update_health_score()
            if current_time - simulator.last_history_log > 5:
                readings = simulator.current_readings()
                plant = simulator.selected_plant_object()
                if plant:
                    simulator.log_simulation_reading(
                        simulator.selected_plant.get("name", "Unknown plant"),
                        readings,
                        round(simulator.current_health_score, 1),
                        simulator.current_health_category()
                    )
                    log_output(
                        f"Reading saved: moisture {readings.get('moisture'):.1f}%, "
                        f"sunlight {readings.get('sunlight'):.1f} lux, "
                        f"health {simulator.current_health_score:.1f}/100"
                    )
                    simulator.last_history_log = current_time
            last_update = current_time

        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_input.strip():
                        log_output(f"> {user_input}")
                        cmd = user_input.lower()
                        if cmd == "help":
                            for command in commands:
                                log_output(command)
                        elif cmd == "clear":
                            clear_output()
                        elif cmd == "quit":
                            log_output("Exiting the program")
                            time.sleep(1)
                            running = False
                        elif cmd.startswith("water "):
                            try:
                                amount = float(cmd.split()[1])
                                if amount < 0:
                                    log_output("Water amount cannot be negative")
                                else:
                                    simulator.add_water_command(amount, log_output)
                                    log_output(f"Added {amount} ml of water")
                            except (IndexError, ValueError):
                                log_output("Usage: water <amount>")
                        elif cmd.startswith("sunlight "):
                            try:
                                amount = float(cmd.split()[1])
                                if amount < 0:
                                    log_output("Sunlight amount cannot be negative")
                                else:
                                    simulator.add_sunlight_command(amount, log_output)
                                    log_output(f"Added {amount} lux of sunlight")
                            except (IndexError, ValueError):
                                log_output("Usage: sunlight <amount>")
                        elif cmd.startswith("temperature "):
                            try:
                                amount = float(cmd.split()[1])
                                if amount < 0:
                                    log_output("Temperature amount cannot be negative")
                                else:
                                    simulator.add_temperature_command(amount, log_output)
                                    log_output(f"Adjusted temperature by {amount}°C")
                            except (IndexError, ValueError):
                                log_output("Usage: temperature <amount>")
                        elif cmd.startswith("humidity "):
                            try:
                                amount = float(cmd.split()[1])
                                if amount < 0:
                                    log_output("Humidity amount cannot be negative")
                                else:
                                    simulator.add_humidity_command(amount, log_output)
                                    log_output(f"Added {amount}% humidity")
                            except (IndexError, ValueError):
                                log_output("Usage: humidity <amount>")
                        else:
                            log_output("Unknown command")
                    user_input = ""
                elif event.unicode.isprintable():
                    user_input += event.unicode

            handle_graph_toggle(event, window_width, window_height, width_scale_factor, height_scale_factor)

        draw_graph_mode_ui(screen, window_width, window_height, width_scale_factor, height_scale_factor)

        pygame.display.flip()

    pygame.quit()