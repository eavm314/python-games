import sys
import pygame

ANCHO = 640
ALTO = 480

class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar la imagen
        self.image = pygame.image.load('./assets/player.png')
        # Rectangulo de la imagen
        self.rect = self.image.get_rect()
        # Posicion inicial centrada
        self.rect.centerx = ANCHO/2
        self.rect.centery = ALTO/2
# Inicializar pantalla
pantalla = pygame.display.set_mode((ANCHO,ALTO))
# Título
pygame.display.set_caption("Juego de ladrillos")

# Creamos la bolita
bolita = Bolita()

while(True):
    # Revisar eventos para cerrar programa
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

    # Mostrar bolita
    pantalla.blit(bolita.image, bolita.rect)

    # Actualizar los elementos de la pantalla
    pygame.display.flip()