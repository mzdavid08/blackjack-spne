# Nathan Ard, David Meraz
# CSCI 455 Game Theory

import sys
import os.path
import json

# Return name of card
def name_of_card(card):
    if card == 1:
        return "Ace"
    else:
        return card

# Function to generate a SPNE
def calculate_spne(starting_val, ace, stop_num, max_num = 21):

    # Define results
    results = {}
    for i in range(stop_num, max_num+1):
        results[i] = 0
    results['BUST'] = 0

    # Function to generate JSON
    def nest_json(node, ace, depth = 1):

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
                    childH["children"][i] = nest_json(childH["children"][i], 1, depth = depth+1)
                #Otherwise, add to percentages
                else:
                    if (parent_result + (i+2)) > max_num:
                        results['BUST'] += ((1/13) ** depth)
                    else:
                        results[parent_result + (i+2)] += ((1/13) ** depth)
            #There is an ace in the current path
            else:
                #See if path busts
                if (parent_result + (i+2)) > max_num:
                    results['BUST'] += ((1/13) ** depth)
                #See if path satisfies hard total
                elif (parent_result + (i+2)) >= stop_num:
                    results[parent_result + (i+2)] += ((1/13) ** depth)
                #See if path satisfies soft total
                elif ((parent_result + (i+2)) >= (stop_num-10)) and ((parent_result + (i+2)) <= (max_num-10)):
                    results[parent_result + (i+12)] += ((1/13) ** depth)
                #Otherwise, recurse
                else:
                    childH["children"][i] = nest_json(childH["children"][i], True, depth+1)

        #Calculate odds for 10, J, Q, K
        for i in range (4):
            #If there are no aces in current path
            if ace == False:
                #If CH is below stop number, recurse
                if (parent_result + 10) < stop_num:
                    childH["children"][8+i] = nest_json(childH["children"][8+i], ace, depth = depth+1)
                #Otherwise, add to percentages
                else:
                    if (parent_result + 10) > max_num:
                        results['BUST'] += ((1/13) ** depth)
                    else:
                        results[parent_result + 10] += ((1/13) ** depth)
            #There is an ace in the current path
            else:
                #See if path busts
                if (parent_result + 10) > max_num:
                    results['BUST'] += ((1/13) ** depth)
                #See if path satisfies hard total
                elif (parent_result + 10) >= stop_num:
                    results[parent_result + 10] += ((1/13) ** depth)
                #See if path satisfies soft total
                elif ((parent_result + 10) >= (stop_num-10)) and ((parent_result + 10) <= (max_num-10)):
                    results[parent_result + 20] += ((1/13) ** depth)
                #Otherwise, recurse
                else:
                    childH["children"][8+i] = nest_json(childH["children"][8+i], True, depth+1)

        #Calculate odds for Ace
        if (parent_result + (1)) > max_num:
            results['BUST'] += ((1/13) ** depth)
        #See if path satisfies hard total
        elif (parent_result + (1)) >= stop_num:
            results[parent_result + (1)] += ((1/13) ** depth)
        #See if path satisfies soft total
        elif ((parent_result + (1)) >= (stop_num-10)) and ((parent_result + (1)) <= (max_num-10)):
            results[parent_result + (11)] += ((1/13) ** depth)
        #Otherwise, recurse
        else:
            childH["children"][12] = nest_json(childH["children"][12], True, depth+1)

        node["children"] = [childS, childH]

        return node

    # Test the function with the provided example and a depth of 2
    initial_json = {
        "name": f"CH={starting_val}",
        "children": []
    }

    for i in range(stop_num, max_num+1):
        results[i] = 0
    results['BUST'] = 0

    data = nest_json(initial_json, ace)

    return data, results

# Starting val
starting_val = 1
if len(sys.argv) > 1 and sys.argv[1]:
    starting_val = sys.argv[1]
ace = False
if name_of_card(starting_val) == "Ace":
    ace = True
stop_num = 17
if len(sys.argv) > 1 and sys.argv[2]:
    stop_num = sys.argv[2]

# Calculate and print data and results
data, results = calculate_spne(starting_val, ace, stop_num)
print(f"With a starting hand of {name_of_card(starting_val)}, the odds are:")
for i in results:
    print("    " + str(i) + ": "+str(results[i]))
total = 0
for i in results:
    total += results[i]
print(total)

# Define output file
output = os.path.dirname(__file__) + "/../output/tree.json"
if len(sys.argv) > 1 and sys.argv[3]:
    output = sys.argv[3]

# Write the data to a output file
with open(output, "w") as json_file:
    json.dump(data, json_file, indent=2)  # 'indent=2' for pretty printing