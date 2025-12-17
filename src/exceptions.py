#we will learn about exceptions in python
# In somple term exceptions are errors that occur during the execution of a program and are important in handling errors gracefully and specifying alternative code paths when errors occur

try: # code that may raise an exception
	print(5/0)
except ZeroDivisionError: # handling division by zero error
	print("You cannot divide by zero")	

except NameError:# handling variable not defined error
	print("Variable is not defined")
except ZeroDivisionError: # handling division by zero error
	print("You cannot divide by zero")
else: # code to run if no exception occurs
	print("No exceptions occurred")
finally:
	print("Execution completed with error or without error")# this works even if there is no error or if there is an error