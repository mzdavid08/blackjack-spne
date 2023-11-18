# Nathan Ard, David Meraz
# CSCI 455 Game Theory

import sys
import os.path
import pickle

# Return name of card
def name_of_card(card):
    if card == 1:
        return "Ace"
    else:
        return card

# hit_or_stand[int current_hand][int visible_card][bool soft_total] where visible_card is 1 if ace
hit_or_stand = {}

# Define whether to hit or stand as a matrix for current hand values til 16
for current_hand in range(17):
    for visible in range (1, 11):
        if current_hand <= 12:
            hit_or_stand[(current_hand, visible, False)] = 'H'
            hit_or_stand[(current_hand, visible, True)] = 'H'
        else:
            hit_or_stand[(current_hand, visible, True)] = 'H'
            if visible > 3 and visible <= 6:
                hit_or_stand[(current_hand, visible, False)] = 'S'
            else:
                if current_hand > 13:
                    hit_or_stand[(current_hand, visible, False)] = 'S'
                else:
                    hit_or_stand[(current_hand, visible, False)] = 'H'

# Define whether to hit or stand as a matrix for current hand values from 17
for current_hand in range(17, 22):
    for visible in range (1, 11):
        # Always stand on soft totals
        hit_or_stand[(current_hand, visible, False)] = 'S'

        # Soft totals depend
        if current_hand > 18:
            hit_or_stand[(current_hand, visible, True)] = 'S'
        else:
            if (current_hand == 18 and visible == 9) or (current_hand == 17 and visible != 7):
                hit_or_stand[(current_hand, visible, True)] = 'H'
            else:
                hit_or_stand[(current_hand, visible, True)] = 'S'

def should_hit_or_stand(current_hand, visible, ace):
    if current_hand >= 21:
        return 'S'
    else:
        return hit_or_stand[(current_hand, visible, ace)]

# Function to calculate SPNEs
def calculate_spne(visible_card, starting_val, ace):

    # Create the tree
    def create_tree(node, depth, ace = False, stop_num = 21, max_num = 21, depthLevel = 1):
        # Base case: if depth is zero, return the node as is
        if depth == 0:
            return node

        # Parse the name field to get the result of the parent
        parent_result = int(node["name"].split("=")[1])

        # Generate the first and second child nodes
        childS = {
            "name": "STAND",
            "children": []
        }
        childH = {
            "name": "HIT (CHANCE)",
            "children": [
                {
                    "name": f"{parent_result}+2={2 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+3={3 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+4={4 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+5={5 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+6={6 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+7={7 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+8={8 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+9={9 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+10={10 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+Jack={10 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+Queen={10 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+King={10 + parent_result}",
                    "children": []
                },
                {
                    "name": f"{parent_result}+Ace={1 + parent_result}",
                    "children": []
                }
            ]
        }

        #Calculate odds for outcomes 2-9
        for i in range (8):
            #If there are no aces in current path
            if ace == False:
                #If CH is below stop number, recurse
                if (parent_result + (i+2)) < stop_num:
                    if should_hit_or_stand(parent_result, visible_card, ace) == 'H':
                        childH["children"][i] = create_tree(childH["children"][i], 1, depthLevel = depthLevel+1)
            #There is an ace in the current path
            else:
                #See if path busts
                if ~((parent_result + (i+2)) > max_num or (parent_result + (i+2)) >= stop_num or ((parent_result + (i+2)) >= (stop_num-10)) and ((parent_result + (i+2)) <= (max_num-10))):
                    if should_hit_or_stand(parent_result, visible_card, ace) == 'H':
                        childH["children"][i] = create_tree(childH["children"][i], 1, True, depthLevel+1)

        #Calculate odds for 10, J, Q, K
        for i in range (4):
            #If there are no aces in current path
            if ace == False:
                #If CH is below stop number, recurse
                if (parent_result + 10) < stop_num:
                    if should_hit_or_stand(parent_result, visible_card, ace) == 'H':
                        childH["children"][8+i] = create_tree(childH["children"][8+i], 1, depthLevel = depthLevel+1)
            #There is an ace in the current path
            else:
                #See if path busts
                if ~((parent_result + 10) > max_num or(parent_result + 10) >= stop_num or ((parent_result + 10) >= (stop_num-10)) and ((parent_result + 10) <= (max_num-10))):
                    if should_hit_or_stand(parent_result, visible_card, ace) == 'H':
                        childH["children"][8+i] = create_tree(childH["children"][8+i], 1, True, depthLevel+1)

        #Calculate odds for Ace
        if ~((parent_result + (1)) > max_num or (parent_result + (1)) >= stop_num or ((parent_result + (1)) >= (stop_num-10)) and ((parent_result + (1)) <= (max_num-10))):
            if should_hit_or_stand(parent_result, visible_card, ace) == 'H':
                childH["children"][12] = create_tree(childH["children"][12], 1, True, depthLevel+1)

        node["children"] = [childS, childH]

        return node

    # Extrapolate data
    initial_json = {
        "name": f"CH={starting_val}",
        "children": []
    }

    data = create_tree(initial_json, 1, ace)

    def compute_spne(node, ace, spne = {}):
        # Extract name
        name = int(node["name"].split("=")[1])

        # Base case: Hit or stand says to stand
        if should_hit_or_stand(name, visible_card, ace) == 'S':
            spne[(name, ace)] = 'S'
            return spne[(name, ace)], spne

        # Check ace
        if "Ace" in node["name"]:
            ace = True

        # Base case: no children = always stand
        if not node["children"] or not node["children"][1]["children"]:
            spne[(name, ace)] = 'S'
            return spne[(name, ace)], spne

        # Define SPNE list
        spne[(name, ace)] = ('H', [])

        # Otherwise, iterate through all
        for i in node["children"][1]["children"]:
            spne[(name, ace)][1].append(compute_spne(i, ace, spne)[0])

        # Return the result
        return spne[(name, ace)], spne

    return compute_spne(data, ace)[1]

# Calculate SPNEs based on any visible card
# spne_map[int visible_card][(int current_hand, bool ace)]
spne_map = {}
for i in range (1, 11):
    print(f"Currently calculating SPNEs with {name_of_card(i)} as the visible card...")

    # Start with hard totals: the minimum starting value is 4 consisting of two 2s
    spne_map[i] = calculate_spne(i, 4, False)

    # Update with soft totals: the minimum starting value is two aces leading to 2
    spne_map[i].update(calculate_spne(i, 2, True))

# Define output file
output = os.path.dirname(__file__) + "/../output/spne_map.pkl"
if len(sys.argv) > 1 and sys.argv[1]:
    output = sys.argv[1]

# Write the data to a output file
with open(output, 'wb') as f:
    pickle.dump(spne_map, f)

# To load, use the lines below in another program
# with open('spne_map.pkl', 'rb') as f:
#     loaded_spne_map = pickle.load(f)