from colorama import Fore, Back, Style
import time
horizontal=("-"*140).center(160)
vertical=(("|"+" "*140+"|").center(160)+"\n")*50
print(horizontal)
print(vertical,end="")
print(horizontal)


# print(king)

starty=11;prevx=starty
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



prevx=startx;prevy=starty
for i in range(0,50):
    prevx=startx+i;prevy=starty+i
    # print("\033["+str(prevx)+";"+str(prevy)+"H"+barbarian)
    # print("\033["+str(prevx+1)+";"+str(prevy)+"H"+barbarian_bottom)

    print("\033["+str(prevx)+";"+str(prevy)+"H"+king)
    print("\033["+str(prevx+1)+";"+str(prevy)+"H"+king_mid)
    print("\033["+str(prevx+2)+";"+str(prevy)+"H"+king_bottom)

    # print("\033["+str(prevx)+";"+str(prevy)+"H"+king_clear)
    # print("\033["+str(prevx+1)+";"+str(prevy)+"H"+king_mid_clear)
    # print("\033["+str(prevx)+";"+str(prevy)+"H"+king_bottom_clear)

    # print("\033["+str(prevx+1)+";"+str(prevy)+"H"+barbarian_bottom)

    time.sleep(0.3)
    print("\033["+str(prevx)+";"+str(prevy)+"H"+king_clear)
    print("\033["+str(prevx+1)+";"+str(prevy)+"H"+king_mid_clear)
    print("\033["+str(prevx+2)+";"+str(prevy)+"H"+king_bottom_clear)

    # print("\033["+str(prevx)+";"+str(prevy)+"H"+barbarian_clear,end="")
    # print("\033["+str(prevx+1)+";"+str(prevy)+"H"+barbarian_clear_bottom,end="")
print("\n\n")

