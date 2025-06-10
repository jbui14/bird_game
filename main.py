import pygame
import sys
from settings import *
from bird import Bird
from pipe import Pipe
from coin import Coin

def load_high_score():
    try:
        with open("hiscore.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def save_high_score(new_high_score):
    with open("hiscore.txt", "w") as f:
        f.write(str(new_high_score))

def draw_text_with_outline(screen, font, text, color, y):
    outline_color = (0, 0, 0)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, y))
    for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, -2), (-2, 0), (2, 0), (0, 2)]:
        screen.blit(font.render(text, True, outline_color), (text_rect.x + dx, text_rect.y + dy))
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bird Flapper")
    
    bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    pipes = []
    coin = Coin()
    clock = pygame.time.Clock()
    game_active = False
    first_start = True
    score = 0
    high_score = load_high_score()
    font = pygame.font.Font(None, 74)
    
    background = pygame.image.load("background.png").convert()
    flap_sound = pygame.mixer.Sound("flap.wav")
    score_sound = pygame.mixer.Sound("score.wav")
    collision_sound = pygame.mixer.Sound("collision.wav")
    coin_sound = pygame.mixer.Sound("coin.wav")
    
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 2200)
    
    while True:
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_active:
                        game_active = True
                        bird.rect.centery = SCREEN_HEIGHT // 2
                        bird.movement = 0
                        pipes.clear()
                        score = 0
                        coin.reset()
                        pygame.time.set_timer(SPAWNPIPE, 2200)
                    else:
                        bird.flap()
                        flap_sound.play()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_active and event.type == SPAWNPIPE:
                pipes.append(Pipe())

        if not game_active:
            bird.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
            bird.movement = 0
            bird.tilt = 0
            bird.draw(screen)
            if first_start:
                draw_text_with_outline(screen, font, "Welcome to Bird Flapper", (255, 255, 255), SCREEN_HEIGHT // 2 - 100)
                draw_text_with_outline(screen, font, "Press Space to Start!", (255, 255, 255), SCREEN_HEIGHT // 2)
            else:
                draw_text_with_outline(screen, font, "Game Over", (255, 255, 255), SCREEN_HEIGHT // 2 - 100)
                draw_text_with_outline(screen, font, "Press Space to Play Again", (255, 255, 255), SCREEN_HEIGHT // 2)
            draw_text_with_outline(screen, font, f"High Score: {high_score}", (255, 255, 255), SCREEN_HEIGHT // 2 + 100)
        else:
            bird.update(GRAVITY)
            bird.draw(screen)

            for pipe in pipes[:]:
                pipe.update()
                pipe.draw(screen)
                if pipe.collide(bird.rect) or bird.rect.bottom >= SCREEN_HEIGHT:
                    game_active = False
                    collision_sound.play()
                    first_start = False
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                if not pipe.passed and (pipe.top_rect.right < bird.rect.left or pipe.bottom_rect.right < bird.rect.left):
                    pipe.passed = True
                    score += 1
                    score_sound.play()

            pipes = [pipe for pipe in pipes if pipe.top_rect.right > 0 or pipe.bottom_rect.right > 0]
            
            coin.update()
            coin.draw(screen)
            if bird.rect.colliderect(coin.rect):
                score += 2
                coin_sound.play()
                coin.reset()

            draw_text_with_outline(screen, font, f'Score: {score}', (255, 255, 255), 20)

        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    main()
