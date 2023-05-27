MAX, MIN = 1000, -1000
nodeIndexExplored = set()

def minimax(depth, nodeIndex, maximizingPlayer, values, alpha, beta):
    if depth == 3:
        nodeIndexExplored.add(nodeIndex)
        return values[nodeIndex]
    
    if maximizingPlayer and depth == 0:
        best = MIN
    
        for i in range(0, 3):
            val = minimax(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)

            if beta <= alpha:
                break
            
        return best

    elif (maximizingPlayer and depth != 0):
        best = MIN
    
        for i in range(0, 2):
            val = minimax(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)

            if beta <= alpha:
                break
            
        return best
    
    else:
        best = MAX
        
        for i in range(0, 2):
            val = minimax(depth + 1, nodeIndex * 2 + i, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)

            if beta <= alpha:
                break
            
        return best
    
if __name__ == "__main__":
    nums = input("Enter 12 numbers separated by space which will correspond to the 12 terminal nodes of the tree from left to right: ")
    list_nums = nums.split(" ")
    values = list(map(lambda x: int(x), list_nums))
    indices = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
    minimax(0, 0, True, values, MIN, MAX)
    nodeIndexPruned = list(indices.difference(nodeIndexExplored))
    nodeIndexPruned.sort()
    
    for i in range(0, len(nodeIndexPruned)):
        print(nodeIndexPruned[i], end = ' ')
    
    
    
    