from colorama import Fore, Back, Style
import time
horizontal=("-"*140).center(160)
vertical=(("|"+" "*140+"|").center(160)+"\n")*50
# print(horizontal)
# print(vertical,end="")
# print(horizontal)
starty=10
startx=2
barbarian=("["+"B"+"]/")+"\n"+("/\\ \n")
#("|"+"-"*4+"|")c
print(barbarian)
king=("_"*4)+"\n"+("{"+" K"+"}/")+("\n /\\ \n")

print(king)
# prevx=startx;prevy=starty
# for i in range(1,50):
#     prevx=startx+i;prevy=starty+i
#     print("\033["+str(prevx)+";"+str(prevy)+"H"+"hello")
#     time.sleep(0.3)
#     print("\033["+str(prevx)+";"+str(prevy)+"H"+" "*len("hello"),end="")
# print("\n\n")