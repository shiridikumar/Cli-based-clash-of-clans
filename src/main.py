from colorama import Fore, Back, Style
import time
horizontal=("-"*80).center(90)
vertical=(("|"+" "*80+"|").center(90)+"\n")*45
print(horizontal)
print(vertical,end="")
print(horizontal)


# print(king)

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



prevx=startx;prevy=starty
# for i in range(0,50):
#     prevx=startx+i;prevy=starty+i
#     # print("\033["+str(prevx)+";"+str(prevy)+"H"+barbarian)
#     # print("\033["+str(prevx+1)+";"+str(prevy)+"H"+barbarian_bottom)

#     print("\033["+str(prevx)+";"+str(prevy)+"H"+king)
#     print("\033["+str(prevx+1)+";"+str(prevy)+"H"+king_mid)
#     print("\033["+str(prevx+2)+";"+str(prevy)+"H"+king_bottom)

#     # print("\033["+str(prevx)+";"+str(prevy)+"H"+king_clear)
#     # print("\033["+str(prevx+1)+";"+str(prevy)+"H"+king_mid_clear)
#     # print("\033["+str(prevx)+";"+str(prevy)+"H"+king_bottom_clear)

#     # print("\033["+str(prevx+1)+";"+str(prevy)+"H"+barbarian_bottom)

#     time.sleep(0.3)
#     print("\033["+str(prevx)+";"+str(prevy)+"H"+king_clear)
#     print("\033["+str(prevx+1)+";"+str(prevy)+"H"+king_mid_clear)
#     print("\033["+str(prevx+2)+";"+str(prevy)+"H"+king_bottom_clear)

#     # print("\033["+str(prevx)+";"+str(prevy)+"H"+barbarian_clear,end="")
#     # print("\033["+str(prevx+1)+";"+str(prevy)+"H"+barbarian_clear_bottom,end="")
# print("\n\n")

townhall=("+"+"-"*4+"+")+"\n"+("|"+"TOWN"+"|\n")+("|"+"HALL"+"|\n")+(("|"+" "*4+"|\n")*1)+("+"+"-"*4+"+")


hut=(" /\\ ")+"\n"+"[ H]"+"\n"

cannon="[<C>]"

th1=("+"+"-"*4+"+")+"\n"
th2=("|"+"TOWN"+"|\n")
th3=("|"+"HALL"+"|\n")
th4=(("|"+" "*4+"|\n")*1)
th5=("+"+"-"*4+"+")
thx=0
thy=0
thpos=(21,38)
h1pos=(10,20)
h2pos=(10,30)
h3pos=(18,20)
h4pos=(15,55)
h5pos=(23,55)
h6pos=(28,24)
cannon1_pos=(18,30)
cannon2_pos=(27,38)
cannon3_pos=(10,55)

prevx=startx+thpos[0]-1
prevy=starty+thpos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+th1)
print("\033["+str(prevx+1)+";"+str(prevy)+"H"+th2)
print("\033["+str(prevx+2)+";"+str(prevy)+"H"+th3)
print("\033["+str(prevx+3)+";"+str(prevy)+"H"+th4)
print("\033["+str(prevx+4)+";"+str(prevy)+"H"+th5)

hut_top=(" /\\ ")+"\n"
hut_bottom="[ H]"

prevx=startx+h1pos[0]-1;prevy=starty+h1pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+hut_top)
print("\033["+str(prevx+1)+";"+str(prevy)+"H"+hut_bottom)

prevx=startx+h2pos[0]-1;prevy=starty+h2pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+hut_top)
print("\033["+str(prevx+1)+";"+str(prevy)+"H"+hut_bottom)

prevx=startx+h3pos[0]-1;prevy=starty+h3pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+hut_top)
print("\033["+str(prevx+1)+";"+str(prevy)+"H"+hut_bottom)

prevx=startx+cannon1_pos[0]-1;prevy=starty+cannon1_pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+cannon)
print("")

prevx=startx+h4pos[0]-1;prevy=starty+h4pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+hut_top)
print("\033["+str(prevx+1)+";"+str(prevy)+"H"+hut_bottom)
print("")

prevx=startx+h5pos[0]-1;prevy=starty+h5pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+hut_top)
print("\033["+str(prevx+1)+";"+str(prevy)+"H"+hut_bottom)
print("")

prevx=startx+cannon2_pos[0]-1;prevy=starty+cannon2_pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+cannon)
print("")

prevx=startx+cannon3_pos[0]-1;prevy=starty+cannon3_pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+cannon)
print("")


prevx=startx+h6pos[0]-1;prevy=starty+h6pos[1]-1
print("\033["+str(prevx)+";"+str(prevy)+"H"+hut_top)
print("\033["+str(prevx+1)+";"+str(prevy)+"H"+hut_bottom)
print("")


# prevx=startx+thpos[0]+2-1;prevy=starty+thpos[1]-2
wall1_attrib=(20,15)
wall1="|"+"-"*(wall1_attrib[0]-1)
wall1_start=(startx+thpos[0]+2-1,starty+thpos[1]-1-wall1_attrib[0])

print("\033["+str(wall1_start[0])+";"+str(wall1_start[1])+"H"+wall1)

for i in range(wall1_attrib[1]):
    print("\033["+str(wall1_start[0]-wall1_attrib[1]+i)+";"+str(wall1_start[1])+"H"+"|")


print("\033["+str(wall1_start[0]-wall1_attrib[1])+";"+str(wall1_start[1])+"H"+wall1+"-"*2)


for i in range(wall1_attrib[1]-2):
    print("\033["+str(wall1_start[0]-wall1_attrib[1]+i)+";"+str(wall1_start[1]+wall1_attrib[0]+2)+"H"+"|")


wall2_attrib=(20,15)
wall2="-"*wall2_attrib[0]

wall2_start=(startx+thpos[0]-wall2_attrib[1]+2,starty+thpos[1]+2)
print("\033["+str(wall2_start[0])+";"+str(wall2_start[1])+"H"+wall2)

for i in range(wall2_attrib[1]+8):
    print("\033["+str(wall2_start[0]+i)+";"+str(wall2_start[1]+wall2_attrib[0])+"H"+"|")


print("\033["+str(wall2_start[0]+i)+";"+str(wall2_start[1]-wall2_attrib[0])+"H"+wall2*2)

endwall=(startx+thpos[0]+2-1,wall2_start[1]-wall2_attrib[0])
for i in range(wall2_start[0]+i-(thpos[0]+startx)):
    print("\033["+str(endwall[0]+i)+";"+str(endwall[1])+"H"+"|")














n=input()

