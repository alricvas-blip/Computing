"""
Pong Game - A fully functional implementation using pygame
Author: Expert Python Software Engineer
"""

import pygame
import math
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Game settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7
PADDLE_MARGIN = 30

BALL_SIZE = 15
BALL_INITIAL_SPEED = 5
BALL_SPEED_INCREMENT = 0.5
HITS_FOR_SPEED_INCREASE = 5
MAX_BOUNCE_ANGLE = 60  # degrees

WINNING_SCORE = 5


class Paddle:
    """Represents a player's paddle."""

    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        """Move paddle up, clamping to screen bounds."""
        self.rect.y = max(0, self.rect.y - self.speed)

    def move_down(self):
        """Move paddle down, clamping to screen bounds."""
        self.rect.y = min(SCREEN_HEIGHT - self.rect.height, self.rect.y + self.speed)

    def draw(self, surface: pygame.Surface):
        """Draw the paddle on the given surface."""
        pygame.draw.rect(surface, WHITE, self.rect)

    def reset(self, x: int, y: int):
        """Reset paddle to initial position."""
        self.rect.x = x
        self.rect.y = y


class Ball:
    """Represents the game ball with physics."""

    def __init__(self):
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = BALL_INITIAL_SPEED
        self.hit_count = 0
        self.reset()

    def reset(self, direction: int = 1):
        """
        Reset ball to center with initial velocity.
        direction: 1 for right, -1 for left
        """
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = BALL_INITIAL_SPEED
        self.hit_count = 0

        # Start with a slight angle (between -30 and 30 degrees)
        angle = 0  # Start straight for fairness
        self.velocity_x = self.speed * direction
        self.velocity_y = 0

    def update(self):
        """Update ball position based on velocity."""
        self.rect.x += round(self.velocity_x)
        self.rect.y += round(self.velocity_y)

    def handle_wall_collision(self):
        """Handle collision with top and bottom walls."""
        if self.rect.top <= 0:
            self.rect.top = 0  # Clamp to prevent sticking
            self.velocity_y = abs(self.velocity_y)  # Ensure moving down
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT  # Clamp to prevent sticking
            self.velocity_y = -abs(self.velocity_y)  # Ensure moving up

    def handle_paddle_collision(self, paddle: Paddle, is_left_paddle: bool):
        """
        Handle collision with a paddle using velocity bounce mechanic.
        Returns True if collision occurred.
        """
        if not self.rect.colliderect(paddle.rect):
            return False

        # Check if ball is moving toward the paddle
        if is_left_paddle and self.velocity_x > 0:
            return False  # Ball moving away from left paddle
        if not is_left_paddle and self.velocity_x < 0:
            return False  # Ball moving away from right paddle

        # Calculate relative hit position (-1 to 1)
        # -1 = top of paddle, 0 = center, 1 = bottom
        paddle_center_y = paddle.rect.centery
        relative_hit = (self.rect.centery - paddle_center_y) / (paddle.rect.height / 2)
        relative_hit = max(-1, min(1, relative_hit))  # Clamp to [-1, 1]

        # Calculate bounce angle based on hit position
        bounce_angle = relative_hit * MAX_BOUNCE_ANGLE
        angle_rad = math.radians(bounce_angle)

        # Determine direction (left paddle sends right, right paddle sends left)
        direction = 1 if is_left_paddle else -1

        # Set new velocity based on angle
        self.velocity_x = self.speed * math.cos(angle_rad) * direction
        self.velocity_y = self.speed * math.sin(angle_rad)

        # Reposition ball outside paddle to prevent sticking
        if is_left_paddle:
            self.rect.left = paddle.rect.right + 1
        else:
            self.rect.right = paddle.rect.left - 1

        # Increment hit count and potentially increase speed
        self.hit_count += 1
        if self.hit_count % HITS_FOR_SPEED_INCREASE == 0:
            self.speed += BALL_SPEED_INCREMENT
            # Update velocity magnitude while preserving direction
            current_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if current_speed > 0:
                scale = self.speed / current_speed
                self.velocity_x *= scale
                self.velocity_y *= scale

        return True

    def check_scoring(self) -> int:
        """
        Check if ball has passed a paddle (scoring).
        Returns: 1 if right scores, -1 if left scores, 0 if no score.
        """
        if self.rect.right < 0:
            return 1  # Right player scores
        elif self.rect.left > SCREEN_WIDTH:
            return -1  # Left player scores
        return 0

    def draw(self, surface: pygame.Surface):
        """Draw the ball on the given surface."""
        pygame.draw.rect(surface, WHITE, self.rect)


class GameManager:
    """Manages game state, rendering, and main loop."""

    # Game states
    STATE_START = 0
    STATE_PLAYING = 1
    STATE_GAME_OVER = 2

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        # Create game objects
        self.left_paddle = Paddle(
            PADDLE_MARGIN,
            SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        )
        self.right_paddle = Paddle(
            SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
            SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        )
        self.ball = Ball()

        # Game state
        self.state = self.STATE_START
        self.left_score = 0
        self.right_score = 0
        self.winner = None

        self.running = True

    def handle_input(self):
        """Handle all input events and continuous key presses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.state == self.STATE_START:
                        self.state = self.STATE_PLAYING
                    elif self.state == self.STATE_GAME_OVER:
                        self.reset_game()
                        self.state = self.STATE_START

        # Continuous key handling for smooth paddle movement
        if self.state == self.STATE_PLAYING:
            keys = pygame.key.get_pressed()

            # Left paddle controls (W/S)
            if keys[pygame.K_w]:
                self.left_paddle.move_up()
            if keys[pygame.K_s]:
                self.left_paddle.move_down()

            # Right paddle controls (Arrow keys)
            if keys[pygame.K_UP]:
                self.right_paddle.move_up()
            if keys[pygame.K_DOWN]:
                self.right_paddle.move_down()

    def update(self):
        """Update game logic."""
        if self.state != self.STATE_PLAYING:
            return

        # Update ball
        self.ball.update()

        # Handle wall collisions
        self.ball.handle_wall_collision()

        # Handle paddle collisions
        self.ball.handle_paddle_collision(self.left_paddle, is_left_paddle=True)
        self.ball.handle_paddle_collision(self.right_paddle, is_left_paddle=False)

        # Check for scoring
        score_result = self.ball.check_scoring()
        if score_result == 1:
            self.right_score += 1
            self.ball.reset(direction=-1)  # Ball goes toward left
        elif score_result == -1:
            self.left_score += 1
            self.ball.reset(direction=1)  # Ball goes toward right

        # Check for game over
        if self.left_score >= WINNING_SCORE:
            self.winner = "Left Player"
            self.state = self.STATE_GAME_OVER
        elif self.right_score >= WINNING_SCORE:
            self.winner = "Right Player"
            self.state = self.STATE_GAME_OVER

    def draw(self):
        """Render the game."""
        self.screen.fill(BLACK)

        if self.state == self.STATE_START:
            self.draw_start_screen()
        elif self.state == self.STATE_PLAYING:
            self.draw_game()
        elif self.state == self.STATE_GAME_OVER:
            self.draw_game()
            self.draw_game_over()

        pygame.display.flip()

    def draw_start_screen(self):
        """Draw the start screen."""
        # Title
        title = self.font_large.render("PONG", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)

        # Instructions
        start_text = self.font_medium.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)

        # Controls
        controls1 = self.font_small.render("Left Player: W/S", True, GRAY)
        controls1_rect = controls1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(controls1, controls1_rect)

        controls2 = self.font_small.render("Right Player: UP/DOWN Arrows", True, GRAY)
        controls2_rect = controls2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3 + 40))
        self.screen.blit(controls2, controls2_rect)

        # Winning score info
        win_text = self.font_small.render(f"First to {WINNING_SCORE} wins!", True, GRAY)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3 + 100))
        self.screen.blit(win_text, win_rect)

    def draw_game(self):
        """Draw the main game elements."""
        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 30):
            pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH // 2 - 2, y, 4, 15))

        # Draw scores
        left_score_text = self.font_large.render(str(self.left_score), True, WHITE)
        left_score_rect = left_score_text.get_rect(center=(SCREEN_WIDTH // 4, 50))
        self.screen.blit(left_score_text, left_score_rect)

        right_score_text = self.font_large.render(str(self.right_score), True, WHITE)
        right_score_rect = right_score_text.get_rect(center=(3 * SCREEN_WIDTH // 4, 50))
        self.screen.blit(right_score_text, right_score_rect)

        # Draw paddles and ball
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # Draw hit count and current speed (for debugging/info)
        info_text = self.font_small.render(
            f"Hits: {self.ball.hit_count} | Speed: {self.ball.speed:.1f}",
            True, GRAY
        )
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(info_text, info_rect)

    def draw_game_over(self):
        """Draw the game over overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)

        # Winner announcement
        winner_text = self.font_medium.render(f"{self.winner} Wins!", True, WHITE)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(winner_text, winner_rect)

        # Restart instruction
        restart_text = self.font_small.render("Press SPACE to Play Again", True, GRAY)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(restart_text, restart_rect)

    def reset_game(self):
        """Reset the game to initial state."""
        self.left_score = 0
        self.right_score = 0
        self.winner = None

        # Reset paddles
        self.left_paddle.reset(
            PADDLE_MARGIN,
            SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        )
        self.right_paddle.reset(
            SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
            SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        )

        # Reset ball
        self.ball.reset()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    game = GameManager()
    game.run()


if __name__ == "__main__":
    main()
