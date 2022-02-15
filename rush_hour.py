''' This is final submission for the rush_hour Sat solver assignment.
Team :-
Niyati Mehta(200050091)
Parshant Arora(200050099)
Hastyn Doshi(200070025)
Submitted on 15/02/2022
Have fun solving :)
you don't know the pain of finding bugs in these clauses :')
'''

from z3 import *

import sys
 

argumentList = sys.argv

file_path = sys.argv[1]



def interval(a,b):
    return range(a,b+1)

pos_c = []
m_c = []
collisions_c = []



with open(file_path, 'r') as f:
    lines = f.readlines()
    n,l = lines[0].split(',')
    n = int(n)
    l = int(l)

    r_x,r_y = lines[1].split(',')
    r_x = int(r_x)
    r_y = int(r_y)
    
    h = [ [ [Bool("h_%s_%s_%s" % (i, j, t)) for t in range(l+1) ] for j in range(n) ] for i in range(n)]
    v = [ [ [ Bool("v_%s_%s_%s" % (i, j, t)) for t in range(l+1) ] for j in range(n) ] for i in range(n)]
    r = [ [ [ Bool("r_%s_%s_%s" % (i, j, t)) for t in range(l+1) ] for j in range(n) ] for i in range(n)]
    
    m = [ [ [ Bool("m_%s_%s_%s" % (i, j, t)) for t in range(l+1) ] for j in range(n) ] for i in range(n)]
    X = [ [ Bool("X_%s_%s" % (i, j)) for j in range(n) ] for i in range(n)]


    for i in range(2,len(lines)):
        orien,x,y = lines[i].split(',')
        orien = int(orien)
        x = int(x)
        y = int(y)
        if orien == 0:
            pos_c.append(v[x][y][0])
        elif orien == 1:
            pos_c.append(h[x][y][0])
        else :
            pos_c.append(X[x][y])

    pos_c.append(r[r_x][r_y][0])    
    #input complete

for i in range(n):
    for j in range(n):
        m_c.append(Not(m[i][j][0]))
        if v[i][j][0] not in pos_c:
            pos_c.append(Not(v[i][j][0])) #init to 0 
        if h[i][j][0] not in pos_c:
            pos_c.append(Not(h[i][j][0])) #init to 0    
        if X[i][j] not in pos_c:
            pos_c.append(Not(X[i][j])) #init to 0        
        if not (i==r_x and j==r_y):
            pos_c.append(Not(r[i][j][0]))        

winning_c = [Or([(r[r_x][n-2][t]) for t in range(0,l+1)] )]



                            #Moves

                    # if move, then pos change
#left move
for i in range(n):
    for j in interval(1,n-2): #both included
        for t in interval(1,l):
            m_c.append(Implies(And(m[i][j][t],h[i][j][t-1]), And(Not(h[i][j+1][t]), Not(h[i][j][t]), h[i][j-1][t])))
            m_c.append(Implies(And(m[i][j][t],r[i][j][t-1]), And(Not(r[i][j+1][t]), Not(r[i][j][t]), r[i][j-1][t])))
         

#right move
for i in range(n):
    for j in interval(1,n-2): #both included
        for t in interval(1,l):
            m_c.append(Implies(And(m[i][j][t],h[i][j-1][t-1]), And(Not(h[i][j-1][t]), Not(h[i][j+1][t]), h[i][j][t])))
            m_c.append(Implies(And(m[i][j][t],r[i][j-1][t-1]), And(Not(r[i][j-1][t]), Not(r[i][j+1][t]), r[i][j][t])))
      
            

#up move
for j in range(n):
    for i in interval(1,n-2): #both included
        for t in interval(1,l):
            m_c.append(Implies(And(m[i][j][t],v[i][j][t-1]), And(Not(v[i][j][t]), Not(v[i+1][j][t]), v[i-1][j][t])))
          
            


#down move
for j in range(n):
    for i in interval(1,n-2): #both included
        for t in interval(1,l):
            m_c.append(Implies(And(m[i][j][t],v[i-1][j][t-1]), And(Not(v[i-1][j][t]), Not(v[i+1][j][t]), v[i][j][t])))
            
                    # Move only if there is a car

for i in interval(1,n-2):
    for j in interval(1, n-2):
        for t in interval(1,l):
            car_left = And(m[i][j][t],h[i][j][t-1])
            car_right = And(m[i][j][t],h[i][j-1][t-1])
            car_down = And(m[i][j][t],v[i][j][t-1])
            car_up = And(m[i][j][t],v[i-1][j][t-1])
            red_car_left = And(m[i][j][t],r[i][j][t-1])
            red_car_right = And(m[i][j][t],r[i][j-1][t-1])
            m_c.append(Implies(m[i][j][t], Or(car_left,car_right,car_down,car_up,red_car_left,red_car_right)))

#for near wall cases

#left wall touch
for i in interval(1,n-1):
        for t in interval(1,l):
            j = 0
            car_left = And(m[i][j][t],h[i][j][t-1])
            # car_right = And(m[i][j][t],h[i][j-1][t-1])
            car_down = And(m[i][j][t],v[i][j][t-1])
            car_up = And(m[i][j][t],v[i-1][j][t-1])
            red_car_left = And(m[i][j][t],r[i][j][t-1])
            m_c.append(Implies(m[i][j][t], Or(car_left,car_down,car_up,red_car_left)))

#right wall
for i in interval(1,n-1):
        for t in interval(1,l):
            j = n-1
            # car_left = And(m[i][j][t],h[i][j][t-1])
            car_right = And(m[i][j][t],h[i][j-1][t-1])
            red_car_right = And(m[i][j][t],r[i][j-1][t-1])
            car_down = And(m[i][j][t],v[i][j][t-1])
            car_up = And(m[i][j][t],v[i-1][j][t-1])
            m_c.append(Implies(m[i][j][t], Or(car_right,car_down,car_up,red_car_right)))


#top wall
for j in interval(1, n-1):
    for t in interval(1,l):
        i = 0
        car_left = And(m[i][j][t],h[i][j][t-1])
        car_right = And(m[i][j][t],h[i][j-1][t-1])
        red_car_left = And(m[i][j][t],r[i][j][t-1])
        red_car_right = And(m[i][j][t],r[i][j-1][t-1])
        car_down = And(m[i][j][t],v[i][j][t-1])
        # car_up = And(m[i][j][t],v[i-1][j][t-1])
        m_c.append(Implies(m[i][j][t], Or(car_left,car_right,car_down,red_car_right,red_car_left)))



#bottom wall
for j in interval(1, n-1):
    for t in interval(1,l):
        i = n-1
        car_left = And(m[i][j][t],h[i][j][t-1])
        car_right = And(m[i][j][t],h[i][j-1][t-1])
        red_car_left = And(m[i][j][t],r[i][j][t-1])
        red_car_right = And(m[i][j][t],r[i][j-1][t-1])
        # car_down = And(m[i][j][t],v[i][j][t-1])
        car_up = And(m[i][j][t],v[i-1][j][t-1])
        m_c.append(Implies(m[i][j][t], Or(car_left,car_right,car_up,red_car_left,red_car_right)))


#only top left corner left
for t in interval(1,l):
    i = 0
    j = 0
    car_left = And(m[i][j][t],h[i][j][t-1])
    # car_right = And(m[i][j][t],h[i][j-1][t-1])
    car_down = And(m[i][j][t],v[i][j][t-1])
    # car_up = And(m[i][j][t],v[i-1][j][t-1])
    m_c.append(Implies(m[i][j][t], Or(car_left,car_down)))

                    #No Spawnning

#for horizontal car
for i in range(n):
    for j in range(n):
        for t in interval(0,l):
            
            if (j<(n-1) and j>0 and t>0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(And(h[i][j-1][t-1],m[i][j][t]),h[i][j][t-1],And(h[i][j+1][t-1],m[i][j+1][t]))))
                pos_c.append(Implies(h[i][j][t], Or(And(h[i][j-1][t+1],m[i][j][t+1]),h[i][j][t+1],And(h[i][j+1][t+1],m[i][j+1][t+1]))))

            if (j<(n-1) and j>0 and t==0 and t<l):
               pos_c.append(Implies(h[i][j][t], Or(And(h[i][j-1][t+1],m[i][j][t+1]),h[i][j][t+1],And(h[i][j+1][t+1],m[i][j+1][t+1]))))

            if (j<(n-1) and j==0 and t>0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j][t-1],And(h[i][j+1][t-1],m[i][j+1][t]))))
                pos_c.append(Implies(h[i][j][t], Or(h[i][j][t+1],And(h[i][j+1][t+1],m[i][j+1][t+1]))))
 
            if (j<(n-1) and j==0 and t==0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j][t+1],And(h[i][j+1][t+1],m[i][j+1][t+1]))))

            if (j<(n-1) and j>0 and t>0 and t==l):
                pos_c.append(Implies(h[i][j][t], Or(And(h[i][j-1][t-1],m[i][j][t]),h[i][j][t-1],And(h[i][j+1][t-1],m[i][j+1][t]))))

            if (j<(n-1) and j==0 and t>0 and t==l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j][t-1],And(h[i][j+1][t-1],m[i][j+1][t]))))                

#for red car
for i in range(n):
    for j in range(n):
        for t in interval(0,l):
            
            if (j<(n-1) and j>0 and t>0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(And(r[i][j-1][t-1],m[i][j][t]),r[i][j][t-1],And(r[i][j+1][t-1],m[i][j+1][t]))))
                pos_c.append(Implies(r[i][j][t], Or(And(r[i][j-1][t+1],m[i][j][t+1]),r[i][j][t+1],And(r[i][j+1][t+1],m[i][j+1][t+1]))))

            if (j<(n-1) and j>0 and t==0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(And(r[i][j-1][t+1],m[i][j][t+1]),r[i][j][t+1],And(r[i][j+1][t+1],m[i][j+1][t+1]))))

            if (j<(n-1) and j==0 and t>0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j][t-1],And(r[i][j+1][t-1],m[i][j+1][t]))))
                pos_c.append(Implies(r[i][j][t], Or(r[i][j][t+1],And(r[i][j+1][t+1],m[i][j+1][t+1]))))
 
            if (j<(n-1) and j==0 and t==0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j][t+1],And(r[i][j+1][t+1],m[i][j+1][t+1]))))

            if (j<(n-1) and j>0 and t>0 and t==l):
                pos_c.append(Implies(r[i][j][t], Or(And(r[i][j-1][t-1],m[i][j][t]),r[i][j][t-1],And(r[i][j+1][t-1],m[i][j+1][t]))))

            if (j<(n-1) and j==0 and t>0 and t==l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j][t-1],And(r[i][j+1][t-1],m[i][j+1][t]))))                

          
#for vertical car
for i in range(n):
    for j in range(n):
        for t in interval(0,l):
            
            if (i<(n-1) and i>0 and t>0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(And(v[i-1][j][t-1],m[i][j][t]),v[i][j][t-1],And(v[i+1][j][t-1],m[i+1][j][t]))))
                pos_c.append(Implies(v[i][j][t], Or(And(v[i-1][j][t+1],m[i][j][t+1]),v[i][j][t+1],And(v[i+1][j][t+1],m[i+1][j][t+1]))))

            if (i<(n-1) and i>0 and t==0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(And(v[i-1][j][t+1],m[i][j][t+1]),v[i][j][t+1],And(v[i+1][j][t+1],m[i+1][j][t+1]))))

            if (i<(n-1) and i==0 and t>0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(v[i][j][t-1],And(v[i+1][j][t-1],m[i+1][j][t]))))
                pos_c.append(Implies(v[i][j][t], Or(v[i][j][t+1],And(v[i+1][j][t+1],m[i+1][j][t+1]))))

            if (i<(n-1) and i==0 and t==0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(v[i][j][t+1],And(v[i+1][j][t+1],m[i+1][j][t+1]))))

            if (i<(n-1) and i>0 and t>0 and t==l):
                pos_c.append(Implies(v[i][j][t], Or(And(v[i-1][j][t-1],m[i][j][t]),v[i][j][t-1],And(v[i+1][j][t-1],m[i+1][j][t]))))

            if (i<(n-1) and i==0 and t>0 and t==l):
                pos_c.append(Implies(v[i][j][t], Or(v[i][j][t-1],And(v[i+1][j][t-1],m[i+1][j][t]))))                


                    # forbidden positions

for i in range(n): #left wall
    for t in interval(0,l):
        pos_c.append(Not(h[i][n-1][t]))
        pos_c.append(Not(r[i][n-1][t]))

for j in range(n): #bottom wall
    for t in interval(0,l):
        pos_c.append(Not(v[n-1][j][t]))


                    # forbidden moves(near wall)

for i in range(n):
    for t in interval(1,l):
        m_c.append(Not(And(m[i][0][t], h[i][0][t-1])))
        m_c.append(Not(And(m[i][0][t], r[i][0][t-1])))        


for i in range(n):
    for t in interval(1,l):
        m_c.append(Not(And(m[i][n-1][t], h[i][n-2][t-1])))
        m_c.append(Not(And(m[i][n-1][t], r[i][n-2][t-1])))

for j in range(n):
    for t in interval(1,l):
        m_c.append(Not(And(m[0][j][t], v[0][j][t-1])))

for j in range(n):
    for t in interval(1,l):
        m_c.append(Not(And(m[n-1][j][t], v[n-2][j][t-1])))

                        
                    # only 1 move true

for t in interval(1,l):
    list_of_tuples = []
    for i in range(n):
        for j in range(n):
            list_of_tuples.append((m[i][j][t],1))  
    m_c.append(z3.PbEq(list_of_tuples,1))


                #collisions

'''case 1'''
    ##(i,j)
     #  

for i in interval(0,n-2):
    for j in interval(1,n-1):
        for t in interval(0,l):
            collisions_c.append(Not(And(h[i][j-1][t], v[i][j][t])))
            collisions_c.append(Not(And(r[i][j-1][t], v[i][j][t])))


'''case 2'''
     #
    ##(i,j)  

for i in interval(1,n-1):
    for j in interval(1,n-1):
        for t in interval(0,l):
            collisions_c.append(Not(And(h[i][j-1][t], v[i-1][j][t])))
            collisions_c.append(Not(And(r[i][j-1][t], v[i-1][j][t])))


'''case 3'''
    ##
    # 
for i in interval(0,n-2):
    for j in interval(0,n-2):
        for t in interval(0,l):
            collisions_c.append(Not(And(h[i][j][t], v[i][j][t])))
            collisions_c.append(Not(And(r[i][j][t], v[i][j][t])))

'''case 4'''
    #
    ## 

for i in interval(1,n-1):
    for j in interval(0,n-2):
        for t in interval(0,l):
            collisions_c.append(Not(And(h[i][j][t], v[i-1][j][t])))
            collisions_c.append(Not(And(r[i][j][t], v[i-1][j][t])))

'''case 5'''
    #
    #
    #

for i in interval(1,n-2):
    for j in interval(0,n-1):
        for t in interval(0,l):
            collisions_c.append(Not(And(v[i][j][t], v[i-1][j][t])))


'''case 6'''
    ###

for i in interval(0,n-1):
    for j in interval(1,n-2):
        for t in interval(0,l):
            collisions_c.append(Not(And(h[i][j-1][t], h[i][j][t])))

#with mines

'''case 1    X#'''
for i in range(n):
    for j in range(n):
        for t in interval(0,l):
            pos_c.append(Not(And(h[i][j][t], X[i][j])))

'''case 2   
 X
 #'''
for i in range(n):
    for j in range(n):
        for t in interval(0,l):
            pos_c.append(Not(And(v[i][j][t], X[i][j])))


'''case 3    #X'''
for i in range(n):
    for j in interval(1,n-1):
        for t in interval(0,l):
            pos_c.append(Not(And(h[i][j-1][t], X[i][j])))

'''case 4   
#
X'''
for i in interval(1,n-1):
    for j in range(n):
        for t in interval(0,l):
            pos_c.append(Not(And(v[i-1][j][t], X[i][j])))



s = Solver()
s.add(pos_c + m_c + collisions_c + winning_c)

moves = []
if s.check() == sat:
    true_m = []
    true_h = []
    true_v = []
    true_r = []
    model = s.model()
    final = 0
    reached = False
    
    for t in range(l+1):
        for j in range(n):
            for i in range(n):               
                if model.evaluate(m[i][j][t])==True:
                    true_m.append("m"+str(i)+str(j)+str(t))
                    moves.append((i,j))
                if model.evaluate(v[i][j][t])==True:
                    true_v.append("v"+str(i)+str(j)+str(t))    
                if model.evaluate(h[i][j][t])==True:
                    true_h.append("h"+str(i)+str(j)+str(t))    
                if model.evaluate(r[i][j][t])==True:
                    true_r.append("r"+str(i)+str(j)+str(t))    
                if model.evaluate(r[i][n-2][t])==True:
                    if not reached:
                        final = t
                        reached = True

else:
    print("unsat")
    


cnt = 0
for (a,b) in moves:
    cnt+=1
    add_text = str(a)+","+str(b)
    print(add_text)
    if cnt==final:
        break

    