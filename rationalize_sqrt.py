

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
        print(f"multiplier {self.multiplier} with distance {self.distance} to {self.text} {self.approximate}")


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
closest_to_int = 10000
closest_to_increment = user_increment

closest_int = 0
closest_increment = 0

multiplier_to_int = 0
multiplier_to_goal = 0

current_distance = -1
using_goal = user_goal != 1



print("\n")

for i in range(iterations):
    multiplier = user_increment * (i + 1)
    result = multiplier * ( (user_radicand) ** (1/user_root_index) )
    print("\r           ", end = "")
    
    current_distance = result % 1
    if current_distance < closest_to_int:
        closest_to_int = current_distance
        closest_int = result - result % 1
        multiplier_to_int = multiplier
        print(f"multiplier {multiplier} with distance {current_distance} to integer {closest_int}")
    
    current_distance = (1 - result) % 1
    if current_distance < closest_to_int:
        closest_to_int = current_distance
        closest_int = result + ((1 - result) % 1)
        multiplier_to_int = multiplier
        print(f"multiplier {multiplier} with distance {current_distance} to integer {closest_int}")
        
    if using_goal:
        current_distance = result % user_goal
        if current_distance < closest_to_increment:
            closest_to_increment = current_distance
            closest_increment = result - result % user_goal
            multiplier_to_goal = multiplier
            print(f"multiplier {multiplier} with distance {current_distance} to goal {closest_increment}")
            
        current_distance = (user_goal - result) % user_goal
        if current_distance < closest_to_increment:
            closest_to_increment = current_distance
            closest_increment = result + (user_goal - result) % user_goal
            multiplier_to_goal = multiplier
            print(f"multiplier {multiplier} with distance {current_distance} to goal {closest_increment}")

    print(f"{int(i/iterations * 100)}% complete", end="")
    
print("\r          100% complete")

#fun printHorizontalDivider(dOm: Dom) = { val drawChar = '&U+2014;' arrayOf(dOm.documentWidth, drawChar) }
print("\n")
print(u'\u2500' * 100)


def printResults(multiplier, target, distance):
    print(f"     >>{multiplier} * √{user_radicand}<<")
    print(f" approximating: {target}")
    print(f" with a distance of {distance}")

print("\n the closest multiplier that approaches an integer is: ")
printResults(multiplier_to_int, closest_int, closest_to_int)

if(using_goal):
    print(f"\n the closest multiplier that approaches a multiple of {user_goal}")
    printResults(multiplier_to_goal, closest_increment, closest_to_increment)

print("\n\n(end)\n\n")



    #time.sleep(1)
#print(f"entered: {user_radicand}")
