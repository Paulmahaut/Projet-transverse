import pygame
import time

# Initialiser Pygame et le mixer
pygame.init()
pygame.mixer.init()

# Charger les deux fichiers sonores
sound1_path = "tqt.mp3"
sound2_path = "Explosion sound.mp3"

try:
    sound1 = pygame.mixer.Sound("tqt.mp3")
    sound2 = pygame.mixer.Sound("Explosion sound.mp3")
    print("Les sons ont été chargés avec succès.")
except pygame.error as e:
    print(f"Erreur lors du chargement des sons: {e}")
    exit()

# Jouer les sons simultanément
sound1.play() 
sound2.play()

# Attendre que les sons se terminent
time.sleep(max(sound1.get_length(), sound2.get_length()))

pygame.quit()
