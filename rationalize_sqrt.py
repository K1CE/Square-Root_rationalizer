'''
TODO
- add scientific notation option for user_limit and user_increment
- add processing time test

'''
print("\n\n===== sqrt rationalizer ========\n     leave blank for default\n     This program is designed to find the multiple of a square root which creates the closest result to a whole number\n     The original purpose of this was to find side lengths of right triangles and other geometric shapes which approximate to workable lengths.\n     √2 or √3 is the usual problem number\n\n")
user_sqrt = input(">enter radicand: √")
user_limit = input(">enter upper limit (default is 20): ") 
user_increment = input(">enter allowed increment (default is 1): ")
print("\n...")

try:
    user_sqrt = float(user_sqrt)
except ValueError:
    print(f"'√{user_sqrt}' is not a valid number.")

print(f"entered: {user_sqrt}")
