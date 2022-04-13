from colorama import Fore, Back, Style
import time
import sys
import termios
import tty
import signal
import os
total=open("./src/total.txt","r+")
totalreplays=0
for i in total.readlines():
    totalreplays=int(i)
global char_inp
f=open("./replays/replay{}.txt".format(totalreplays+1),"w+")   
valid=False
while(not(valid)):
    char_inp=input("Which Character do you want to choose : q for queen / k for king \n")
    if(char_inp!="k" and char_inp!="q"):
        print("Invalid Response\n")
        valid=False
    else:
        valid=True

print("\033["+str(1)+";"+str(0)+"H"+"")  
horizontal=("-"*80).center(90)
vertical=(("|"+" "*80+"|").center(90)+"\n")*45
print(horizontal)
print(vertical,end="")
print(horizontal)
starty=6;prevx=starty
startx=3;prevy=starty
if(char_inp=="k"):
    print("Kings health")
else:
    print("Queens health")
    
print(250)
print("\033["+str(startx+48)+";"+str(0)+"H"+Back.GREEN+"|"*50,end="")
print(Style.RESET_ALL,end="")
global capture,starttick
capture=[]
global village,mapping,k,timetick,rage_spell,heal_spell,healtime,heal,timeout,rage,ragetime,walls,king_spawned,active_spell,barabarians,symbol,archers,ballons
rage=0
heal=0
ballons=[]
timeout=0.1
timetick=time.time()
#king=("_"*4),"{"+" K"+"}/",(" /\\")
village=[list(" "*80) for i in range(45)]
walls={}
king_spawned=0
active_spell=[]
barabarians=[]
symbol=0
archers=[]

class Buildings:
    def add(self,x,y,string,vil=0):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            if(vil==0):
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
    
    def get_string(self):
        return self.__string


class TownHall(Buildings):
    destroyed=0
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=6
        self.__height=5
        self.health=500
        self.destroyed=0
        self.orig=500
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
    
    def get_string(self):
        return self.__string


class Cannon(Buildings):
    destroyed=0
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=3
        self.range=10
        self.__height=1
        self.__string=["[<C>]"]
        self.health=350
        self.orig=350
        self.destroyed=0
        self.damage=5
        self.__clear=["     "]
        self.__lastshot=0
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
    
    
    def get_string(self):
        return self.__string
    
    def attack(self):
        global barabarians,k,king_spawned
        flag=0;flag1=0
        if(time.time()-self.__lastshot>0.2):
            for i in range(len(barabarians)):
                if(abs(barabarians[i].x-self.x)+abs(barabarians[i].y-self.y)<=10 and barabarians[i].dead==0):
                    barabarians[i].health-=self.damage
                    flag=1
                    break
            if(flag==0 and king_spawned==1):
                if(abs(k.x-self.x)+abs(k.y-self.y)<=10 and k.destroyed==0):
                    k.health-=self.damage
                    flag1=1
                    k.update_health()
            if(flag==0 and flag1==0):
                for i in range(len(archers)):
                    if(abs(archers[i].x-self.x)+abs(archers[i].y-self.y)<=10 and archers[i].dead==0):
                        archers[i].health-=self.damage
                        flag=1
                        break
            
                    
            self.__lastshot=time.time()
            
class Wizard(Buildings):
    destroyed=0
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=3
        self.range=10
        self.__height=1
        self.__string=["[<W>]"]
        self.health=350
        self.orig=350
        self.destroyed=0
        self.damage=5
        self.__clear=["     "]
        self.__lastshot=0
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
    
    
    def get_string(self):
        return self.__string
    
    def attack(self):
        global barabarians,k,king_spawned
        flag=0;flag1=0;flag2=0
        aoe_x=-1;aoe_y=-1
        if(time.time()-self.__lastshot>0.2):
            for i in range(len(ballons)):
                if(abs(ballons[i].x-self.x)+abs(ballons[i].y-self.y)<=10 and ballons[i].dead==0):
                    flag2=1
                    aoe_x=ballons[i].x;aoe_y=ballons[i].y
                    break
            if(flag2==0):
                for i in range(len(barabarians)):
                    if(abs(barabarians[i].x-self.x)+abs(barabarians[i].y-self.y)<=10 and barabarians[i].dead==0):
                        aoe_x=barabarians[i].x;aoe_y=barabarians[i].y
                        flag=1
                        break
            if(flag==0 and king_spawned==1 and flag2==0):
                if(abs(k.x-self.x)+abs(k.y-self.y)<=10 and k.destroyed==0):
                    flag1=1
                    aoe_x=k.x;aoe_y=k.y
                    k.update_health()
            if(flag==0 and flag1==0 and flag2==0):
                for i in range(len(archers)):
                    if(abs(archers[i].x-self.x)+abs(archers[i].y-self.y)<=10 and archers[i].dead==0):
                        aoe_x=archers[i].x;aoe_y=archers[i].y
                        flag=1
                        break
            
            if(aoe_x!=-1):
                flag=0;flag1=0;flag2=0
                for i in range(len(ballons)):
                    if(abs(ballons[i].x-aoe_x)+abs(ballons[i].y-aoe_y)<=3 and ballons[i].dead==0):
                        ballons[i].health-=self.damage

                for i in range(len(barabarians)):
                    if(abs(barabarians[i].x-aoe_x)+abs(barabarians[i].y-aoe_y)<=3 and barabarians[i].dead==0):
                        barabarians[i].health-=self.damage
                        
                if(king_spawned==1):
                    if(abs(k.x-aoe_x)+abs(k.y-aoe_y)<=3 and k.destroyed==0):
                        flag1=1
                        k.health-=self.damage
                        k.update_health()
                
                for i in range(len(archers)):
                    if(abs(archers[i].x-aoe_x)+abs(archers[i].y-aoe_y)<=3 and archers[i].dead==0):
                        archers[i].health-=self.damage
                               
            self.__lastshot=time.time()
                
           
            
        
        
        

class Wall(Buildings):
   
    def __init__(self,x,y):
        self.x=x;self.y=y
        self.__width=1
        self.__height=1
        self.destroyed=0
        self.__string=["/"]
        self.health=200
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
        
    def get_string(self):
        return self.__string
        
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
            
    def low_color(self,x,y,string):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            print("\033["+str(posx)+";"+str(posy)+"H"+Back.WHITE+string[i],end="")
            
    def mid_color(self,x,y,string):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            print("\033["+str(posx)+";"+str(posy)+"H"+Back.LIGHTBLUE_EX+string[i],end="")
                    
    def destroy(self,x,y,string):
        for i in range(len(string)):
            posx=startx-1+x+i;posy=starty-1+y
            village[x+i][y:y+len(string[i])]=str(" ")*len(string[i])
            print("\033["+str(posx)+";"+str(posy)+"H"+Style.RESET_ALL+string[i],end="")

    
            
            
        
        
class Barbarian(Troops):
    def __init__(self,x,y):
        self.health=50
        self.name="b"
        self.damage=6
        self.speed=1
        self.orig=50
        self.__width=1
        self.dead=0
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
            buildings[building_index].health-=self.damage
        else:
            target=walls[str(self.x+i)+"_"+str(self.y+j)]
            target.health-=self.damage
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
    

    def get_string(self):
        return self.__string
    
class Archer(Troops):
    def __init__(self,x,y):
        self.health=25
        self.name="A"
        self.damage=3
        self.speed=2
        self.range=6
        self.orig=25
        self.__width=1
        self.__lastshot=0
        self.dead=0
        self.__height=1
        self.__string=["A"]
        self.x=x
        self.y=y
        self.clear=[" "]
        Troops.addtroop(self,self.x,self.y,self.__string)
        
    def move(self,i,j):
        ret=self.attack(i,j)
        if(ret==0):
            if(village[self.x+i][self.y+j]=="w"):
                target=walls[str(self.x+i)+"_"+str(self.y+j)]
                target.health-=self.damage
                target.destroyed=1
                if(target.health<=0):
                    target.clear()
            else:
                Troops.move(self,self.x,self.y,self.__string,self.clear,i,j)
                self.x+=i;self.y+=j
            
    def attack(self,i,j):
       
        for i in range(len(buildings)):
            if(abs(buildings[i].x-self.x)+abs(buildings[i].y-self.y)<=self.range and buildings[i].destroyed==0):
                if(time.time()-self.__lastshot>0.2):
                    buildings[i].health-=self.damage
                    self.__lastshot=time.time()
                flag=1
                return 1
                break
        return 0

    def nearest(self):
        dis=float("inf")
        ind=0
        for i in range(len(buildings)):
            if(abs(buildings[i].x-self.x)+abs(buildings[i].y-self.y)<dis and buildings[i].destroyed==0):
                dis=abs(buildings[i].x-self.x)+abs(buildings[i].y-self.y)
                ind=i
        return ind
    

    def get_string(self):
        return self.__string
    

class Ballon(Troops):
    def __init__(self,x,y):
        self.health=50
        self.name="^"
        self.damage=12
        self.speed=2
        self.range=10
        self.orig=50
        self.__width=1
        self.__lastshot=0
        self.__prev=" "
        self.dead=0
        self.__height=1
        self.__string=["^"]
        self.x=x
        self.y=y
        self.clear=[" "]
        Troops.addtroop(self,self.x,self.y,self.__string)
        
        
    def move(self,i,j):
        ret=self.attack(i,j)
        if(ret==0):
            Troops.move(self,self.x,self.y,self.__string,self.clear,i,j)
            if(self.__prev!=" " and self.__prev!="w"):
                building_index=mapping[self.__prev]
                building=buildings[building_index]
                if(building.destroyed==0):
                    building.add(building.x,building.y,building.get_string(),1)
            if(self.__prev=="w"):
                string=["/"]
                x=self.x;y=self.y
                posx=startx-1+x;posy=starty-1+y
                print("\033["+str(posx)+";"+str(posy)+"H"+Back.GREEN+string[0],end="")
                print(Style.RESET_ALL,end="")
            
            self.x+=i;self.y+=j
        else:
            Troops.move(self,self.x,self.y,self.__string,self.clear,0,0)
        self.__prev=village[self.x][self.y]
            
    def attack(self,i,j):
        flag=0
        for i in range(len(defenses)):
            if(abs(defenses[i].x-self.x)+abs(defenses[i].y-self.y)==0 and defenses[i].destroyed==0):
                if(time.time()-self.__lastshot>0.2):
                    defenses[i].health-=self.damage
                    self.__lastshot=time.time()
                flag=1
                return 1
        for i in range(len(defenses)):
            if(defenses[i].destroyed==0):
                flag=1
                break
        else:
            flag=0
                
        if(flag==0):
            dis=float("inf")
            for i in range(len(buildings)):
                if(abs(buildings[i].x-self.x)+abs(buildings[i].y-self.y)==0 and buildings[i].destroyed==0):
                    if(time.time()-self.__lastshot>0.2):
                        buildings[i].health-=self.damage
                        self.__lastshot=time.time()
                    flag=1
                    return 1
        return 0

    def nearest(self):
        dis=float("inf")
        ind=0
        flag=0
        for i in range(len(defenses)):
            if(abs(defenses[i].x-self.x)+abs(defenses[i].y-self.y)<dis and defenses[i].destroyed==0):
                dis=abs(defenses[i].x-self.x)+abs(defenses[i].y-self.y)
                flag=1
                ind=i
        for i in range(len(defenses)):
            if(defenses[i].destroyed==0):
                flag=1
                return buildings.index(defenses[ind])
        else:
            flag=0
        
        if(flag==0):
            dis=float("inf")
            for i in range(len(buildings)):
                if(abs(buildings[i].x-self.x)+abs(buildings[i].y-self.y)<dis and buildings[i].destroyed==0):
                    dis=abs(buildings[i].x-self.x)+abs(buildings[i].y-self.y)
                    flag=1
                    ind=i
        return ind
                    
                    
                    
        
            
        
    

    def get_string(self):
        return self.__string
    
        
   
class King(Troops):
    def __init__(self,x,y):
        self.health=250
        self.name="k"
        self.destroyed=0
        self.orig=250
        self.bar=48
        self.number=47
        self.damage=50
        self.speed=1
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
            buildings[building_index].health-=self.damage
            
        elif(village[self.x+i][self.y+j]=="w"):
            target=walls[str(self.x+i)+"_"+str(self.y+j)]
            target.health-=self.damage
            target.destroyed=1
            if(target.health<=0):
                target.clear()
                
    def update_health(self):
        print("\033["+str(startx+47)+";"+str(0)+"H"+Style.RESET_ALL+" "*4,end="")
        print("\033["+str(startx+48)+";"+str(0)+"H"+Style.RESET_ALL+" "*50,end="")
        print("\033["+str(startx+47)+";"+str(0)+"H"+Style.RESET_ALL+str(max(0,self.health)),end="")
        print("\033["+str(startx+48)+";"+str(0)+"H"+Back.GREEN+"|"*int(self.health//5),end="") 
        
class Queen(Troops):
    def __init__(self,x,y):
        self.health=250
        self.name="k"
        self.destroyed=0
        self.orig=250
        self.bar=48
        self.number=47
        self.damage=30
        self.speed=1
        self.__string=["Q"]
        self.x=x
        self.movement=[0,1]
        self.y=y
        self.clear=[" "]
        Troops.addtroop(self,self.x,self.y,self.__string)
    
    def move(self,i,j):
        if(village[self.x+i][self.y+j]==" "):
            Troops.move(self,self.x,self.y,self.__string,self.clear,i,j)
            self.x+=i;self.y+=j
            self.movement=[i,j]
   
    
    def attack(self,i,j):
        dirx=self.x+self.movement[0]*8;diry=self.y+self.movement[1]*8
        
        
        for i in range(len(buildings)):
            if(abs(buildings[i].x-dirx)+abs(buildings[i].y-diry)<=5 and buildings[i].destroyed==0):
                buildings[i].health-=self.damage
        
        for i in walls:
            if(abs(walls[i].x-dirx)+abs(walls[i].y-diry)<=5 and walls[i].destroyed==0):
                walls[i].health-=self.damage
                if(walls[i].health<=0):
                    walls[i].destroyed=0
                    walls[i].clear()
                
                
        # if(village[self.x+i][self.y+j]!="w" and village[self.x+i][self.y+j]!=" "):
        #     building_index=mapping[village[self.x+i][self.y+j]]
        #     buildings[building_index].health-=self.damage
            
        # elif(village[self.x+i][self.y+j]=="w"):
        #     target=walls[str(self.x+i)+"_"+str(self.y+j)]
        #     target.health-=self.damage
        #     target.destroyed=1
        #     if(target.health<=0):
        #         target.clear()
                
    def update_health(self):
        print("\033["+str(startx+47)+";"+str(0)+"H"+Style.RESET_ALL+" "*4,end="")
        print("\033["+str(startx+48)+";"+str(0)+"H"+Style.RESET_ALL+" "*50,end="")
        print("\033["+str(startx+47)+";"+str(0)+"H"+Style.RESET_ALL+str(max(0,self.health)),end="")
        print("\033["+str(startx+48)+";"+str(0)+"H"+Back.GREEN+"|"*int(self.health//5),end="") 
    
        
        
class Spells:
    def __init__(self):
        self.time=5 
        
    def spell(self,speed):
        global timeout,barabarians,k,king_spawned
        self.speed=speed
        timeout=timeout/speed
        for i in range(len(barabarians)):
            barabarians[i].damage*=2
        if(king_spawned==1):
            k.damage*=2
        
        
    def deactive(self):
        global timeout,barabarians,k,king_spawned
        timeout*=self.speed
        for i in range(len(barabarians)):
            barabarians[i].damage//=2
        if(king_spawned==1):
            k.damage//=2
        

class Rage(Spells):
    raged=0
    def __init__(self):
        self.time=5
        

class Heal(Spells):
    def __init__(self):
        self.time=5
    def spell(self):
        global timeout,barabarians,k,king_spawned
        #print(barabarians[0].health)
        for i in range(len(barabarians)):
            if(barabarians[i].dead==0):
                barabarians[i].health=min(barabarians[i].orig,1.5*barabarians[i].health)
        #print(barabarians[0].health)
        if(king_spawned==1):
            if(k.destroyed==0):
                k.health=min(k.orig,1.5*k.health)
                
        
            
  
class Get:
    def __call__(self):
        global king_spawned
        global timetick
        global active_spell,rage,ragetime,rage_spell,heal_spell,heal,healtime,capture,starttick,archers,ballons,char_inp
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
                capture.append([time.time()-starttick,"z"])
            if(ch=="x"):
                b=Barbarian(position2[0],position2[1])
                barabarians.append(b)
                capture.append([time.time()-starttick,"x"])
            if(ch=="c"):
                b=Barbarian(position3[0],position3[1])
                barabarians.append(b)
                capture.append([time.time()-starttick,"c"])
            if(ch=="k" and king_spawned==0):
                if(char_inp=="k"):
                    k=King(2,5)
                else:
                    k=Queen(2,5)
                king_spawned=1
                capture.append([time.time()-starttick,"k"])
            
            if(ch=="b"):
                a=Archer(position1[0],position1[1])
                archers.append(a)
                capture.append([time.time()-starttick,"b"])
                
            if(ch=="n"):
                a=Archer(position2[0],position2[1])
                archers.append(a)
                capture.append([time.time()-starttick,"n"])
            
            if(ch=="m" ):
                a=Archer(position3[0],position3[1])
                archers.append(a)
                capture.append([time.time()-starttick,"m"])
                
            if(ch=="r"):
                a=Ballon(position1[0],position1[1])
                ballons.append(a)
                capture.append([time.time()-starttick,"r"])
            
            if(ch=="t" and king_spawned==0):
                a=Ballon(position2[0],position2[1])
                ballons.append(a)
                capture.append([time.time()-starttick,"t"])
                
                
            if(ch=="y" and king_spawned==0):
                a=Ballon(position3[0],position3[1])
                ballons.append(a)
                capture.append([time.time()-starttick,"y"])
            
         
            if(ch=="a" and king_spawned==1 and k.destroyed==0):
                k.move(0,-1)
                k.movement=[0,-1]
                capture.append([time.time()-starttick,"a"])
                
            if(ch=="w" and king_spawned==1 and k.destroyed==0):
                k.move(-1,0);k.movement=[-1,0]
                capture.append([time.time()-starttick,"w"])
                
            if(ch=="d" and king_spawned==1 and k.destroyed==0):
                k.move(0,1);k.movement=[0,1]
                capture.append([time.time()-starttick,"d"])
                 
            if(ch=="s" and king_spawned==1 and k.destroyed==0):
                k.move(1,0);k.movement=[1,0]
                capture.append([time.time()-starttick,"s"])
                 
            if(ch==" " and king_spawned==1 and k.destroyed==0):
                if(char_inp=="k"):
                    k.attack(0,1)
                    k.attack(0,-1)
                    k.attack(1,0)
                    k.attack(-1,0)
                    k.attack(1,1)
                    k.attack(-1,-1)
                    k.attack(1,-1)
                    k.attack(-1,1)
                else:
                    k.attack(0,1)
                
                capture.append([time.time()-starttick," "])
                
            if(ch=="j"):
                if(rage==0):
                    rage_spell=Rage()
                    rage_spell.spell(4)
                    ragetime=time.time()
                    rage=1
                    capture.append([time.time()-starttick,"j"])
                    
            if(ch=="i"):
                if(heal==0):
                    heal_spell=Heal()
                    heal_spell.spell()
                    healtime=time.time()
                    heal=1
                    capture.append([time.time()-starttick,"i"])
            if(ch=="e"):
                capture.append([time.time()-starttick,"e"])
                return 1
            timetick=time.time()
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
      


class AlarmException(Exception):
    pass


def alarmHandler(signum, frame):
    raise AlarmException


def input_to(callback,timeout=0):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text=callback()
        signal.alarm(0)
        return text
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return None




def level_1():
    exit=0
    global mapping
    mapping={"0":0,"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15,"p":16,"q":17}
    th=TownHall(21,38);symbol="a"
    h1=Hut(10,20);symbol="b"
    h2=Hut(10,24);symbol="c"
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
    wizard1=Wizard(40,40)
    wizard2=Wizard(15,65)
    global buildings,defenses
    buildings=[th,h1,h2,h3,h4,h5,h6,h7,h8,h9,cannon1,cannon2,cannon3,cannon4,cannon5,cannon6,wizard1,wizard2]
    defenses=[wizard1,wizard2,cannon1,cannon2,cannon3,cannon4,cannon5,cannon6]
    global cannons
    cannons=[cannon1,cannon2,cannon3,cannon4,cannon5,cannon6]
    global wizards
    wizards=[wizard1,wizard2]


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



starttick=time.time()
#-----------------------------------------------Main Code------------------------------------
def getinput():
    a=Get()
    ans=a.__call__()
    return ans
position1=(2,35)
position2=(45,20)
position3=(40,70)
def check_end_game():
    global king_spawned,k
    buildflag=1;kflag=1;bflag=1
    for i in range(len(barabarians)):
        if(barabarians[i].dead==0):
            bflag=1
            break
    else:
        if(len(barabarians)>0):
            bflag=0
    for i in range(len(buildings)):
        if(buildings[i].destroyed==0):
            buildflag=1
            break
    else:
        buildflag=0
    if(king_spawned==1):
        if(k.destroyed==1):
            kflag=0
        else:
            kflag=1
    if(kflag==0 and bflag==0):
        return (True,"You Lose")
    elif(buildflag==0):
        return (True,"You Won")
    
    else:
        return (False,"")
        
def animate():
    global rage,king_spawned,k,wizards
    res=check_end_game()
    if(res[0]):
        return res
    for i in range(len(buildings)):
        if(buildings[i].health<(70/100)*buildings[i].orig and buildings[i].destroyed==0):
            buildings[i].mid_color()
        if(buildings[i].health<=(30/100)*buildings[i].orig and buildings[i].destroyed==0):
            buildings[i].low_color()
        if(buildings[i].health<=0 and buildings[i].destroyed==0):
            buildings[i].clear()
    # if(rage==1):
    #     if(time.time()-ragetime>10):
    #         rage_spell.deactive()

        
    for i in range(len(barabarians)):
        if(barabarians[i].dead==0):
            result=barabarians[i].nearest()
            locx=buildings[result].x;locy=buildings[result].y
            dirx=(locx-barabarians[i].x);diry=(locy-barabarians[i].y)
            movex=0 if(dirx==0) else (locx-barabarians[i].x)/abs(locx-barabarians[i].x)
            movey=0 if(diry==0) else (locy-barabarians[i].y)/abs(locy-barabarians[i].y)
            barabarians[i].move(int(movex),int(movey))
        if(barabarians[i].health<=(70/100)*barabarians[i].orig and barabarians[i].dead==0):
            barabarians[i].mid_color(barabarians[i].x,barabarians[i].y,barabarians[i].get_string())
        if(barabarians[i].health<=(30/100)*barabarians[i].orig and barabarians[i].dead==0):
            barabarians[i].low_color(barabarians[i].x,barabarians[i].y,barabarians[i].get_string())
        if(barabarians[i].health<=0 and barabarians[i].dead==0):
            barabarians[i].destroy(barabarians[i].x,barabarians[i].y,barabarians[i].clear)
            barabarians[i].dead=1
            
        
    for i in range(len(archers)):
        if(archers[i].dead==0):
            for j in range(archers[i].speed):
                result=archers[i].nearest()
                locx=buildings[result].x;locy=buildings[result].y
                dirx=(locx-archers[i].x);diry=(locy-archers[i].y)
                movex=0 if(dirx==0) else (locx-archers[i].x)/abs(locx-archers[i].x)
                movey=0 if(diry==0) else (locy-archers[i].y)/abs(locy-archers[i].y)
                archers[i].move(int(movex),int(movey))
            
        if(archers[i].health<=(70/100)*archers[i].orig and archers[i].dead==0):
            archers[i].mid_color(archers[i].x,archers[i].y,archers[i].get_string())
        if(archers[i].health<=(30/100)*archers[i].orig and archers[i].dead==0):
            archers[i].low_color(archers[i].x,archers[i].y,archers[i].get_string())
        if(archers[i].health<=0 and archers[i].dead==0):
            archers[i].destroy(archers[i].x,archers[i].y,archers[i].clear)
            archers[i].dead=1
            
    
    for i in range(len(ballons)):
        if(ballons[i].dead==0):
            for j in range(ballons[i].speed):
                result=ballons[i].nearest()
                locx=buildings[result].x;locy=buildings[result].y
                dirx=(locx-ballons[i].x);diry=(locy-ballons[i].y)
                movex=0 if(dirx==0) else (locx-ballons[i].x)/abs(locx-ballons[i].x)
                movey=0 if(diry==0) else (locy-ballons[i].y)/abs(locy-ballons[i].y)
                ballons[i].move(int(movex),int(movey))
            
        if(ballons[i].health<=(70/100)*ballons[i].orig and ballons[i].dead==0):
            ballons[i].mid_color(ballons[i].x,ballons[i].y,ballons[i].get_string())
        if(ballons[i].health<=(30/100)*ballons[i].orig and ballons[i].dead==0):
            ballons[i].low_color(ballons[i].x,ballons[i].y,ballons[i].get_string())
        if(ballons[i].health<=0 and ballons[i].dead==0):
            ballons[i].destroy(ballons[i].x,ballons[i].y,ballons[i].clear)
            ballons[i].dead=1
            
    if(king_spawned==1):
        if(k.health<=0 and k.destroyed==0):
            k.destroy(k.x,k.y,k.clear)
            k.destroyed=1
       
    for i in range(len(cannons)):
        if(cannons[i].destroyed==0):
            c=cannons[i].attack()
    
    for i in range(len(wizards)):
        if(wizards[i].destroyed==0):
            c=wizards[i].attack()
    return (False,"")
            
    

level_1()
while(1):
    os.system("stty -echo")
    ans=input_to(getinput,timeout)
    if(ans==1):
        os.system("stty echo")
        break
    game=animate()
    if(game[0]==1):
        print("\033["+str(startx+49)+";"+str(0)+"H"+game[1],end="")
        os.system("stty echo")
        break
    
    print("",end="")
    print("\r",end="")
    time.sleep(timeout)
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    
f.write(str(capture))
total.close()
total=open("./src/total.txt","w+")
total.write(str(totalreplays+1))
total.close()
f.close()
    
    

    

