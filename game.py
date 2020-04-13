import random
from os import system, name
import time
from pynput import keyboard
import logging
import threading

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


emptySpace = "░"
playerChar = " "
obstacle = "O"
rowCount = 20
rowLength = 30
t = 0.5
k = 0.99
emptyRow = rowLength*emptySpace
rightKey = "d"
leftKey = "a"


def printRow(n,isPlayer):
    pic = obstacle
    if isPlayer:
        pic = playerChar
    if 0 <= n < rowLength:
        print(n * emptySpace + pic + (rowLength - n -1) * emptySpace)
    else:
        print(emptyRow)
    
def printPlayground(a):
    for item in a:
        printRow(item,False)

def regenerate(a):
    for i in range(rowCount-1,0, -1):
        a[i] = a[i-1]
    a[0] = random.randint(0,rowLength)

l = threading.Lock()

def redraw(a,player):
    global l    
    if not l.acquire(True):
        return    
    clear()    
    printPlayground(a)    
    printRow(player,True)  
    l.release()

rightPress = False
leftPress = False

def on_press(key): 
    global player, leftPress, rightPress,leftKey, rightKey, a   
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if k == leftKey and not leftPress:
        leftPress = True
        player = (player - 1) % rowLength
        redraw(a,player)
    if k == rightKey and not rightPress:
        rightPress = True
        player = (player + 1) % rowLength
        redraw(a,player)

def on_release(key):
    global leftPress, rightPress,leftKey, rightKey
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == leftKey:        
        leftPress = False
    if k == rightKey:
        rightPress = False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()  # start to listen on a separate thread

a = [-1]*rowCount
player = int(rowLength / 2)

while True:
    redraw(a,player)      
    if a[rowCount-1] == player:
        break
    time.sleep(t)
    regenerate(a)
    t = k*t
    



