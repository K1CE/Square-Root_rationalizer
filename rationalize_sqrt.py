

class Data_Point():


    def __init__(self, approximate, distance, multiplier, text="goal"):
        self.approximate = approximate
        self.distance = distance
        self.multiplier = multiplier
        self.text = text
    
    @classmethod
    def from_data_point(self, data_point):
        return Data_Point(data_point.approximate, data_point.distance, data_point.multiplier, data_point.text)
        
    def print(self):
        print(f"multiplier {self.multiplier} with distance {abs(self.distance)} to {self.text} {self.approximate}")


def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False


print("\n\n======== sqrt rationalizer ========")
print("     leave blank for default") 
print("     This program is designed to find the multiples of a square root which create the closest result to a whole number")
print("     The original purpose of this was to find side lengths of right triangles and other geometric shapes which approximate to workable lengths.")
print("     √2 or √3 is the usual problem number\n\n")

user_radicand = input(">enter radicand: √")
user_limit = input(">enter upper limit (default is 20): ") 
user_increment = input(">enter allowed increment (default is 1): ")
user_goal = input(">enter goal multiple (default is set to increment): ")
user_root_index = 2 #TODO: add options for higher order roots

#goal_precision = len(user_increment[user_increment.find("."):])

print("\n...")

try:
    user_radicand = float(user_radicand)
except ValueError:
    print(f"'√{user_radicand}' is not a valid number.")

if not is_number_tryexcept(user_limit):
    user_limit = 20
user_limit = float(user_limit)

if not is_number_tryexcept(user_increment):
    user_increment = 1
user_increment = float(user_increment)

if not is_number_tryexcept(user_goal):
    user_goal = float(user_increment)
user_goal = float(user_goal)
    
iterations = int(user_limit / user_increment)

best_integer_data = Data_Point(0, 10000, 0, "integer")
best_goal_data = Data_Point(0, user_goal, 0)

using_goal = user_goal != 1

def find_match(value, multiplier, goal, text, distance_limit):
    #print(f"value is {value}")   
    
    distance = ((value + (goal/2)) % goal - goal/2)
    approximate = value - distance
    
    #print(f"distance from goal {approximate} is {distance}")
    if abs(distance) < distance_limit:
        data = Data_Point(approximate, distance, multiplier, text)
        data.print()
        return data

print("\n")

for i in range(iterations):
    print("\r           ", end = "")
    
    
    multiplier = user_increment * (i + 1)
    result = multiplier * ( (user_radicand) ** (1/user_root_index) )
    
    integer_data = find_match(result, multiplier, 1, "integer", abs(best_integer_data.distance))
    if integer_data:
        best_integer_data = integer_data

    if using_goal:
        goal_data = find_match(result, multiplier, user_goal, "goal", abs(best_goal_data.distance))
        if(goal_data):
            best_goal_data = goal_data
    
    print(f"{int(i/iterations * 100)}% complete", end="")
    
print("\r          100% complete")
print("\n")
print(u'\u2500' * 100) #line


def printResults(multiplier, target, distance):
    print(f"     >>{multiplier} * √{user_radicand}<<")
    print(f" approximating: {target}")
    print(f" with a distance of {distance}")

print("\n the closest multiplier that approaches an integer is: ")
printResults(best_integer_data.multiplier, best_integer_data.approximate, abs(best_integer_data.distance))

if(using_goal):
    print(f"\n the closest multiplier that approaches a multiple of {user_goal}")
    printResults(best_goal_data.multiplier, best_goal_data.approximate, abs(best_goal_data.distance))

print("\n\n(end)\n\n")

