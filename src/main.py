from colorama import Fore, Back, Style
import time
import sys
import termios
import tty
import signal
import os
horizontal=("-"*80).center(90)
vertical=(("|"+" "*80+"|").center(90)+"\n")*45
print(horizontal)
print(vertical,end="")
print(horizontal)
starty=6;prevx=starty
startx=3;prevy=starty
global village
global mapping
global k
global timetick
timetick=time.time()
#king=("_"*4),"{"+" K"+"}/",(" /\\")
village=[list(" "*80) for i in range(45)]
global walls
walls={}
global king_spawned
king_spawned=0

global barabarians
barabarians=[]
global symbol
symbol=0

class Buildings:
    def add(self,x,y,string):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            village[x+i][y:y+len(string[i])]=str(symbol)*len(string[i])
            print("\033["+str(posx)+";"+str(posy)+"H"+Back.GREEN+string[i],end="")
        
    def low_color(self,x,y,string):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            print("\033["+str(posx)+";"+str(posy)+"H"+Back.RED+string[i],end="")
    def mid_color(self,x,y,string):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            print("\033["+str(posx)+";"+str(posy)+"H"+Back.YELLOW+string[i],end="")
        
        
        

class Hut(Buildings):
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=2
        self.__height=2
        self.health=200
        self.destroyed=0
        self.orig=200
        self.__string=[(" /\\ "),"[ H]"]
        self.__clear=[("    "),"    "]
        Buildings.add(self,self.x,self.y,self.__string)
    
    def clear(self):
        string=self.__clear;x=self.x;y=self.y
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            village[x+i][y:y+len(string[i])]=str(" ")*len(string[i])
            print("\033["+str(posx)+";"+str(posy)+"H"+Style.RESET_ALL+string[i],end="")
        self.destroyed=1
    def low_color(self):
        Buildings.low_color(self,self.x,self.y,self.__string)
    
    def mid_color(self):
        Buildings.mid_color(self,self.x,self.y,self.__string)


class TownHall(Buildings):
    destroyed=0
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=6
        self.__height=5
        self.health=400
        self.destroyed=0
        self.orig=400
        self.__string=[("+"+"-"*4+"+"),("|"+"TOWN"+"|"),("|"+"HALL"+"|"),(("|"+" "*4+"|")*1),("+"+"-"*4+"+")]
        self.__clear=[(" "+" "*4+" "),(" "+"    "+" "),(" "+"    "+" "),((" "+" "*4+" ")*1),(" "+" "*4+" ")]
        Buildings.add(self,self.x,self.y,self.__string)
    
    def clear(self):
        string=self.__clear;x=self.x;y=self.y
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            village[x+i][y:y+len(string[i])]=str(" ")*len(string[i])
            print("\033["+str(posx)+";"+str(posy)+"H"+Style.RESET_ALL+string[i],end="")
        self.destroyed=1
    def low_color(self):
        Buildings.low_color(self,self.x,self.y,self.__string)
    
    def mid_color(self):
        Buildings.mid_color(self,self.x,self.y,self.__string)


class Cannon(Buildings):
    destroyed=0
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=3
        self.__height=1
        self.__string=["[<C>]"]
        self.health=200
        self.orig=200
        self.destroyed=0
        self.__clear=["     "]
        Buildings.add(self,self.x,self.y,self.__string)
    
    def clear(self):
        string=self.__clear;x=self.x;y=self.y
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            village[x+i][y:y+len(string[i])]=str(" ")*len(string[i])
            print("\033["+str(posx)+";"+str(posy)+"H"+Style.RESET_ALL+string[i],end="")
        self.destroyed=1
    def low_color(self):
        Buildings.low_color(self,self.x,self.y,self.__string)
    
    def mid_color(self):
        Buildings.mid_color(self,self.x,self.y,self.__string)

        
        

class Wall(Buildings):
   
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=1
        self.__height=1
        self.destroyed=0
        self.__string=["/"]
        self.health=120
        self.__clear=[" "]
        Buildings.add(self,self.x,self.y,self.__string)
    
    def clear(self):
        string=self.__clear;x=self.x;y=self.y
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            village[x+i][y:y+len(string[i])]=str(" ")*len(string[i])
            print("\033["+str(posx)+";"+str(posy)+"H"+Style.RESET_ALL+string[i],end="")
        self.destroyed=1
    
    def low_color(self):
        Buildings.low_color(self,self.x,self.y,self.__string)
    
    def mid_color(self):
        Buildings.mid_color(self,self.x,self.y,self.__string)

        
class Troops:
    def addtroop(self,x,y,string):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            print("\033["+str(posx)+";"+str(posy)+"H"+Back.BLUE+string[i],end="")
            print(Style.RESET_ALL,end="")
            
    def move(self,x,y,string,clear,ind_i,ind_j):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            print("\033["+str(posx)+";"+str(posy)+"H"+Style.RESET_ALL+clear[i],end="")
        x+=ind_i;y+=ind_j
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            
            print("\033["+str(posx)+";"+str(posy)+"H"+Back.BLUE+string[i],end="")
            print(Style.RESET_ALL,end="")
    
            
            
        
        
class Barbarian(Troops):
    def __init__(self,x,y):
        self.__health=30
        self.name="b"
        self.__damage=6
        self.__width=1
        self.__height=1
        self.__string=["B"]
        self.x=x
        self.y=y
        self.clear=[" "]
        Troops.addtroop(self,self.x,self.y,self.__string)
            
    def move(self,i,j):
        if(village[self.x+i][self.y+j]==" "):
            Troops.move(self,self.x,self.y,self.__string,self.clear,i,j)
            self.x+=i;self.y+=j
        else:
            self.attack(i,j)
    
    def attack(self,i,j):
        if(village[self.x+i][self.y+j]!="w"):
            building_index=mapping[village[self.x+i][self.y+j]]
            buildings[building_index].health-=self.__damage
        else:
            target=walls[str(self.x+i)+"_"+str(self.y+j)]
            target.health-=self.__damage
            target.destroyed=1
            if(target.health<=0):
                target.clear()
                
            
    
    def nearest(self):
        dis=float("inf")
        ind=0
        for i in range(len(buildings)):
            if(abs(buildings[i].x-self.x)+abs(buildings[i].y-self.y)<dis and buildings[i].destroyed==0):
                dis=abs(buildings[i].x-self.x)+abs(buildings[i].y-self.y)
                ind=i
        return ind
            
        
        
        
        
        
class King(Troops):
    def __init__(self,x,y):
        self.__health=100
        self.name="k"
        self.__damage=50
        self.__string=["K"]
        self.x=x
        self.movement=[0,1]
        self.y=y
        self.clear=[" "]
        Troops.addtroop(self,self.x,self.y,self.__string)
    
    def move(self,i,j):
        if(village[self.x+i][self.y+j]==" "):
            Troops.move(self,self.x,self.y,self.__string,self.clear,i,j)
            self.x+=i;self.y+=j
   
    
    def attack(self,i,j):
        if(village[self.x+i][self.y+j]!="w" and village[self.x+i][self.y+j]!=" "):
            building_index=mapping[village[self.x+i][self.y+j]]
            buildings[building_index].health-=self.__damage
            
        elif(village[self.x+i][self.y+j]=="w"):
            target=walls[str(self.x+i)+"_"+str(self.y+j)]
            target.health-=self.__damage
            target.destroyed=1
            if(target.health<=0):
                target.clear()
        
        
            
    
    
class Get:
    def __call__(self):
        global king_spawned
        global timetick
        global k
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
       
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            print("\r",end="")
            if(ch=="z"):
             
                b=Barbarian(position1[0],position1[1])
                barabarians.append(b)
            if(ch=="x"):
                
                b=Barbarian(position2[0],position2[1])
                barabarians.append(b)
            if(ch=="c"):
                b=Barbarian(position3[0],position3[1])
                barabarians.append(b)
            if(ch=="k" and king_spawned==0):
                k=King(2,5)
                king_spawned=1
                
            if(ch=="a" and king_spawned==1):
                k.move(0,-1)
                k.movement=[0,-1]
            if(ch=="w" and king_spawned==1):
                k.move(-1,0);k.movement=[-1,0]
            if(ch=="d" and king_spawned==1):
                k.move(0,1);k.movement=[0,1]
            if(ch=="s" and king_spawned==1):
                k.move(1,0);k.movement=[1,0]
            if(ch==" " and king_spawned==1):
                k.attack(k.movement[0],k.movement[1])                    
            if(ch=="e"):
                return 1
            timetick=time.time()
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
      


class AlarmException(Exception):
    pass


def alarmHandler(signum, frame):
    raise AlarmException


def input_to(callback,timeout=0.2):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text=callback()
        signal.alarm(0)
        return text
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return None




exit=0
mapping={"0":0,"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15}
th=TownHall(21,38);symbol="a"
h1=Hut(10,20);symbol="b"
h2=Hut(10,30);symbol="c"
h3=Hut(18,20);symbol="d"
h4=Hut(15,55);symbol="e"
h5=Hut(23,55);symbol="f"
h6=Hut(28,24);symbol="g"
h7=Hut(35,55);symbol="h"
h8=Hut(20,70);symbol="i"
h9=Hut(20,10);symbol="j"
cannon1=Cannon(18,30);symbol="k"
cannon2=Cannon(27,38);symbol="l"
cannon3=Cannon(10,55);symbol="m"
cannon4=Cannon(29,73);symbol="n"
cannon5=Cannon(38,10);symbol="o"
cannon6=Cannon(5,40)
global buildings
buildings=[th,h1,h2,h3,h4,h5,h6,h7,h8,h9,cannon1,cannon2,cannon3,cannon4,cannon5,cannon6]


thpos=(21,38)
symbol="w"
wall1_attrib=(20,15)
wall1_start=(thpos[0]+2,thpos[1]-wall1_attrib[0])
for i in range(wall1_attrib[0]):
    w=Wall(thpos[0]+2,thpos[1]-wall1_attrib[0]+i)
    walls.update({str(thpos[0]+2)+"_"+str(thpos[1]-wall1_attrib[0]+i):w})
for i in range(wall1_attrib[1]):
    w=Wall(wall1_start[0]-wall1_attrib[1]+i,wall1_start[1])
    walls.update({str(wall1_start[0]-wall1_attrib[1]+i)+"_"+str(wall1_start[1]):w})
for i  in range(wall1_attrib[0]+2):
    w=Wall(wall1_start[0]-wall1_attrib[1],wall1_start[1]+i)
    walls.update({str(wall1_start[0]-wall1_attrib[1])+"_"+str(wall1_start[1]+i):w})
for i in range(wall1_attrib[1]-2):
    w=Wall(wall1_start[0]-wall1_attrib[1]+i,wall1_start[1]+wall1_attrib[0]+2)
    walls.update({str(wall1_start[0]-wall1_attrib[1]+i)+"_"+str(wall1_start[1]+wall1_attrib[0]+2):w})


wall2_attrib=(20,15)
wall2="/"*wall2_attrib[0]
wall2_start=(thpos[0]-wall2_attrib[1]+3,thpos[1]+3)
for i in range(wall2_attrib[0]):
    w=Wall(wall2_start[0],wall2_start[1]+i)
    walls.update({str(wall2_start[0])+"_"+str(wall2_start[1]+i):w})
for i in range(wall2_attrib[1]+8):
    w=Wall(wall2_start[0]+i,wall2_start[1]+wall2_attrib[0])
    walls.update({str(wall2_start[0]+i)+"_"+str(wall2_start[1]+wall2_attrib[0]):w})
end =i    
for i in range(wall2_attrib[0]*2):
    w=Wall(wall2_start[0]+end,wall2_start[1]-wall2_attrib[0]+i)
    walls.update({str(wall2_start[0]+end)+"_"+str(wall2_start[1]-wall2_attrib[0]+i):w})
endwall=(thpos[0]+2,wall2_start[1]-wall2_attrib[0])
for i in range(wall2_start[0]+end-(thpos[0]+startx)+1):
    w=Wall(endwall[0]+i,endwall[1])
    walls.update({str(endwall[0]+i)+"_"+str(endwall[1]):w})




#-----------------------------------------------Main Code------------------------------------
def getinput():
    a=Get()
    ans=a.__call__()
    return ans
position1=(2,35)
position2=(45,20)
position3=(40,70)

def animate():
    for i in range(len(buildings)):
        if(buildings[i].health<(70/100)*buildings[i].orig and buildings[i].destroyed==0):
            buildings[i].mid_color()
        if(buildings[i].health<=(30/100)*buildings[i].orig and buildings[i].destroyed==0):
            buildings[i].low_color()
        if(buildings[i].health<=0 and buildings[i].destroyed==0):
            buildings[i].clear()
    for i in range(len(barabarians)):
        result=barabarians[i].nearest()
        locx=buildings[result].x;locy=buildings[result].y
        dirx=(locx-barabarians[i].x);diry=(locy-barabarians[i].y)
        movex=0 if(dirx==0) else (locx-barabarians[i].x)/abs(locx-barabarians[i].x)
        movey=0 if(diry==0) else (locy-barabarians[i].y)/abs(locy-barabarians[i].y)
        barabarians[i].move(int(movex),int(movey))

        
    
        
while(1):
    os.system("stty -echo")
    ans=input_to(getinput)
    if(ans==1):
        os.system("stty echo")
        break
    animate()
    print("",end="")
    print("\r",end="")
    time.sleep(0.2)
    

    
    

    

