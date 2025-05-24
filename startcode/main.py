import pygame
import time
from snake import Snake
from food import Food
import csv
from datetime import datetime
# kleuren
kleur_achtergrond = (0, 0, 0)
kleur_tekst = (255, 0, 0)

# schermgrootte
breedte = 800
hoogte = 600
veld_grootte = 20

# Snelheid van het spel
spel_snelheid = 5

# Initialiseren van de pygame-module
pygame.init()

# Creëer een venster met opgegeven breedte en hoogte
venster = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption('Snake')

def haal_hoogste_score_op():
    try:
        with open('highscore.csv', mode='r') as file:
            reader = csv.reader(file)
            highscores = list(reader)
            highscore = max(int(row[0]) for row in highscores)
            return highscore
    except FileNotFoundError:
        return 0


def sla_op_in_csv(score, tijdstip):
    with open("highscore.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([score, tijdstip])


# Functie om de score op het scherm te tonen
def toon_score(score, venster):
    font = pygame.font.Font(None, 36)
    scoretekst = font.render(f"Score: {score}", True, kleur_tekst)
    venster.blit(scoretekst, (10, 10))



# Start de hoofdloop van het spel
def game_lus():
    food = Food(breedte, hoogte)
    snake = Snake(breedte//2, hoogte//2)
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.x_verandering == 0:
                    snake.x_verandering = -veld_grootte
                    snake.y_verandering = 0
                elif event.key == pygame.K_RIGHT and snake.x_verandering == 0:
                    snake.x_verandering = veld_grootte
                    snake.y_verandering = 0
                elif event.key == pygame.K_UP and snake.y_verandering == 0:
                    snake.y_verandering = -veld_grootte
                    snake.x_verandering = 0
                elif event.key == pygame.K_DOWN and snake.y_verandering == 0:
                    snake.y_verandering = veld_grootte
                    snake.x_verandering = 0
                elif event.key == pygame.K_p:
                    gepauzeerd = True
                    pauze_font = pygame.font.Font(None, 36)
                    pauze_tekst = pauze_font.render("Pauze (Druk op P om door te gaan)", True, kleur_tekst)

                    venster.blit(pauze_tekst,(breedte // 2 - pauze_tekst.get_width() // 2, hoogte // 2))
                    while gepauzeerd:
                        for pauze_event in pygame.event.get():
                            if pauze_event.type == pygame.KEYDOWN and pauze_event.key == pygame.K_p:
                                gepauzeerd = False






        snake.beweeg()
        if snake.is_buiten_veld(breedte, hoogte) or snake.raakt_zichzelf():
            game_over = True

        venster.fill(kleur_achtergrond)  # Vul het scherm met een zwarte achtergrond
        food.teken(venster)
        snake.teken(venster)
        toon_score(score, venster)

        if snake.x == food.x and snake.y == food.y:
            food.plaats_voedsel()
            snake.lengte_slang += 1
            score += 10

        pygame.display.update()
        time.sleep(1 / spel_snelheid)
    print(f"Jouw score is {score}")
    sla_op_in_csv(score, datetime.now())
    highscores = haal_hoogste_score_op()
    print(f"De hoogste score is {highscores}")

# Start de hoofdloop van het spel
game_lus()
