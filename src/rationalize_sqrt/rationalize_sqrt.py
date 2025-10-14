#########IMPORTS
import sys
import time



#########CLASSES

#simple object for storing data in groups.
#    represents a multiplier that approximates a number when it was multiplied by a square root
#    TODO: add the function itself to the Data_Point class?
class Data_Point():

    def __init__(self, approximates, distance, multiplier, text="goal"):
        self.approximates = approximates
        self.distance = distance
        self.multiplier = multiplier
        self.text = text
    
    @classmethod
    def from_data_point(self, data_point):
        return Data_Point(data_point.approximate, data_point.distance, data_point.multiplier, data_point.text)
        
    def print(self):
        print(f"multiplier {self.multiplier} with distance {abs(self.distance)} to {self.text} ", end = "")
        for i in range(len(self.approximates)):
            print(self.approximates[i], end = "")
            if i < len(self.approximates) - 1:
                print(", ", end = "")
        print()




#########FUNCTIONS

def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def attempt_convert_scientific_notation(s):
    s = s.lower()
    index = s.find('e')
    if index >= 0:
        s1 = s[0:index]
        s2 = s[index + 1:]
        if is_number_tryexcept(s1) and is_number_tryexcept(s2):
            return float(s1) ** float(s2)
    return s
    
    

def find_match(values, multiplier, goal, text, distance_limit):
    #print(f"value is {value}") #debug code
    
    #calculates distance to closest multiple of the goal. 
    #because 'value' will be in between two approximate goal nums, we add goal/2 in conjunction with modulo to
    #get the remainder only if it's half a goal num away
    averageDistance = 0
    distance = 0
    approximates = []
    for i in range(len(values)):
        distance = ((values[i] + (goal/2)) % goal - goal/2)
        averageDistance += abs(distance)
        approximates.append(values[i] - distance)
    
    averageDistance = averageDistance / len(values)
    
    #print(f"distance from goal {approximate} is {distance}") #debug code
    #distance_limit is used to filter undesirable results
    if abs(averageDistance) < distance_limit and abs(distance) < distance_limit:
        data = Data_Point(approximates, averageDistance, multiplier, text)
        data.print()
        return data
    #returns null if theres no match

def mod_minimum(new_entry):
    distance = abs(new_entry.distance)
    if distance < minimum_distance:
        #print(f"minimum {minimum_distance}")
        #print(f"new minimum {minimum_distance - (distance - minimum_distance) / MAX_MENTIONS}")
        return minimum_distance - (minimum_distance - distance) / MAX_MENTIONS
    else:
        return minimum_distance


def store_mention(data):
    space = mentions[MAX_MENTIONS - 1] is None
    for i in range(MAX_MENTIONS):
        if space:
            if not mentions[i]:
                mentions[i] = data
                return True
        else:
            if abs(data.distance) < abs(mentions[i].distance):
                mentions[i] = data
                return True
        
        
        




#########USER INPUT

advancedMode = len(sys.argv) > 1 and sys.argv[1] == "-advanced"

print("\n\n======== sqrt rationalizer ========")
print("     leave blank for default") 
print("     This program is designed to find the multiples of a square root which create the closest result to a whole number")
print("     The original purpose of this was to find side lengths of right triangles and other geometric shapes which approximate to workable lengths.")
print("     √2 or √3 is the usual problem number\n\n")

user_radicand_list = []
user_radicand_list.append(input(">enter radicand: √"))
if advancedMode:
    i = 0
    while True:
        i += 1
        extra = input(">enter extra radicand (optional): √")
        if extra == "": 
            break
        user_radicand_list.append(extra)
user_limit = input(">enter upper limit (default is 20): ") 
user_increment = input(">enter allowed increment (default is 1): ")
user_goal = input(">enter goal multiple (default is set to increment): ")
user_root_index = 2 #TODO: add options for higher order roots

#goal_precision = len(user_increment[user_increment.find("."):])

print("\n...")

num_radicands = len(user_radicand_list)

for i in range(num_radicands):
    try:
        user_radicand_list[i] = float(user_radicand_list[i])
    except ValueError:
        print(f"'√{user_radicand_list[i]}' is not a valid number.")

user_limit = attempt_convert_scientific_notation(user_limit)
if not is_number_tryexcept(user_limit):
    user_limit = 20
user_limit = float(user_limit)

user_increment = attempt_convert_scientific_notation(user_increment)
if not is_number_tryexcept(user_increment):
    user_increment = 1
user_increment = float(user_increment)

user_goal = attempt_convert_scientific_notation(user_goal)
if not is_number_tryexcept(user_goal):
    user_goal = float(user_increment)
user_goal = float(user_goal)

using_goal = user_goal != 1
    
    



#########START OF MAIN PROCESS

MAX_MENTIONS = 10

iterations = int(user_limit / user_increment)
minimum_distance = user_goal/10

best_integer_data = Data_Point(0, 10000, 0, "integer")
best_goal_data = Data_Point(0, user_goal, 0)
mentions = [None] * 10


#tracking completion time
start_time = time.time()

print("\n")

for i in range(iterations):
    print("\r           ", end = "")
    
    #current testcase
    multiplier = user_increment * (i + 1)
    
    #the core math function: multiplier √(radicand)
    #the result is stored and compared with previous results to decide if the multiplier is notably close to an integer/goal
    results = []
    for g in range(num_radicands):
        results.append(multiplier * ( (user_radicand_list[g]) ** (1/user_root_index) ))
    
    best = False #track if it was selected for best option
    
    #***program always shows results for integers regardless of settings
    #previous best integer approximate is compared with this iteration.
    integer_data = find_match(results, multiplier, 1, "integer", abs(best_integer_data.distance))
    #an output indicates that this iteration is closer to an integer
    if integer_data:
        best_integer_data = integer_data
        best = True

    #***if a custom goal or increment is set for iterating, the program will track the closest match to a multiple of that increment
    if using_goal:
    
        #previous best increment approximate is compared with this iteration
        goal_data = find_match(results, multiplier, user_goal, "goal", abs(best_goal_data.distance))
        #an output indicates that this iteration is closer to a multiple of an increment
        if goal_data:
            store_mention(best_goal_data)
            best_goal_data = goal_data
            best = True
    
    #***this is the honorable mentions circuit. remembers results that aren't the best
    if not best:
        mention_data = find_match(results, multiplier, user_goal, "mention", minimum_distance)#redundant
        if mention_data:
            stored = store_mention(mention_data)
            if stored:
                minimum_distance = mod_minimum(mention_data)
    
    print(f"{int(i/iterations * 100)}% complete", end="")
    
print("\r           100% complete")
print("           %ss" % (round(time.time() - start_time, 4))) #execution time
print("\n")
print(u'\u2500' * 100) #line

#########END OF MAIN PROCESS








#########USER OUTPUT

def printResults(multiplier, targets, distance):
    if len(targets) <= 1:
        print(f"     >>{multiplier} * √{user_radicand_list[0]}<<")
        print(f" approximating: {targets[0]}")
        print(f" with a distance of {distance}")
    else:
        print(f"     >>{multiplier} * (√{user_radicand_list[0]}", end="")
        for i in range(1, num_radicands):
            print(f" OR √{user_radicand_list[i]}", end="")
        print(")<<")
        
        print(f" approximating: {targets[0]}", end="")
        for i in range(1, num_radicands):
            print(f", {targets[i]}", end="")
        print()
        
        print(f" with an average distance of {distance}")

print("\n the closest multiplier that approaches an integer is: ")
printResults(best_integer_data.multiplier, best_integer_data.approximates, abs(best_integer_data.distance))

if(using_goal):
    print(f"\n the closest multiplier that approaches a multiple of {user_goal}")
    printResults(best_goal_data.multiplier, best_goal_data.approximates, abs(best_goal_data.distance))

print("\n\nmentions:")
for i in range(MAX_MENTIONS):
    if not mentions[i]: #list ends here so leave loop
        break
    mentionV = mentions[i].distance
    mentionE = 0
    if mentionV != 0.0:
        while int(mentionV) == 0.0:
            mentionV *= 10
            mentionE -= 1
    mentionV = round(abs(mentionV), 5)
    print(f"{mentions[i].multiplier}({mentionV}e{mentionE})")


#ascii
print("\n\n")      
print("                      ▲")
print("                            ◣")
print("                               ▼")
print("")
print("                                ◥")
print("")
print("                            ◤")
print("")
print("                        ►")
print("                     ◂")
print("                    ▸")
print("                     ▵")
print("")
print("                         ◃")

print("\n(end)\n\n")

