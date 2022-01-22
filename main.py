# Pong
import pygame
import tkinter as tk

pygame.init()
Width, Height = 800, 450
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pong")


class Player:
    def __init__(self, letters_pressed, pong1):
        self.speed = 5
        self.white = 255, 255, 255
        self.grey = 32, 32, 32
        self.letters = letters_pressed
        self.pong1 = pong1

    def key_player(self):
        if self.letters[pygame.K_w] and self.pong1.y > 0:
            self.pong1.y -= self.speed
        if self.letters[pygame.K_s] and self.pong1.y + self.pong1.height < Height:
            self.pong1.y += self.speed

    def draw(self):
        pygame.draw.rect(Screen, self.grey, (0, 0, Width, Height))  # Background
        pygame.draw.rect(Screen, self.white, (self.pong1.x, self.pong1.y, 5, 60))
        pygame.draw.rect(Screen, self.white, ((Width // 2), 0, 3, Height))  # Divider


class MoveOpp:
    def __init__(self, pong2, ball):
        self.speed = 3.99
        self.pong2 = pong2
        self.ball = ball
        self.white = 255, 255, 255

    def move_p2(self):
        if self.pong2.top < self.ball.y:
            self.pong2.y += self.speed
        elif self.pong2.bottom > self.ball.y:
            self.pong2.y -= self.speed

        if self.pong2.y > 0:
            self.pong2.y -= self.speed
        if self.pong2.y + self.pong2.height < Height:
            self.pong2.y += self.speed

    def draw(self):
        pygame.draw.rect(Screen, self.white, (self.pong2.x, self.pong2.y, 5, 60))


class BallCollide:
    def __init__(self, ball, pong1, pong2):
        self.ball = ball
        self.pong1 = pong1
        self.pong2 = pong2
        self.speedX = 5
        self.speedY = 4
        self.white = (255, 255, 255)

    def ballCollide(self):
        self.ball.x += self.speedX
        self.ball.y += self.speedY

        if self.ball.top <= 0 or self.ball.bottom >= Height:
            self.speedY *= -1
        if self.ball.left <= 0 or self.ball.right >= Width:
            self.speedX *= -1
        if self.ball.colliderect(self.pong1):
            self.speedX *= -1
        if self.ball.colliderect(self.pong2):
            self.speedX *= -1

    def displayBall(self):
        pygame.draw.ellipse(Screen, self.white, self.ball)


def displayScore(counter1, counter2):
    white = 255, 255, 255
    font = pygame.font.SysFont("comicsans", 12)
    score1 = font.render("Player's' Points: " + str(counter1), 1, white)
    score2 = font.render("Computer's Points: " + str(counter2), 1, white)

    Screen.blit(score1, (0, 0))
    Screen.blit(score2, ((Width - score2.get_width()), 0))


def highScoregui(letters, counter1):
    if letters[pygame.K_q]:
        HEIGHT, WIDTH = 100, 400
        root = tk.Tk()
        root.title("High Score Entry")

        canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="#80c1ff")
        canvas.pack()

        name = tk.Entry(canvas, font=("Courier", 10))
        name.place(relx=0.4, rely=0.35, relwidth=0.5, relheight=0.2)

        detail = tk.Label(canvas, font=("Courier", 10), text="Enter your name:", bg="#80c1ff")
        detail.place(relx=0.05, rely=0.25, relwidth=0.35, relheight=0.4)

        button = tk.Button(canvas, text="Go", command=lambda: highScore(counter1, name.get()))
        button.place(relx=0.4, rely=0.7, relwidth=0.2, relheight=0.2)
        root.mainloop()


def highScore(counter1, name):
    high_scores = {}

    with open("score.txt", 'a') as f:
        f.write(name + " " + str(counter1) + "\n")

    with open("score.txt") as f:
        for line in f:
            key, value = line.split()
            high_scores[key] = int(value)

    highScores = sorted(high_scores.items(), key=lambda x: x[1], reverse=True)
    highscore_display(highScores)


def highscore_display(highscores):
    HEIGHT, WIDTH = 400, 500
    leaderboard = ""

    root = tk.Tk()
    root.title("High Score in Pong!")

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="Black")
    canvas.pack()

    title = tk.Label(canvas, font=("Times New Roman", 22), text="High Scores:", bg="Black", fg="White")
    title.place(relx=0.25, relwidth=0.5, rely=0.02)

    button = tk.Button(canvas, text="Ok", command=lambda: quit(), bg='White')
    button.place(relx=0.35, rely=0.9, relwidth=0.25, relheight=0.07)

    highscore_data = tk.Label(canvas, font=("Times New Roman", 15), bg="White")

    highscores = highscores[:5]

    for name, score in highscores:
        leaderboard += f"{name}:   {str(score)} \n \n"

    highscore_data['text'] = leaderboard
    highscore_data.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.7)

    root.mainloop()


def main():
    run = True
    clock = pygame.time.Clock()
    pong1 = pygame.Rect((10, 200, 5, 60))
    pong2 = pygame.Rect((790, 200, 5, 60))
    ball = pygame.Rect(Width / 2, Height / 2, 13, 13)
    collide = BallCollide(ball, pong1, pong2)
    counter1 = 0
    counter2 = 0

    while run:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if ball.left <= 0:
            counter2 += 1
            ball.x, ball.y = 400, 225
            pygame.time.wait(1500)
        elif ball.right >= Width:
            counter1 += 1
            ball.x, ball.y = 400, 225
            pygame.time.wait(1500)

        letters_pressed = pygame.key.get_pressed()
        highScoregui(letters_pressed, counter1)

        move = Player(letters_pressed, pong1)
        move.key_player()
        move.draw()

        collide.displayBall()
        collide.ballCollide()

        opp = MoveOpp(pong2, ball)
        opp.move_p2()
        opp.draw()

        displayScore(counter1, counter2)
        pygame.display.flip()

    pygame.quit()


main()