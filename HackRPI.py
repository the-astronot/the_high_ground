import math
import HackRPI_data

def BFSNodeNode(G, s):
    n = len(G)
    pred = [ -1 for i in range(n)]
    order = [ 0 for i in range(n)]
    mark = [0 for i in range(n)] 
    Star = [s]
    pred[s] = s
    order[s] = 1
    mark[s] = 1
    k = 2
    
    while len(Star) > 0:
        i = Star.pop(0)
        for j in range(n):
            if G[i][j] == 1:
                if mark[j] == 0:
                    pred[j] = i
                    order[j] = k
                    k+= 1
                    mark[j] = 1
                    Star.append(j)
    
    return pred, order, Star


def PathCreator(pred, s, j):
    #Determines the path from source node s to node j using the predecessor array.
    Path = [j]
    node = j
    while node != s:
        Path.insert(0, pred[node])
        node = pred[node]
        
    return Path


def AugPath(G, U, s, t):
   
   #Applies the augmenting path algorithm to a network G, represented using a node-node adjancency matrix with arc capacities given by U and source node s and sink node t.  Throughout the algorithm, the residual network will be represented as a node-node adjancency matrix since it is easier to remove arcs from this representation.
    
    n = len(G)
    RG = [ [0 for i in range(n)] for i in range(n)]   #node-node adjancency matrix of the residual network
    RU = [ [0 for i in range(n)] for i in range(n)]  #residual capacities 
    
    for i in range(n):  #Initialization of residual network
        for j in range(n):
            if G[i][j] == 1:    #If arc (i, j) exists, then update its residual capacity
                RU[i][j] = U[i][j]
                if RU[i][j] > 0:
                    RG[i][j] = 1    #If arc (i, j) has positive residual capacity, put it in the residual network.
                    
    vstar = 0
    pred, order = BFSNodeNode(RG, s)  #if pred[t] >=0, then there is an s-t path.
    
    while pred[t] > -1:
        P = PathCreator(pred, s, t)  #Get path
        print(P)
        delta = math.inf
        for i in range(len(P)-1):  #Finds the minimum residual capacatiy.  The arc (P[i], P[i+1]) is in the path for all i < len(P)-1
            if RU[P[i]][P[i+1]] < delta:
                delta = RU[P[i]][P[i+1]]
        vstar += delta  #Increase delta
        for i in range(len(P)-1):   #Scan all arcs in the path and update their residual capacities and their backward arcs' residual capacities
            RU[P[i+1]][P[i]] += delta   #Updating backwards arc's residual capacities
            RG[P[i+1]][P[i]] = 1
            RU[P[i]][P[i+1]] -= delta  #Forward arc's turn
            if RU[P[i]][P[i+1]] == 0:   #Remove arc's whose residual capacity drops to zero.
                RG[P[i]][P[i+1]] = 0
        pred, order = BFSNodeNode(RG, s)  #Run search on updated residual network.  
    
    return pred, order

    
def MinTimeMaxFlow(G, U, S, s, t, P):
    n = len(G)
    pplz = 0
    T = 1
    while pplz <= P:
        for i in range(n):
            for j in range(n):
                if G[i][j] == 1:
                    T += S[i][j] #get time
                    P -= U[i][j]
    return T
    
    GT, UT = NodeyNodes(G, U, S, T)
    vstar = AugPath(GT, UT, s, t)
    return vstar


if __name__ == '__main__':
    s = 0
    G = HackRPI_data.G
    S = HackRPI_data.S
    U = HackRPI_data.U
    (pred, order, Star) = BFSNodeNode(G, 0)
    #MinTimeMaxFlow(G, U, S, s, t, 100)
    #pred, order = AugPath(GT, UT, 1, 19)
    Path=PathCreator(pred, s, 18)
    print(Path)

