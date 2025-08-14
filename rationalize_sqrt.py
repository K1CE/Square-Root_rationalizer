'''
TODO
- add scientific notation option for user_limit and user_increment
- add processing time test
- add binary stability test
- add target point option
- use functions

'''
print("\n\n===== sqrt rationalizer ========\n     leave blank for default\n     This program is designed to find the multiple of a square root which creates the closest result to a whole number\n     The original purpose of this was to find side lengths of right triangles and other geometric shapes which approximate to workable lengths.\n     √2 or √3 is the usual problem number\n\n")
user_radicand = input(">enter radicand: √")
user_limit = input(">enter upper limit (default is 20): ") 
user_increment = input(">enter allowed increment (default is 1): ")
user_root_index = 2 #TODO: add options for higher order roots
user_goal = 1

#goal_precision = len(user_increment[user_increment.find("."):])

print("\n...")


try:
    user_radicand = float(user_radicand)
except ValueError:
    print(f"'√{user_radicand}' is not a valid number.")

if not user_limit.isnumeric():
    user_limit = 20
user_limit = float(user_limit)

if not user_increment.isnumeric():
    user_increment = 1
user_increment = float(user_increment)
    
user_goal = float(user_increment)
    
iterations = int(user_limit / user_increment)
closest_to_int = 10000
closest_to_increment = user_increment

closest_int = 0
closest_increment = 0

multiplier_to_int = 0
multiplier_to_goal = 0


current_distance = -1

print("\n")

for i in range(iterations):
    multiplier = user_increment * (i + 1)
    result = multiplier * ( (user_radicand) ** (1/user_root_index) )
    print("\r           ", end = "")
    
    current_distance =  result % 1
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
        
    if user_goal != int(user_goal):
        current_distance = result % user_goal
        if current_distance < closest_to_increment:
            closest_to_increment = current_distance
            closest_increment = result - result % user_goal
            multiplier_to_goal = multiplier
            print(f"multiplier {multiplier} with distance {current_distance} to goal {closest_increment}")
            
        current_distance = (user_goal - result) % user_goal
        if current_distance < closest_to_increment:
            closest_to_increment = current_distance
            closest_increment = (user_goal - result) % user_goal
            multiplier_to_goal = multiplier
            print(f"multiplier {multiplier} with distance {current_distance} to goal {closest_increment}")

    print(f"{int(i/iterations * 100)}% complete", end="")
    
print("\r 100% complete")
    #time.sleep(1)
#print(f"entered: {user_radicand}")

