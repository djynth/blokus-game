class Gui:
    def __init__(self):
        # Try to allow playing even if you don't have pygame installed, by
        # doing this late import
        import pygame

        pygame.init()
        size = width, height = 320, 240
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 0))

    def update(self):
        import pygame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()

