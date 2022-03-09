from colorama import Fore, Back, Style
import time
import sys
import termios
import tty
import signal

horizontal=("-"*80).center(90)
vertical=(("|"+" "*80+"|").center(90)+"\n")*45
print(horizontal)
print(vertical,end="")
print(horizontal)
starty=6;prevx=starty
startx=3;prevy=starty

barbarian=("["+"B"+"]/\n")
barbarian_bottom=("/\\")
barbarian_clear=(" "+" "+"  \n")
barbarian_clear_bottom=("  ")

king=("_"*4)+"\n"
king_mid=("{"+" K"+"}/")+"\n"
king_bottom=(" /\\")
king_clear=(" "*4)+"\n"
king_mid_clear=(" "+"  "+"  ")+"\n"
king_bottom_clear=("  ")

class Buildings:
    def add(self,x,y,string):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            print("\033["+str(posx)+";"+str(posy)+"H"+string[i],end="")

class Hut(Buildings):
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=2
        self.__height=2
        self.__string=[(" /\\ "),"[ H]"]
        Buildings.add(self,self.x,self.y,self.__string)


class TownHall(Buildings):
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=4
        self.__height=3
        self.__string=[("+"+"-"*4+"+"),("|"+"TOWN"+"|"),("|"+"HALL"+"|"),(("|"+" "*4+"|")*1),("+"+"-"*4+"+")]
        Buildings.add(self,self.x,self.y,self.__string)

class Cannon(Buildings):
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=3
        self.__height=1
        self.__string=["[<C>]"]
        Buildings.add(self,self.x,self.y,self.__string)

class Wall(Buildings):
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=3
        self.__height=1
        self.__string=["/"]
        Buildings.add(self,self.x,self.y,self.__string)



th=TownHall(21,38)
h1=Hut(10,20)
h2=Hut(10,30)
h3=Hut(18,20)
h4=Hut(15,55)
h5=Hut(23,55)
h6=Hut(28,24)
cannon1=Cannon(18,30)
cannon2=Cannon(27,38)
cannon3=Cannon=(10,55)

thpos=(21,38)
wall1_attrib=(20,15)
wall1_start=(thpos[0]+2,thpos[1]-wall1_attrib[0])
for i in range(wall1_attrib[0]):
    Wall(thpos[0]+2,thpos[1]-wall1_attrib[0]+i)
for i in range(wall1_attrib[1]):
    Wall(wall1_start[0]-wall1_attrib[1]+i,wall1_start[1])
for i  in range(wall1_attrib[0]+2):
    Wall(wall1_start[0]-wall1_attrib[1],wall1_start[1]+i)
for i in range(wall1_attrib[1]-2):
    Wall(wall1_start[0]-wall1_attrib[1]+i,wall1_start[1]+wall1_attrib[0]+2)


wall2_attrib=(20,15)
wall2="/"*wall2_attrib[0]
wall2_start=(thpos[0]-wall2_attrib[1]+3,thpos[1]+3)
for i in range(wall2_attrib[0]):
    Wall(wall2_start[0],wall2_start[1]+i)
for i in range(wall2_attrib[1]+8):
    Wall(wall2_start[0]+i,wall2_start[1]+wall2_attrib[0])
end =i    
for i in range(wall2_attrib[0]*2):
    Wall(wall2_start[0]+end,wall2_start[1]-wall2_attrib[0]+i)
endwall=(thpos[0]+2,wall2_start[1]-wall2_attrib[0])
for i in range(wall2_start[0]+end-(thpos[0]+startx)+1):
    Wall(endwall[0]+i,endwall[1])




class Get:
    """Class to get input."""

    def __call__(self):
        """Defining __call__."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class AlarmException(Exception):
    """Handling alarm exception."""
    pass


def alarmHandler(signum, frame):
    """Handling timeouts."""
    raise AlarmException


def input_to(getch, timeout=0.1):
    """Taking input from user."""
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return None


