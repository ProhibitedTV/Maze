import pygame

def handle_input(event, camera):
    """
    Process keyboard or mouse events and update camera or other settings.

    Args:
    - event: The current event to process.
    - camera: The camera object to be manipulated based on user input.
    """
    if event.type == pygame.KEYDOWN:  # Check if a key is pressed down
        if event.key == pygame.K_w:  # Move camera forward
            camera.move_forward()
        elif event.key == pygame.K_s:  # Move camera backward
            camera.move_backward()
        elif event.key == pygame.K_a:  # Rotate camera left
            camera.rotate_left()
        elif event.key == pygame.K_d:  # Rotate camera right
            camera.rotate_right()