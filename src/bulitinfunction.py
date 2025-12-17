 #Buildin functions for the numbers

abs(gpa)
round(gp, 1)
import math
(math,pi)
print(math.sqrt(16))
print(math.p)
print(math.floor(gpa))
print(math.ceil(gpa))


#casting string to number 
gpa_str = "3.8"
gpa_float = float(gpa_str)
gpa_int = int(float(gpa_str))
print(gpa_float)
print(gpa_int)
#error for casting the incorrect data
zip_code = "new york"#zip code is a number and new york is string so cannot convert
zip_int = int(zip_code) # this causes ValueError