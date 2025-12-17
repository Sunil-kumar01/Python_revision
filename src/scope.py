
name = "Sunil" #global variable

def greeting(namek):
	color = "blue"
	print(color)#local variable
	print(name) #global variable
	print(namek)#local variable

greeting("John")#calling function


def another_function():
	age = 25 #local variable
	print(age)

def another_function2():#another function inside another function   
	greeting("Sunil") #global variable

another_function2() #calling another function inside another function

#we did nested function and variables things

another_function()#calling another function 

name = "Alice" #global variable
count = 10 #global variable

def function17():
	color = "red" #local variable
	#count=2#this is also local variable and created new variable
	#count +=1 #this will give error because count is not defined in local scope
	global count #to use global variable inside function
	count += 1 #now this will work because we declared count as global
	print(count) #prints global variable

	def inner_function(name):
		print(name) #local variable
		print(color) #local variable from outer function
		print(name) #global variable from outer scope

	greeting("Bob") #global variable

#Above is nested function and variable scope