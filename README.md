<p align="center"><img width="546" height="100" src="https://github.com/user-attachments/assets/3153b433-755d-43ff-84eb-045b6e62a907" alt="Logo Laravel Boost"></p>

# △
  This project is intended to be used as a simple calculator for bruteforcing and displaying different variations of irrational square-roots. 
  I quickly built this for myself in a couple hours to fix an issue with my design work. By using this app I found a strong candidate for the 
  side lengths of my hexagon's broken down model. When splayed out into triangles and squares each side length could be approximately represented
  in whole numbers. 

  Although it's useful for design work where exact precision isn't necessary, this may not be the solution if you're looking for triangles with actual
  whole numbers.

## The Problem

<img width="381" height="381" alt="rationalizing1" src="https://github.com/user-attachments/assets/af2f8025-3369-4324-a13b-dd82ce8c7e56" />

A simple issue may be encountered when arranging equally sized squares onto triangle faces. They will not align back onto the standard grid ever again.
Image above shows a case where an attempt is made to align the squares back with the grid using another 45 degree right triangle.


## Getting The Solution

<img width="381" height="381" alt="rationalizing2" src="https://github.com/user-attachments/assets/77692b77-aad4-4713-9a49-53dbca9d0c96" />

The previous example can be broken down into a function that solves for the marked distance:

### $y=\frac{3}{2}\cdot x\sqrt{2}-\ 2\cdot x$ 

where x is the width of a square.

Substituting x with `58` (which I hand picked from a list my app generated), we can simplify $58\sqrt{2}$ into 82 because the real result is only two 
hundredths of a unit away:

### $y=\frac{3}{2}\cdot82-\ 2\cdot58$

the equation then quietly resolves to 7

## applying the solution

<img width="381" height="381" alt="rationalizing3" src="https://github.com/user-attachments/assets/8a75cb72-a79d-4bb5-9d19-0675583615ef" />

Finally, we can fill the gap left by the odd geometry with a rectangle that's exactly 65 units in length.
