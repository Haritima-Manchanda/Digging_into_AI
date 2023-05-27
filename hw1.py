from queue import Queue
import math
import json

def calculateCost(str1: str, str2: str) ->int:
    # “4w1b2w3b” to “2b1w4b3b” is equal to 3
    # We find the count by which the first number is shifted.
    # So for example, in str1 the first digit that is 4 is at intially
    # position = 1 (in comparison to other digits),
    # and in str2 it is at position 3. So cost = second pos - first pos + 1
    # since we always find the position by which the first digit is shifted, first pos is always 1
    # So cost = second pos
    cost = 1
    digitAtFirstPos = str1[0]
    
    for i in range(0, len(str2), 2):
        if str2[i] == digitAtFirstPos:
            break
        cost = cost + 1
    return cost

def heuristicFunction(str1: str) -> int:
    goal = "1w2w3w4w"
    heuristic = 0
    
    for i in range(0, len(str1), 2):
        if str1[i] != goal[i]:
            if(int(str1[i]) > heuristic):
                heuristic = int(str1[i])
    return heuristic

def generateChildNodes(arr: str, i: int, childlist: list) -> list:
    end = i+1
    newarr = ""
    
    for start in range(0, end+1):
        if arr[start].isdigit():
            newarr = newarr + arr[start]
        else:
            if(arr[start] == 'w'):
                newarr = newarr + 'b'
            else:
                newarr = newarr + 'w'
                
    for start in range(end+1, len(arr)):
        newarr = newarr + arr[start]
    
    end = i
    temp = end
    finalarr = ""
    
    while end>=0 :
        if newarr[end].isdigit():
            finalarr = finalarr + newarr[end]
            finalarr = finalarr + newarr[end+1]
        end = end - 2
    
    for start in range(temp+2, len(arr)):
        finalarr = finalarr + newarr[start]
       
    childlist.append(finalarr)
    return childlist

def expand(parent: str) -> list:
    childlist = []
    
    for i in range(0, len(parent), 2):
        childlist = generateChildNodes(parent, i, childlist)
    
    return childlist

def tie(listEqual: list) -> str:
    ids = []
    id1 = ""
    for str1 in listEqual:
        id1 = ""
        for i in range(0, len(str1)):
            if(str1[i].isdigit()):
                id1 = id1 + str1[i]
            else:
                if(str1[i] == 'w'):
                    id1 = id1 + '1'
                else:
                    id1 = id1 + '0'
        ids.append(id1)

    maximum = math.inf
    
    for string in ids:
        if (int(string) < maximum):
            maximum = int(string)
    
    str2 = ""
    for string in ids:
        if (int(string) == maximum):
            for j in range(0, len(string)):
                if j%2 == 0:
                    str2 = str2 + string[j]
                else:
                    if string[j] == '1':
                        str2 = str2 + 'w'
                    else:
                        str2 = str2 + 'b'
    return str2
    

def findLeastF(nodes: dict) -> str:
    minimum = math.inf
    equalFCostNodes = []

    for node in nodes:
        if nodes[node]['f'] <= minimum :
            minimum = nodes[node]['f']
      
    for node in nodes.keys():
        if nodes[node]['f'] == minimum:
            equalFCostNodes.append(node)
    
    if len(equalFCostNodes) == 1:
        return equalFCostNodes[0]    
    
    string = tie(equalFCostNodes)
    return string
        
def graphSearchBFS(problem : str):
    finalSol = "1w2w3w4w"
    frontier = Queue()     # a queue initially containing one path, for the problem's initial state
    frontier.put(problem)
    reached = {}           # a table of {state: True/False}; initially empty
    reached[problem] = True
    solution = ""          # initially assigned to failure
    parent = {}            # to keep track of parent of a node
    parent[problem] = None
    
    while not frontier.empty():
        u = frontier.get() # some node that we choose to remove from frontier, in this case the leftmost or the first node
        
        for child in expand(u):
            if child not in reached:
                reached[child] = True
                parent[child] = u
                frontier.put(child)
                if child == finalSol:
                    solution = solution + child
    path = []
    while solution!=None:
        path.append(solution)
        solution = parent[solution]
        
    pathFlip = []
    pathFlip.append(path[0])
    
    for i in range(0, len(path)-1, 1):
        string = path[i]
        
        digitAtFirstPosition = string[0]
        flipIndex = 0
        
        string2 = path[i+1]
        for j in range(0, len(string2), 2):
            if string2[j] == digitAtFirstPosition:
                flipIndex = j+2
                break
        newString = ""
        
        if flipIndex == 8:
            newString = newString + string2
            newString += '|'
            pathFlip.append(newString)
            continue
        
        for j in range(0, len(string2), 1):
            if(j == flipIndex -1):
                newString += string2[j]
                newString += '|'
            else:
                newString += string2[j]
                
        pathFlip.append(newString)
        
    # printing the nodes that lead to the path
    for i in range(len(pathFlip)-1, -1, -1):
        print(pathFlip[i])
        
def graphSearchA(problem : str) ->str:
    reached = {}
    fringe = {}
    parent = {}
    finalSol = "1w2w3w4w"
    solution = None
    fringe[problem] = {'g' : 0, 'h' : 0, 'f' : 0}
    parent[problem] = None
    
    while fringe:
        node = findLeastF(fringe)
        nodeValue = fringe.pop(node)
        
        reached[node] = nodeValue
        for child in expand(node):
            gCost = nodeValue['g'] + calculateCost(node, child)
            hCost = heuristicFunction(child)
            fCost = hCost + gCost
            
            childValue = {'g' : gCost, 'h' : hCost, 'f' : fCost}
            
            if child == finalSol:
                solution = child
                reached[child] = childValue
                parent[child] = node
                break
            
            if child not in fringe and child not in reached:
                parent[child] = node
                fringe[child] = childValue
                
            elif child in fringe and fringe[child]['f'] > fCost:
                parent[child] = node
                fringe[child] = childValue
                
            elif child in reached and reached[child]['g'] > gCost:
                reached.pop(child)
                parent[child] = node
                fringe[child] = childValue
                
        if solution != None:
            break
                
    '''path = []
    while solution!= None:
        path.append(solution)
        solution = parent[solution]'''
    
    path = []
    while solution!=None:
        path.append(solution)
        solution = parent[solution]
        
    pathFlip = []
    pathFlip.append(path[0])
    
    for i in range(0, len(path)-1, 1):
        string = path[i]
        
        digitAtFirstPosition = string[0]
        flipIndex = 0
        
        string2 = path[i+1]
        for j in range(0, len(string2), 2):
            if string2[j] == digitAtFirstPosition:
                flipIndex = j+2
                break
        newString = ""
        
        if flipIndex == 8:
            newString = newString + string2
            newString += '|'
            pathFlip.append(newString)
            continue
        
        for j in range(0, len(string2), 1):
            if(j == flipIndex -1):
                newString += string2[j]
                newString += '|'
            else:
                newString += string2[j]
                
        pathFlip.append(newString)
        
    # printing the nodes that lead to the path
    for i in range(len(pathFlip)-1, -1, -1):
        print(pathFlip[i] + ' ' + 'g:' + json.dumps(reached[path[i]]['g']) + ' h:' + json.dumps(reached[path[i]]['h']))
        
                
def main():
    '''
    inputarr = input("Enter the starting state of the problem: ")
        
    length = len(inputarr)
    inputstr = ""
    if(inputarr[length - 1] == 'a'):
        inputstr += inputarr[:length-2]
        graphSearchA(inputstr)
        
    elif(inputarr[length - 1] == 'b'):
        inputstr += inputarr[:length-2]
        graphSearchBFS(inputstr)'''
    set1 = ('i1', 'i2', 'i3')
    set2 = ('i2', 'i1', 'i3')
    # Check if two list of tuples are identical
    # using cmp()
    res = not cmp(test_list1, test_list2)
  
# printing result
    print("Are tuple lists identical ? : " + str(res))
if __name__ == "__main__":
    main()

