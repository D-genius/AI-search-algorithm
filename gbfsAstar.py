import operator;

"""The Environment"""
class Environment(object):
    mygraph = { "1" : set(["2","4"]),
                "2" : set(["1","3","5"]),
                "3" : set(["2", "6" ]),
                "4" : set(["1","5","7"]),
                "5" : set(["2","4","6","8"]),
                "6" : set(["3","5","9"]),
                "7" : set(["4","8"]),
                "8" : set(["7","5","9"]),
                "9" : set(["8","6"]),
               } 

    #keys in a string should be stings and unique
    #cost is not unique hence becomes the value
    cost ={     str(["1","2"]): "3",   str(["1", "4"]):"5",
                str(["2","1" ]): "3",  str(["2","3"]):"5",   str(["2","5"]):"7",
                str(["3","2"]): "5",   str(["3","6"]):"9",
                str(["4","1" ]): "5",  str(["4","5"]): "9",  str(["4","7"]):"11",
                str(["5","2" ]): "7",  str(["5","4"]):"9",   str(["5","6"]):"11" , str(["5","8"]) :"13",
                str(["6","3" ]): "9",  str(["6","5"]): "11", str(["6","9"]): "15",
                str(["7","4"]): "11",  str(["7","8"]): "15", str(["8","7" ]):"15",
                str(["8","5"]): "13",  str(["8","9"]):"17" ,
                str(["9","8"]): "17",  str(["9","6"]):"15"
               } 

    myHeuristics={ "1":["1","3"],
                   "2":["2","3"],
                   "3":["3","3"],
                   "4":["1","2"],
                   "5":["2","2"],
                   "6":["3","2"],
                   "7":["1","1"],
                   "8":["2","1"],
                   "9":["3","1"],

    }
    State="2"
    Goal="9"

"""Agent Behaviour"""
#Depth First Search
class Agent(Environment):
 def dfs(graph, start, goal):
    stack = [(start, [start])]
    p=[]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                p.append(path + [next])
            else:
               stack.append((next, path + [next]))
    return p 

 #Breadth First Search
 def bfs(graph, start, goal):
    queue = [(start, [start])]
    p=[]
    while queue:
        (vertex, path) = queue.pop(0)
        #poping 0 make it a queue
        for next in graph[vertex] - set(path):
            if next == goal:
                p.append(path + [next])
                return p 
                #first path returned by bfs is the shortest path
                #we dont need to check the rest
            else:
                queue.append((next, path + [next]))
    return p 

 def getcost(pathToCost):
    i=0
    pathcost=0
    while i<len(pathToCost)-1:
        #extract 2 neighbors in path
        l=[]
        l.append(pathToCost[i])
        l.append(pathToCost[i+1])
        #read and add cost of neighbors to pathcost
        pathcost=pathcost+int(Environment.cost[str(l)])
        i+=1
    #return final path cost
    return pathcost
 def getheur(vertex,goal):
    v=[]
    g=[]
    for i in Environment.myHeuristics[vertex]:
        v.append(int(i))
    for i in Environment.myHeuristics[goal]:
        g.append(int(i))
    heuristic = abs(v[0]-g[0]) + abs(v[1]-g[1])
    return heuristic

 def ucs(graph, start, goal):
    stack = [(start, [start])]
    p=[]
    leastcost=1000 #max cost limit

    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                #paths identified by dfs techniques: path+ [next]
                pathcost=Agent.getcost(path+ [next])
                print("UCS path ",path+ [next]," pathcost ",pathcost)
                 #update least cost & least cost path
                if pathcost<leastcost:
                    leastcost=pathcost
                    p=path + [next]
            else:
               stack.append((next, path + [next]))
    return p

 def gbfs(graph,start, goal):
    p=[]
    p.append(start)
    while True:
        neighbour = graph[start]
        heur={}
        for i in neighbour.difference(p):
            heur[i] = Agent.getheur(i,goal)
            sorted_heur = sorted(heur.items(), key=operator.itemgetter(1))
            x=next(iter(sorted_heur[0]))
            p.append(x)
        if x == goal:
            return p 
        else:
            start=x

 def A_Star(graph,start, goal):
    p=[]
    
    p.append(start)
    while True:
        neighbour = graph[start]
        heur={}
        for i in neighbour.difference(p):
            l=[]
            l.append(str(start))
            l.append(str(i))
            heur[i] = Agent.getheur(i,goal)+Agent.getcost(l)
            sorted_heur = sorted(heur.items(), key=operator.itemgetter(1))
            x=next(iter(sorted_heur[0]))
            p.append(x)
        if x == goal:
            return p 
        else:
            start=x


 def hcs(graph, start, goal):
    stack = [(start, [start])]
    p=[]
    p.append(start)
    leastcost=0
    while True:
        neighbour = graph[start]
        cost={}
        for i in neighbour.difference(p):
            l=[]
            l.append(str(start))
            l.append(str(i))
            cost[i] = Agent.getcost(l)
            
            #initialize leastcost to first cost
            if leastcost==0:
                leastcost=cost[i]
            print("Path tested and cost",l,cost[i])
        sorted_cost = sorted(cost.items(), key=operator.itemgetter(0))
        x=next(iter(sorted_cost[0]))
        print("Selected path", x)
        #append paths for increasing value only or stop search
        if int(x)<leastcost:
                leastcost=int(Environment.cost[str(l)])
                p.append(x)
        else:
                break
        if x == goal:
            return p 
        else:
            start=x



 def __init__(self, Environment):
    print("DFS-Paths Available")
    print(Agent.dfs(Environment.mygraph,Environment.State, Environment.Goal)) 
    # returns all possible routes
    print("BFS-Shortest Path")
    print(Agent.bfs(Environment.mygraph,Environment.State, Environment.Goal)) 
    # returns shortest routes
    print("UCS-Cheapest Paths")
    print(Agent.ucs(Environment.mygraph,Environment.State, Environment.Goal)) 
    # returns cheapest routes
    print("GBFS-Best Heuristic Paths")
    print(Agent.gbfs(Environment.mygraph,Environment.State, Environment.Goal)) 
    # returns cheapest routes
    print("A-star Best Heuristic Paths")
    print(Agent.A_Star(Environment.mygraph,Environment.State, Environment.Goal)) 
    # returns cheapest routes
    print("Hill Climb search Paths")
    print(Agent.hcs(Environment.mygraph,Environment.State, Environment.Goal)) 
    # returns cheapest routes

    """Create the agent"""
theEnvironment = Environment()
theAgent= Agent(theEnvironment)