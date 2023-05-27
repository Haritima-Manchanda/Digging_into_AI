import random

MAX_ITER = 10000
START_INDEX = 13
EPSILON = 0.5
GAMMA = 0.1
ALPHA = 0.3
    
class BoardBox:
    def __init__(self, box_type, box_index, box_q_values, box_row, box_column, box_reward):
        self.box_type = box_type
        self.box_index = box_index
        self.box_q_values = box_q_values
        self.box_row = box_row
        self.box_column = box_column
        self.box_reward = box_reward
        
    def __str__ (self):
        return 'Box(box_type=' + str(self.box_type) + ' ,box_index=' + str(self.box_index) + ', box_q_values=' + str(self.box_q_values)+ ', box_row='+ str(self.box_row)+ ', box_column='+ str(self.box_column)+ ', box_reward= ' + str(self.box_reward) + ' )'
    
    def get_box_type(self):
        return self.box_type
    
    def get_box_index(self):
        return self.box_index
    
    def get_box_q_values(self):
        return self.box_q_values
    
    def get_box_row(self):
        return self.box_row
    
    def get_box_column(self):
        return self.box_column
    
    def set_box_type(self, box_type):
        self.box_type = box_type
    
    def set_box_q_value(self, q_value_index, q_value):
        self.box_q_value[q_value_index] = q_value
    
    def set_box_reward(self, box_reward):
        self.box_reward = box_reward
    
def get_board_index_from_box_index(box_index: int) ->int:
    if(box_index == 13 or box_index == 14 or box_index == 15 or box_index == 16):
        return box_index - 13
    elif(box_index == 9 or box_index == 10 or box_index == 11 or box_index == 12):
        return box_index - 5
    elif(box_index == 5 or box_index == 6 or box_index == 7 or box_index == 8):
        return box_index + 3
    elif(box_index == 1 or box_index == 2 or box_index == 3 or box_index == 4):
        return box_index + 11

board = []
index_count = temp = 16
row_index = 0
for i in range(4):
    board_row = []
    index_count = temp
    for j in range(4):
        box = BoardBox("NORMAL", index_count - 3, [0.0, 0.0, 0.0, 0.0], row_index, j, -0.1)
        board.append(box)
        index_count = index_count + 1
    temp = temp - 4
    row_index = row_index + 1

input_string = input()
input_string_splitted = input_string.split(' ')

goal_state_1 = int(input_string_splitted[0])
goal_state_2= int(input_string_splitted[1])
forbidden_state = int(input_string_splitted[2])
wall_state = int(input_string_splitted[3])


goal_state_1_index = get_board_index_from_box_index(goal_state_1)
goal_state_2_index = get_board_index_from_box_index(goal_state_2)
wall_index = get_board_index_from_box_index(wall_state)
forbidden_state_index = get_board_index_from_box_index(forbidden_state)


board[goal_state_1_index].set_box_type("GOAL")
board[goal_state_1_index].set_box_reward(100.0)
board[goal_state_2_index].set_box_type("GOAL")
board[goal_state_2_index].set_box_reward(100.0)
board[wall_index].set_box_type("WALL")
board[forbidden_state_index].set_box_type("FORBIDDEN")
board[forbidden_state_index].set_box_reward(-100.0)
    
def change_position_of_agent(action_index, current_box):
    '''action_index is either 0: up, 1: down, 2: left, 3: right'''
    temp = current_box.box_index
    new_box_index = current_box.box_index
    
    
    if(action_index == 0 and current_box.box_row > 0):
        new_box_index = current_box.box_index + 4
    elif(action_index == 1 and current_box.box_row < 3):
        new_box_index = current_box.box_index - 4
    elif(action_index == 2 and current_box.box_column > 0):
        new_box_index = current_box.box_index - 1
    elif(action_index == 3 and current_box.box_column < 3):
        new_box_index = current_box.box_index + 1
    
    if(get_board_index_from_box_index(new_box_index) == wall_index):
        new_box_index = temp
    return get_board_index_from_box_index(new_box_index)
    
    
    
def update_q_value_of_current_box(current_box, action_index, next_position_box):
    return (((1-ALPHA) * current_box.box_q_values[action_index]) + ALPHA * (next_position_box.box_reward + GAMMA * max(next_position_box.box_q_values)))
 

def tie_breaker(q_values_list):
    q_values_up = q_values_list[0]
    q_values_down = q_values_list[1]
    q_values_left = q_values_list[2]
    q_values_right = q_values_list[3]
    
    maximum = float("-inf")
    for i in range(len(q_values_list)):
        if(q_values_list[i] > maximum):
            maximum = q_values_list[i]
    
    if maximum == q_values_up:
        return 0
    elif(maximum == q_values_right):
        if(q_values_right == q_values_up):
            return 0
        return 3
    elif(maximum == q_values_down):
        if(q_values_down == q_values_up):
            return 0
        elif(q_values_down == q_values_right):
            return 3
        return 1
    elif(maximum == q_values_left):
        if(q_values_left == q_values_up):
            return 0
        elif(q_values_left == q_values_right):
            return 3
        elif(q_values_left == q_values_down):
            return 1
        return 2
    
    
 
current = board[START_INDEX]
iterations = 0
action_index = -1
temp_board = board



while iterations <= MAX_ITER:
    board = temp_board
    while not(current.box_type == 'GOAL' or current.box_type == 'FORBIDDEN'):
        if EPSILON > random.random():
            action_index = random.randint(0,3)
        else:
            action_index = current.box_q_values.index(max(current.box_q_values))
            
        next_position_box = board[change_position_of_agent(action_index, current)]
            
        current.box_q_values[action_index] = update_q_value_of_current_box(current, action_index, next_position_box)
        
        if next_position_box.box_type != 'WALL':
            current = next_position_box
        
    current = temp_board[START_INDEX]
    iterations = iterations + 1



actions = {0: "up", 1: "down", 2: "left", 3: "right"}
policy_dict = {}


if (len(input_string_splitted) == 5 and input_string_splitted[-1] == 'p'):
    for i in range(16):
        policy_dict[board[i].box_index] = actions[tie_breaker(board[i].box_q_values)]
        
    policy_dict[goal_state_1] = 'goal'
    policy_dict[goal_state_2] = 'goal'
    policy_dict[wall_state] = 'wall-square'
    policy_dict[forbidden_state] = 'forbid'
    
    for i in sorted (policy_dict.keys()) :
        print(i, policy_dict[i])
        

elif(len(input_string_splitted) == 6 and input_string_splitted[-2] == 'q'):
    n = int(input_string_splitted[-1])
    given_index_q_values = board[get_board_index_from_box_index(n)].box_q_values
    print("up ", round(given_index_q_values[0], 2))
    print("right ", round(given_index_q_values[3], 2))
    print("down ", round(given_index_q_values[1], 2))
    print("left ", round(given_index_q_values[2], 2))
