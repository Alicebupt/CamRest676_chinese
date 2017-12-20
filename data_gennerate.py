import json
import random

def get_user_goal(data):
    user_goal_set = {}
    index = 0
    user_goal = {'diaact':'', 'inform_slots':{}, 'request_slots':{}}
    for i in range(len(data)):
        dialog = data[i]
        goal = dialog['goal']
        user_goal['diaact'] = 'request'
        if goal['constraints'] != []:
            for j in range(len(goal['constraints'])):
               user_goal['inform_slots'][goal['constraints'][j][0]] = goal['constraints'][j][1]
        else:
            pass
        if goal['request-slots'] != []:
            for k in range(len(goal['request-slots'])):
               user_goal['request_slots'][goal['request-slots'][k]] = 'UNK'
        else:
            pass
        user_goal_set[index] = user_goal
        index += 1
        # print(user_goal)
    with open('goal_set.json', 'w') as f:
        f.write(json.dumps(user_goal_set))

def get_acts(data):
    act_set = []
    for i in range(len(data)):
        dial = data[i]['dial']
        for j in range(len(dial)):
            acts = dial[j]['usr']['slu']
            for k in range(len(acts)):
                act = acts[k]['act']
                if act not in act_set:
                    act_set.append(act)
                else:
                    pass
    return act_set

def get_restdic(db):
    add_set = []
    area_set = []
    food_set = []
    location_set = []
    phone_set = []
    pri_set = []
    post_set = []
    type_set = []
    id_set = []
    name_set = []
    dict = {}
    for i in range(len(db)):
        ticket = db[i]
        add_set.append(db[i]['address'])
        area_set.append(db[i]['area'])
        if 'food' in db[i].keys():
            food_set.append(db[i]['food'])
        location_set.append(db[i]['location'])
        if 'phone' in db[i].keys():
            phone_set.append(db[i]['phone'])
        pri_set.append(db[i]['pricerange'])
        post_set.append(db[i]['postcode'])
        type_set.append(db[i]['type'])
        id_set.append(db[i]['id'])
        name_set.append(db[i]['name'])
    add_set = list(set(add_set))
    area_set = list(set(area_set))
    food_set = list(set(food_set))
    location_set = list(set(location_set))
    phone_set = list(set(phone_set))
    pri_set = list(set(pri_set))
    post_set = list(set(post_set))
    type_set = list(set(type_set))
    id_set = list(set(id_set))
    name_set = list(set(name_set))
    dict['address'] = add_set
    dict['area'] = area_set
    dict['food'] = food_set
    dict['location'] = location_set
    dict['phone'] = phone_set
    dict['pricerange'] = pri_set
    dict['postcode'] = post_set
    dict['type'] = type_set
    dict['id'] = id_set
    dict['name'] = name_set
    with open('CamRestOTGY.json','w') as fr:
        fr.write(json.dumps(dict))

'''
if __name__ == '__main__':

    # with open('CamRest676.json') as f:
    #    data = json.load(f)
    # get_user_goal(data)
    # act_set = get_acts(data)
    # print(act_set)

    with open('CamRestDB.json') as f:
        db = json.load(f)
    # get_restdic(db)

    with open('CamRestOTGY.json') as f:
        data = json.load(f)
    # goal = {'inform_slots':{}}
    count = 0
    goal_set = {}
    index = 0
    for i in range(50):
        goal = {'inform_slots': {}}
        goal['diaact'] = 'request'
        goal['request_slots'] = {'name': 'UNK'}
        goal['inform_slots']['pricerange'] = random.choice(data['pricerange'])
        goal['inform_slots']['area'] = random.choice(data['area'])
        goal['inform_slots']['food'] = random.choice(data['food'])
        print(goal)
        # print(goal_set)
        goal_set[i] = goal
        for j in range(len(db)):
            if 'pricerange' in db[j].keys() and 'food' in db[j].keys() and 'area' in db[j].keys():
                if db[j]['pricerange'] == goal['inform_slots']['pricerange'] and db[j]['area'] == goal['inform_slots']['area'] and db[j]['food'] == goal['inform_slots']['food']:
                    count += 1
    print(count)
    for i in range(100):
        ticket = random.choice(db)
        goal = {'inform_slots': {}}
        goal['diaact'] = 'request'
        goal['request_slots'] = {'name': 'UNK', 'address': 'UNK'}
        goal['inform_slots']['pricerange'] = ticket['pricerange']
        goal['inform_slots']['area'] = ticket['area']
        if 'food' in ticket.keys():
            goal['inform_slots']['food'] = ticket['food']
        goal_set[i+50] = goal
    for i in range(50):
        ticket = random.choice(db)
        goal = {'inform_slots': {}}
        goal['diaact'] = 'request'
        goal['request_slots'] = {'address': 'UNK', 'phone': 'UNK'}
        goal['inform_slots']['name'] = ticket['name']
        goal['inform_slots']['pricerange'] = ticket['pricerange']
        goal['inform_slots']['area'] = ticket['area']
        if 'food' in ticket.keys():
            goal['inform_slots']['food'] = ticket['food']
        goal_set[i+150] = goal
    print(goal_set)
    with open('goal_set.json', 'w') as fr:
        fr.write(json.dumps(goal_set))
        '''



