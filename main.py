import pygame


width, height = 700, 700
# def draw(screen):
#    screen.fill((0, 0, 0))
#    pygame.draw.line(screen, (255, 255, 255), (0, 0), (w, h), 5)
#    pygame.draw.line(screen, (255, 255, 255), (w, 0), (0, h), 5)


if __name__ == '__main__':
    try:
        pygame.init()
        pygame.display.set_caption('Dark Lifes')
        size = width, height
        screen = pygame.display.set_mode(size)
        screen.fill('white')
        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass
        pygame.quit()
    except ValueError:
        print('Неправильный формат ввода')