[1mdiff --git a/rationalize_sqrt.py b/rationalize_sqrt.py[m
[1mindex cc63d2e..f8efcbf 100644[m
[1m--- a/rationalize_sqrt.py[m
[1m+++ b/rationalize_sqrt.py[m
[36m@@ -3,6 +3,7 @@[m [mprint("\n\n===== sqrt rationalizer ========\n     leave blank for default\n[m
 user_radicand = input(">enter radicand: √")[m
 user_limit = input(">enter upper limit (default is 20): ") [m
 user_increment = input(">enter allowed increment (default is 1): ")[m
[32m+[m[32muser_goal = input(">enter goal multiple (default is set to increment): ")[m
 user_root_index = 2 #TODO: add options for higher order roots[m
 user_goal = 1[m
 [m
[36m@@ -33,8 +34,10 @@[m [mif not is_number_tryexcept(user_increment):[m
     user_increment = 1[m
     print("no increment inputted")[m
 user_increment = float(user_increment)[m
[31m-    [m
[31m-user_goal = float(user_increment)[m
[32m+[m
[32m+[m[32mif not is_number_tryexcept(user_limit):[m
[32m+[m[32m    user_goal = float(user_increment)[m
[32m+[m[32muser_goal = float(user_goal)[m
     [m
 iterations = int(user_limit / user_increment)[m
 closest_to_int = 10000[m
