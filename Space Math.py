import sys
import pygame
import random

pygame.init()
BG = pygame.image.load("C:\\Users\\tuqam\\space.jpeg")
space_ship = pygame.transform.scale(pygame.image.load("C:\\Users\\tuqam\\Space Ship (3).png"),
                                    (115, 65))  # Enemy image
shooter_image = pygame.image.load("C:\\Users\\tuqam\\shooter.png")  # Load the player image

# Scale up the player's ship (your ship)
shooter_image = pygame.transform.scale(shooter_image, (150, 150))  # Increased size

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
game_music = pygame.mixer.Sound("C:\\Users\\tuqam\\game music.mp3")
shooting_sound = pygame.mixer.Sound("C:\\Users\\tuqam\\shooting sound effect.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Counting Stars")
pygame.display.set_icon(BG)

font = pygame.font.Font(None, 45)
clock = pygame.time.Clock()

bullets = []
enemies = []
score = 0



class Player:
    def __init__(self, image, x, y, width, height, speed):
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


# Generate the player object
player = Player(shooter_image, WIDTH / 4, HEIGHT - 150, 150, 150, 5)


def generate_question():
    num1, num2 = random.randint(0, 9), random.randint(0, 9)
    answer = num1 * num2
    question = f"{num1} * {num2}"

    # Generate unique wrong answers
    answers = [answer]
    while len(answers) < 3:
        wrong_answer = random.randint(1, 100)  # Generate a random wrong answer
        if wrong_answer != answer and wrong_answer not in answers:
            answers.append(wrong_answer)

    random.shuffle(answers)  # Shuffle the answer options
    return question, answer, answers


# Generate the first question
question, answer, answers = generate_question()

# Generate enemies with answers
for i in range(3):
    enemies.append({'rect': pygame.Rect(100 + i * 150, 50, 100, 80), 'answer': answers[i]})

game_music.play(fade_ms=1000)
game_music.set_volume(0.6)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player.rect.centerx - 5
                bullet_y = player.rect.centery - 50
                bullets.append(pygame.Rect(bullet_x, bullet_y, 10, 20))
                shooting_sound.set_volume(2)
                shooting_sound.play()
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    keys = pygame.key.get_pressed()
    player.move(keys)

    for bullet in bullets:
        bullet.y -= 5
        if bullet.y < 0:
            bullets.remove(bullet)

    hit_correct_enemy = False
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy['rect']):
                if enemy['answer'] == answer:
                    score += 1
                    hit_correct_enemy = True
                bullets.remove(bullet)
                enemies.remove(enemy)
                break
        if hit_correct_enemy:# generating a new question
            question, answer, answers = generate_question()
            enemies.clear()
            for i in range(3):
                enemies.append({'rect': pygame.Rect(100 + i * 150, 50, 100, 80), 'answer': answers[i]})
            break

    screen.blit(BG, (0, 0))
    player.draw(screen)
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

    for enemy in enemies:
        screen.blit(space_ship, enemy['rect'].topleft)
        text = font.render(str(enemy['answer']), True, (255, 255, 255))
        text_rect = text.get_rect(center=(enemy['rect'].x + 60, enemy['rect'].y + 30))
        screen.blit(text, text_rect)

    text = font.render(question, True, (255, 255, 255))
    screen.blit(text, (player.rect.x + 40, player.rect.y + 20))
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if score >= 5:
        text = font.render("You Win!", True, (0, 255, 0))
        screen.blit(text, (WIDTH / 2 - 50, HEIGHT / 2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(60)