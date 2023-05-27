import numpy as np
import math

def binary_perceptron(inputs: list) -> None:    
    input_feature_list = []
    true_y_list = []
    for i in range(len(inputs)):
        temp =[]
        temp.append(inputs[i][0])
        temp.append(inputs[i][1])
        input_feature_list.append(temp)
        true_y_list.append(inputs[i][2])
        
    weight_matrix = [0.0, 0.0]
    
    for i in range(100): 
        for j in range(len(inputs)):
            feature_matrix = np.array(input_feature_list[j])
            classifier_value = np.dot(feature_matrix, weight_matrix)        
            y = 0
            
            if(classifier_value >= 0):
                y = +1
            else:
                y = -1
                
            if(y != true_y_list[j]):
                weight_matrix =  weight_matrix + np.dot(true_y_list[j], feature_matrix)
                
    print(round(weight_matrix[0],2), ",", round(weight_matrix[1],2))

def sigmoid(x):
    s=1/(1+math.pow(math.e, -x))
    return s

def logistic_regression(inputs: list) -> None:
    alpha = 0.1
        
    input_feature_list = []
    true_y_list = []
    
    for i in range(len(inputs)):
        temp =[]
        temp.append(inputs[i][0])
        temp.append(inputs[i][1])
        input_feature_list.append(temp)
        if(inputs[i][2] == -1):
            true_y_list.append(0)
        else:
            true_y_list.append(inputs[i][2])
        
    weight_matrix = [0.0, 0.0]
    w1 = weight_matrix[0]
    w2 = weight_matrix[1]
    P = [] # a list that holds the probability values computed by the logistic regression
    
    for i in range(100): 
        for j in range(len(inputs)):
            item = input_feature_list[j]

            z = w1 * item[0] + w2 * item[1]
            p = sigmoid(z)
            
            w1 = w1 + alpha * item[0] * (true_y_list[j] - p)
            w2 = w2 + alpha * item[1] * (true_y_list[j] - p)
            
    for j in range(len(inputs)):
        item = input_feature_list[j]
        z = w1 * item[0] + w2 * item[1]
        p = sigmoid(z)
        P.append(round(p,2))
    
    for i in range(len(P)):
        print(P[i], end = ' ')
        
def main():
    input_from_user = input()
    perceptron_or_logistic_type = input_from_user[0]
    my_string = input_from_user[2:]
    input_tuples_list = list(eval(my_string.replace(") (", "),(")))
    
    if(perceptron_or_logistic_type == 'P'):
        binary_perceptron(input_tuples_list)
    else:
        logistic_regression(input_tuples_list)
    

if __name__ == "__main__":
    main()
