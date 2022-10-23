#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

f = open('testdata.json')
data = json.load(f)
response_answer =   [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
                     [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
                     [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
                     [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

response_weights =  [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
                     [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
                     [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
                     [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
counter = 0
for user in data['users']:
    #print(user['responses'])
    for i in range(0, len(user['responses'])):
        #print(user['responses'][i])
        if user['responses'][i] == 0:
            response_answer[i][0] += 1
        elif user['responses'][i] == 1:
            response_answer[i][1] += 1
        elif user['responses'][i] == 2:
            response_answer[i][2] += 1
        elif user['responses'][i] == 3:
            response_answer[i][3] += 1
        elif user['responses'][i] == 4:
            response_answer[i][4] += 1
        else:
            response_answer[i][5] += 1
    #print(response_answer)
    counter += 1
#print(response_answer)

for i in range(0, len(response_answer)):
    res_sum = 0.0
    for j in range(0, 6):
        res_sum += response_answer[i][j]
    for k in range(0, 6):
        #print(res_sum)
        response_weights[i][k] = response_answer[i][k] / res_sum



# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2, res_weights):
    overall_score = 0.0

    if user2.gender == user1.preferences[0] and user1.gender == user2.preferences[0]:
        overall_score += .1
    elif user1.gender == user2.preferences[0] and user2.gender != user1.preferences[0]:
        overall_score += .05
    elif user2.gender == user1.preferences[0] and user1.gender != user2.preferences[0]:
        overall_score += .05
    
    if user1.grad_year == user2.grad_year and user1.gender == user2.gender:
        overall_score += .1
    elif user1.grad_year == user2.grad_year and user1.gender != user2.gender:
        overall_score += .15
    elif user1.grad_year - user2.grad_year == 1 and user1.gender == "M" and user2.gender == "F":
        overall_score += .1
    elif user1.grad_year - user2.grad_year == 2 and user1.gender == "M" and user2.gender == "F":
        overall_score += .05
    elif user1.grad_year - user2.grad_year == 1 and user1.gender == "F" and user2.gender == "M":
        overall_score += .12
    elif user1.grad_year - user2.grad_year == 2 and user1.gender == "F" and user2.gender == "M":
        overall_score += .08

    counter = 0
    for i in range(0, len(user1.responses) - 1):
        if user1.responses[i] == user2.responses[i]:
            if i == 0:
                overall_score += (2.5 * res_weights[i][user1.responses[i]])
    overall_score += counter * 1
    return overall_score

if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2, response_weights)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
