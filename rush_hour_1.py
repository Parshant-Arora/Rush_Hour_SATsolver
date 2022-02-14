# to do
# optimize
# mine

from cv2 import add
from z3 import *

def interval(a,b):
    return range(a,b+1)

pos_c = []
m_c = []
collisions_c = []

with open('foo.txt', 'r') as f:
    lines = f.readlines()
    print(lines)
    n,l = lines[0].split(',')
    n = int(n)
    l = int(l)
    print(n+l)

    r_x,r_y = lines[1].split(',')
    r_x = int(r_x)
    r_y = int(r_y)
    
    # e = [  [Bool("h_%s_%s" % (j, t)) for t in range(l+1) ] for j in range(n) ] 
    # print(e)
    h = [ [ [Bool("h_%s_%s_%s" % (i, j, t)) for t in range(l+1) ] for j in range(n) ] for i in range(n)]
    v = [ [ [ Bool("v_%s_%s_%s" % (i, j, t)) for t in range(l+1) ] for j in range(n) ] for i in range(n)]
    r = [ [ [ Bool("r_%s_%s_%s" % (i, j, t)) for t in range(l+1) ] for j in range(n) ] for i in range(n)]
    
    m = [ [ [ Bool("m_%s_%s_%s" % (i, j, t)) for t in range(l+1) ] for j in range(n) ] for i in range(n)]
    X = [ [ Bool("X_%s_%s" % (i, j)) for j in range(n) ] for i in range(n)]

    print(h)
    # print(h[0][2][1])

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

# m_c = [Implies(And(m[0][1][1],h[0][0][0],Not(h[0][1][0]),Not(v[2][0][0])),h[0][1][1])]
# pos_c.append(h[0][1][1]) winning clause
# print("m_c1", m_c)
winning_c = [Or([(r[r_x][n-2][t]) for t in range(0,l+1)] )]

print(winning_c)


                            #Moves

                    # if move, then pos change
#left move
for i in range(n):
    for j in interval(1,n-2): #both included
        for t in interval(1,l):
            m_c.append(Implies(And(m[i][j][t],h[i][j][t-1]), And(Not(h[i][j+1][t]), Not(h[i][j][t]), h[i][j-1][t])))
            m_c.append(Implies(And(m[i][j][t],r[i][j][t-1]), And(Not(r[i][j+1][t]), Not(r[i][j][t]), r[i][j-1][t])))
            # unchanged_c = []
            # for i1 in range(n):
            #     for j1 in range(n):
            #         if (i1,j1) != (i,j+1) and (i1,j1)!=(i,j) and (i1,j1)!=(i,j-1):
            #             # unchanged_c.append(And(Implies(h[i1][j1][t-1],h[i1][j1][t]) ,Implies(h[i1][j1][t],h[i1][j1][t-1])))        
            #             hz_same = And(Implies(h[i1][j1][t-1],h[i1][j1][t]) ,Implies(h[i1][j1][t],h[i1][j1][t-1]))
            #             vt_same = And(Implies(v[i1][j1][t-1],v[i1][j1][t]) ,Implies(v[i1][j1][t],v[i1][j1][t-1]))
            #             rd_same = And(Implies(r[i1][j1][t-1],r[i1][j1][t]) ,Implies(r[i1][j1][t],r[i1][j1][t-1]))
            #             unchanged_c.append(hz_same)        
            #             unchanged_c.append(vt_same)     
            #             unchanged_c.append(rd_same)           

            # v1_same = And(Implies(v[i][j-1][t-1],v[i][j-1][t]) ,Implies(v[i][j-1][t],v[i][j-1][t-1]))                            
            # v2_same = And(Implies(v[i][j+1][t-1],v[i][j+1][t]) ,Implies(v[i][j+1][t],v[i][j+1][t-1]))                            
            # v3_same = And(Implies(v[i][j][t-1],v[i][j][t]) ,Implies(v[i][j][t],v[i][j][t-1]))                            

            # r1_same = And(Implies(r[i][j-1][t-1],r[i][j-1][t]) ,Implies(r[i][j-1][t],r[i][j-1][t-1]))                            
            # r2_same = And(Implies(r[i][j+1][t-1],r[i][j+1][t]) ,Implies(r[i][j+1][t],r[i][j+1][t-1]))                            
            # r3_same = And(Implies(r[i][j][t-1],r[i][j][t]) ,Implies(r[i][j][t],r[i][j][t-1]))                            
            
            # h1_same = And(Implies(h[i][j-1][t-1],h[i][j-1][t]) ,Implies(h[i][j-1][t],h[i][j-1][t-1]))                            
            # h2_same = And(Implies(h[i][j+1][t-1],h[i][j+1][t]) ,Implies(h[i][j+1][t],h[i][j+1][t-1]))                            
            # h3_same = And(Implies(h[i][j][t-1],h[i][j][t]) ,Implies(h[i][j][t],h[i][j][t-1]))                            

            # unchanged_c.append(v1_same)
            # unchanged_c.append(v2_same)
            # unchanged_c.append(v3_same)               

            # h_unchanged_c = unchanged_c.copy()
            # r_unchanged_c = unchanged_c.copy()

            # h_unchanged_c.append(r1_same)
            # h_unchanged_c.append(r2_same)
            # h_unchanged_c.append(r3_same)

            # r_unchanged_c.append(h1_same)
            # r_unchanged_c.append(h2_same)
            # r_unchanged_c.append(h3_same)

            


# m_c.append(m[2][1][1])




#right move
for i in range(n):
    for j in interval(1,n-2): #both included
        for t in interval(1,l):
            m_c.append(Implies(And(m[i][j][t],h[i][j-1][t-1]), And(Not(h[i][j-1][t]), Not(h[i][j+1][t]), h[i][j][t])))
            m_c.append(Implies(And(m[i][j][t],r[i][j-1][t-1]), And(Not(r[i][j-1][t]), Not(r[i][j+1][t]), r[i][j][t])))
            # unchanged_c = []
            # for i1 in range(n):
            #     for j1 in range(n):
            #         if (i1,j1) != (i,j-1) and (i1,j1)!=(i,j+1) and (i1,j1)!=(i,j):
            #             hz_same = And(Implies(h[i1][j1][t-1],h[i1][j1][t]) ,Implies(h[i1][j1][t],h[i1][j1][t-1]))
            #             vt_same = And(Implies(v[i1][j1][t-1],v[i1][j1][t]) ,Implies(v[i1][j1][t],v[i1][j1][t-1]))
            #             rd_same = And(Implies(r[i1][j1][t-1],r[i1][j1][t]) ,Implies(r[i1][j1][t],r[i1][j1][t-1]))
            #             unchanged_c.append(hz_same)        
            #             unchanged_c.append(vt_same)        
            #             unchanged_c.append(rd_same)        
            
            # v1_same = And(Implies(v[i][j-1][t-1],v[i][j-1][t]) ,Implies(v[i][j-1][t],v[i][j-1][t-1]))                            
            # v2_same = And(Implies(v[i][j+1][t-1],v[i][j+1][t]) ,Implies(v[i][j+1][t],v[i][j+1][t-1]))                            
            # v3_same = And(Implies(v[i][j][t-1],v[i][j][t]) ,Implies(v[i][j][t],v[i][j][t-1]))                            


            # h1_same = And(Implies(h[i][j-1][t-1],h[i][j-1][t]) ,Implies(h[i][j-1][t],h[i][j-1][t-1]))                            
            # h2_same = And(Implies(h[i][j+1][t-1],h[i][j+1][t]) ,Implies(h[i][j+1][t],h[i][j+1][t-1]))                            
            # h3_same = And(Implies(h[i][j][t-1],h[i][j][t]) ,Implies(h[i][j][t],h[i][j][t-1]))                            

            # r1_same = And(Implies(r[i][j-1][t-1],r[i][j-1][t]) ,Implies(r[i][j-1][t],r[i][j-1][t-1]))                            
            # r2_same = And(Implies(r[i][j+1][t-1],r[i][j+1][t]) ,Implies(r[i][j+1][t],r[i][j+1][t-1]))                            
            # r3_same = And(Implies(r[i][j][t-1],r[i][j][t]) ,Implies(r[i][j][t],r[i][j][t-1]))                            

            # unchanged_c.append(v1_same)
            # unchanged_c.append(v2_same)
            # unchanged_c.append(v3_same)   

            # r_unchanged_c = unchanged_c.copy()
            # h_unchanged_c = unchanged_c.copy()

            # r_unchanged_c.append(h1_same)
            # r_unchanged_c.append(h2_same)
            # r_unchanged_c.append(h3_same)

            # h_unchanged_c.append(r1_same)
            # h_unchanged_c.append(r2_same)
            # h_unchanged_c.append(r3_same)

            

# m_c.append(m[2][1][1])
# for i in range(n)
#up move
for j in range(n):
    for i in interval(1,n-2): #both included
        for t in interval(1,l):
            m_c.append(Implies(And(m[i][j][t],v[i][j][t-1]), And(Not(v[i][j][t]), Not(v[i+1][j][t]), v[i-1][j][t])))
            # unchanged_c = []
            # for i1 in range(n):
            #     for j1 in range(n):
            #         if (i1,j1) != (i,j) and (i1,j1)!=(i+1,j) and (i1,j1)!=(i-1,j):
            #             # unchanged_c.append(And(Implies(v[i1][j1][t-1],v[i1][j1][t]) ,Implies(v[i1][j1][t],v[i1][j1][t-1])))        
            #             hz_same = And(Implies(h[i1][j1][t-1],h[i1][j1][t]) ,Implies(h[i1][j1][t],h[i1][j1][t-1]))
            #             vt_same = And(Implies(v[i1][j1][t-1],v[i1][j1][t]) ,Implies(v[i1][j1][t],v[i1][j1][t-1]))
            #             rd_same = And(Implies(r[i1][j1][t-1],r[i1][j1][t]) ,Implies(r[i1][j1][t],r[i1][j1][t-1]))
            #             unchanged_c.append(hz_same)        
            #             unchanged_c.append(vt_same)   
            #             unchanged_c.append(rd_same)   

            # h1_same = And(Implies(h[i-1][j][t-1],h[i-1][j][t]) ,Implies(h[i-1][j][t],h[i-1][j][t-1]))                            
            # h2_same = And(Implies(h[i+1][j][t-1],h[i+1][j][t]) ,Implies(h[i+1][j][t],h[i+1][j][t-1]))                            
            # h3_same = And(Implies(h[i][j][t-1],h[i][j][t]) ,Implies(h[i][j][t],h[i][j][t-1]))                    
            # r1_same = And(Implies(r[i-1][j][t-1],r[i-1][j][t]) ,Implies(r[i-1][j][t],r[i-1][j][t-1]))                            
            # r2_same = And(Implies(r[i+1][j][t-1],r[i+1][j][t]) ,Implies(r[i+1][j][t],r[i+1][j][t-1]))                            
            # r3_same = And(Implies(r[i][j][t-1],r[i][j][t]) ,Implies(r[i][j][t],r[i][j][t-1]))                            

            # unchanged_c.append(h1_same)
            # unchanged_c.append(h2_same)
            # unchanged_c.append(h3_same)
            # unchanged_c.append(r1_same)
            # unchanged_c.append(r2_same)
            # unchanged_c.append(r3_same)                                         

            


#down move
for j in range(n):
    for i in interval(1,n-2): #both included
        for t in interval(1,l):
            m_c.append(Implies(And(m[i][j][t],v[i-1][j][t-1]), And(Not(v[i-1][j][t]), Not(v[i+1][j][t]), v[i][j][t])))
            # unchanged_c = []
            # for i1 in range(n):
            #     for j1 in range(n):
            #         if (i1,j1) != (i-1,j) and (i1,j1)!=(i+1,j) and (i1,j1)!=(i,j):
            #             # unchanged_c.append(And(Implies(v[i1][j1][t-1],v[i1][j1][t]) ,Implies(v[i1][j1][t],v[i1][j1][t-1])))        
            #             hz_same = And(Implies(h[i1][j1][t-1],h[i1][j1][t]) ,Implies(h[i1][j1][t],h[i1][j1][t-1]))
            #             vt_same = And(Implies(v[i1][j1][t-1],v[i1][j1][t]) ,Implies(v[i1][j1][t],v[i1][j1][t-1]))
            #             rd_same = And(Implies(r[i1][j1][t-1],r[i1][j1][t]) ,Implies(r[i1][j1][t],r[i1][j1][t-1]))
            #             unchanged_c.append(hz_same)        
            #             unchanged_c.append(vt_same) 
            #             unchanged_c.append(rd_same) 

            # h1_same = And(Implies(h[i-1][j][t-1],h[i-1][j][t]) ,Implies(h[i-1][j][t],h[i-1][j][t-1]))                            
            # h2_same = And(Implies(h[i+1][j][t-1],h[i+1][j][t]) ,Implies(h[i+1][j][t],h[i+1][j][t-1]))                            
            # h3_same = And(Implies(h[i][j][t-1],h[i][j][t]) ,Implies(h[i][j][t],h[i][j][t-1]))                            

            # r1_same = And(Implies(r[i-1][j][t-1],r[i-1][j][t]) ,Implies(r[i-1][j][t],r[i-1][j][t-1]))                            
            # r2_same = And(Implies(r[i+1][j][t-1],r[i+1][j][t]) ,Implies(r[i+1][j][t],r[i+1][j][t-1]))                            
            # r3_same = And(Implies(r[i][j][t-1],r[i][j][t]) ,Implies(r[i][j][t],r[i][j][t-1]))                            

            # unchanged_c.append(h1_same)
            # unchanged_c.append(h2_same)
            # unchanged_c.append(h3_same)
            # unchanged_c.append(r1_same)
            # unchanged_c.append(r2_same)
            # unchanged_c.append(r3_same)                                                            

            


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

for i in range(n):
    for j in range(n):
        for t in interval(0,l):
            
            if (j<(n-1) and j>0 and t>0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j-1][t-1],h[i][j][t-1],h[i][j+1][t-1])))
                pos_c.append(Implies(h[i][j][t], Or(h[i][j-1][t+1],h[i][j][t+1],h[i][j+1][t+1])))

            if (j<(n-1) and j>0 and t==0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j-1][t+1],h[i][j][t+1],h[i][j+1][t+1])))

            if (j<(n-1) and j==0 and t>0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j][t-1],h[i][j+1][t-1])))
                pos_c.append(Implies(h[i][j][t], Or(h[i][j][t+1],h[i][j+1][t+1])))

            if (j<(n-1) and j==0 and t==0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j][t+1],h[i][j+1][t+1])))

            if (j==(n-1) and j>0 and t>0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j-1][t-1],h[i][j][t-1])))
                pos_c.append(Implies(h[i][j][t], Or(h[i][j-1][t+1],h[i][j][t+1])))

            if (j==(n-1) and j>0 and t==0 and t<l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j-1][t+1],h[i][j][t+1])))

            if (j<(n-1) and j>0 and t>0 and t==l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j-1][t-1],h[i][j][t-1],h[i][j+1][t-1])))

            if (j<(n-1) and j==0 and t>0 and t==l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j][t-1],h[i][j+1][t-1])))                

            if (j==(n-1) and j>0 and t>0 and t==l):
                pos_c.append(Implies(h[i][j][t], Or(h[i][j-1][t-1],h[i][j][t-1])))                


for i in range(n):
    for j in range(n):
        for t in interval(0,l):
            
            if (j<(n-1) and j>0 and t>0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j-1][t-1],r[i][j][t-1],r[i][j+1][t-1])))
                pos_c.append(Implies(r[i][j][t], Or(r[i][j-1][t+1],r[i][j][t+1],r[i][j+1][t+1])))

            if (j<(n-1) and j>0 and t==0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j-1][t+1],r[i][j][t+1],r[i][j+1][t+1])))

            if (j<(n-1) and j==0 and t>0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j][t-1],r[i][j+1][t-1])))
                pos_c.append(Implies(r[i][j][t], Or(r[i][j][t+1],r[i][j+1][t+1])))

            if (j<(n-1) and j==0 and t==0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j][t+1],r[i][j+1][t+1])))

            if (j==(n-1) and j>0 and t>0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j-1][t-1],r[i][j][t-1])))
                pos_c.append(Implies(r[i][j][t], Or(r[i][j-1][t+1],r[i][j][t+1])))

            if (j==(n-1) and j>0 and t==0 and t<l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j-1][t+1],r[i][j][t+1])))

            if (j<(n-1) and j>0 and t>0 and t==l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j-1][t-1],r[i][j][t-1],r[i][j+1][t-1])))

            if (j<(n-1) and j==0 and t>0 and t==l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j][t-1],r[i][j+1][t-1])))                

            if (j==(n-1) and j>0 and t>0 and t==l):
                pos_c.append(Implies(r[i][j][t], Or(r[i][j-1][t-1],r[i][j][t-1])))                



for i in range(n):
    for j in range(n):
        for t in interval(0,l):
            
            if (i<(n-1) and i>0 and t>0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(v[i-1][j][t-1],v[i][j][t-1],v[i+1][j][t-1])))
                pos_c.append(Implies(v[i][j][t], Or(v[i-1][j][t+1],v[i][j][t+1],v[i+1][j][t+1])))

            if (i<(n-1) and i>0 and t==0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(v[i-1][j][t+1],v[i][j][t+1],v[i+1][j][t+1])))

            if (i<(n-1) and i==0 and t>0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(v[i][j][t-1],v[i+1][j][t-1])))
                pos_c.append(Implies(v[i][j][t], Or(v[i][j][t+1],v[i+1][j][t+1])))

            if (i<(n-1) and i==0 and t==0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(v[i][j][t+1],v[i+1][j][t+1])))

            if (i==(n-1) and i>0 and t>0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(v[i-1][j][t-1],v[i][j][t-1])))
                pos_c.append(Implies(v[i][j][t], Or(v[i-1][j][t+1],v[i][j][t+1])))

            if (i==(n-1) and i>0 and t==0 and t<l):
                pos_c.append(Implies(v[i][j][t], Or(v[i-1][j][t+1],v[i][j][t+1])))

            if (i<(n-1) and i>0 and t>0 and t==l):
                pos_c.append(Implies(v[i][j][t], Or(v[i-1][j][t-1],v[i][j][t-1],v[i+1][j][t-1])))

            if (i<(n-1) and i==0 and t>0 and t==l):
                pos_c.append(Implies(v[i][j][t], Or(v[i][j][t-1],v[i+1][j][t-1])))                

            if (i==(n-1) and i>0 and t>0 and t==l):
                pos_c.append(Implies(v[i][j][t], Or(v[i-1][j][t-1],v[i][j][t-1])))                
                    
                    
                    
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

                        # Only move at a time

# for t in interval(1,l):
#     atleast_one_move  = []
#     for i in range(n):
#         for j in range(n):
#             atleast_one_move.append(m[i][j][t])
#     m_c.append(Or(atleast_one_move))





# PbEq()

for t in interval(1,l):
    list_of_tuples = []
    for i in range(n):
        for j in range(n):
            list_of_tuples.append((m[i][j][t],1))  
    m_c.append(z3.PbEq(list_of_tuples,1))


#Exactly 3 of the variables should be true
# print(m)


# #atmost 1
# for i in range(n):    
#     for j in range(n):
#         for t in interval(1,l):
#             for i1 in range(n):
#                 for j1 in range(n):
#                     if (i1,j1)!=(i,j): #not both true
#                         m_c.append(Not(And(m[i][j][t],m[i1][j1][t])))



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
            # collisions_c.append(Not(And(r[i][j-1][t], r[i][j][t])))

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


# m_c.append(m[1][2][1])
print("m_c", m_c)
print("pos_c", pos_c)
print("coll_c",collisions_c)

print(5*"\n")
s = Solver()
s.add(pos_c + m_c + collisions_c + winning_c)
# s.add( z3.PbEq(list_of_tuples, 1) )
if s.check() == sat:
    true_m = []
    true_h = []
    true_v = []
    true_r = []
    model = s.model()
    
    moves = []
    for t in range(l+1):
        for j in range(n):
            for i in range(n):
                # print(model.evaluate(m[i][j][t]))
                if model.evaluate(m[i][j][t])==True:
                    true_m.append("m"+str(i)+str(j)+str(t))
                    moves.append((i,j))
                if model.evaluate(v[i][j][t])==True:
                    true_v.append("v"+str(i)+str(j)+str(t))    
                if model.evaluate(h[i][j][t])==True:
                    true_h.append("h"+str(i)+str(j)+str(t))    
                if model.evaluate(r[i][j][t])==True:
                    true_r.append("r"+str(i)+str(j)+str(t))    

    print(true_m)
    print(true_h)
    print(true_v)
    print(true_r)

else:
    print("failed to solve")


    

with open("boo.txt","w") as f:
    for (a,b) in moves:
        add_text = str(a)+","+str(b)
        print(add_text, file = f)
    f.close()



# # # each cell contains a value in {1, ..., 9}
# cells_c  = [ And(1 <= X[i][j], X[i][j] <= 9)
#              for i in range(9) for j in range(9) ]
# print(cells_c)
# # each row contains a digit at most once
# rows_c   = [ Distinct(X[i]) for i in range(9) ]
# print(rows_c)

# # each column contains a digit at most once
# cols_c   = [ Distinct([ X[i][j] for i in range(9) ])
#              for j in range(9) ]

# print(cols_c)
# # each 3x3 square contains a digit at most once

# sq_c     = [ Distinct([ X[3*i0 + i][3*j0 + j]
#                         for i in range(3) for j in range(3) ])
#              for i0 in range(3) for j0 in range(3) ]

# print(sq_c)
# sudoku_c = cells_c + rows_c + cols_c + sq_c

# # sudoku instance, we use '0' for empty cells
# instance = ((0,0,0,0,9,4,0,3,0),
#             (0,0,0,5,1,0,0,0,7),
#             (0,8,9,0,0,0,0,4,0),
#             (0,0,0,0,0,0,2,0,8),
#             (0,6,0,2,0,1,0,5,0),
#             (1,0,2,0,0,0,0,0,0),
#             (0,7,0,0,0,0,5,2,0),
#             (9,0,0,0,6,5,0,0,0),
#             (0,4,0,9,7,0,0,0,0))

# instance_c = [ If(instance[i][j] == 0,
#                   True,
#                   X[i][j] == instance[i][j])
#                for i in range(9) for j in range(9) ]

# s = Solver()
# s.add(sudoku_c + instance_c)
# if s.check() == sat:
#     m = s.model()
#     r = [ [ m.evaluate(X[i][j]) for j in range(9) ]
#           for i in range(9) ]
#     print_matrix(r)
# else:
#     print("failed to solve")