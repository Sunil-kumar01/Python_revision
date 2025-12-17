
'''nums = [4,11,34,566,1111]
nums.reverse()
print(nums)

nums.sort(reverse=True)
print(nums)'''

'''def hello_world():
    print("Hello, world!")  # just defined so no output yet until called #pringting

hello_world()

def sum(num1, num2):
    if(type(num1) != int or type(num2) != int):
        return "Invalid input"
    return num1 + num2# function defined to add two numbers #returning

total = sum(2,3)  # now the result is stored in 'total'
print(total)  # printing the result '''

def multiple_items(*args):
	print(args)
	print(type(args))

multiple_items("Sunil", "Kumar",25, True, "Hello")

def mult_named_items(**kwargs):
	print(kwargs)
	print(type(kwargs))
	   
mult_named_items(name="Sunil", age=25, is_student=True)

def add_one(num):

	if (num>=9):
		return num +1
	
	total = num+1
	print(total)

	return add_one(total)


mynewtotal = add_one(5)
print(mynewtotal)
#while loop for this
value = True

while value:
	print(value)
	value = False
#another example
value="y"
count= 0 # initialize count variable

while value: # loop continues as long as value is truthy
	count+=1 # increment count by 1
	print("Loop count:", count)
	if (count==5):# check if count has reached 5
		break # exit the loop when count reaches 5
	else:
		value=0 # set value to 0
		continue  # continue to the next iteration (though loop will exit since value is 0)


	#MAP, reduce, filter, lambda, list functions
from functools import reduce # import reduce function from functools module
numbers = [1,2,3,4,5]	# list of numbers	
result = reduce(lambda x, y: x * y, numbers) # multiply all numbers in list using reduce function 
print(result) # print the final result (120) 
squared_numbers = list(map(lambda x: x**2, numbers)) # square each number in the list using map function
print(squared_numbers) # print the list of squared numbers ([1, 4, 9, 16, 25])
even_numbers = list(filter(lambda x: x % 2 == 0, numbers)) # filter out even numbers from the list using filter function
print(even_numbers) # print the list of even numbers ([2, 4])
#modules.py and kansas.py
# modules.py
# --- existing code ---
from math import pi, sin, cos
import math	
import random as rdm
from enum import Enum  # corrected: use the standard library 'enum'

print(pi)		
for i in dir(rdm):
	print(i)
# --- existing code ---
import kansas  # corrected: use the standard library 'enum'		
print(kansas.capital)
kansas.randomfunfact()
# kansas.py
# minimal module with the attributes used by modules.py
capital = "Topeka"
def randomfunfact(): # this function prints a random fun fact about Kansas
	print("Kansas is home to the geographic center of the contiguous United States.")
# --- existing code ---
# --- existing code ---
	