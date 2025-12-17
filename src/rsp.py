value = input("Enter a value: ")
# try integer, then float; if neither, show message and exit
try:
    num = int(value)
except ValueError:
    try:
        num = float(value)
    except ValueError:
        print("Input is not a number:", value)
        print("type:", type(value))
        raise SystemExit(1)

print(num)
print(type(num))
print(num + 1)