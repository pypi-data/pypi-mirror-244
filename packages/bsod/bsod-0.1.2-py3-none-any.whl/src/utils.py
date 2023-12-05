import sys
import pygame
import keyboard
import pkg_resources

def path_convertor(path):
    return pkg_resources.resource_filename('bsod', path)

def blocK_keyboard():
    for i in range(150):
        keyboard.block_key(i)

def play_audio(path):
    cassete_path = pkg_resources.resource_filename('bsod', path)

    try:
        pygame.init()
        pygame.mixer.music.load(cassete_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        
def show_error():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    image_path = path_convertor('assets/image.png')
    image = pygame.image.load(image_path)
    image_rect = image.get_rect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0, 0, 0))
        screen.blit(image, image_rect)

        pygame.display.update()

    pygame.quit()
    sys.exit()