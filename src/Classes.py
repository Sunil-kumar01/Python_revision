# let us lear about class and how tod efine them in python
class Vehicle:
	def __init__(self, make, model):# constructor method, it is called when an object is created and helps initialize the object's attributes
		self.make = make
		self.model = model
	def moves(self):
		print("Vehicle is moving") # defining a class with a method

	def get_make_model(self):
		print(f"{self.make} {self.model}")  # method to get full vehicle description		

my_car = Vehicle('tesla', 'model s')

#print(my_car.make)
#print(my_car.model)
my_car.moves()

#YOU CAN CREATE ANOTHER OBJECTS AS WELL FROM SAME CLASS
my_bike = Vehicle('Yamaha', 'FZ')
my_bike.moves()
my_bike.get_make_model()
my_car.get_make_model()
# Now let us learN about the inheritance in python


class Airoplane(Vehicle): # inheriting from Vehicle class
	def moves(self):
		print("Airoplane is flying")  # overriding the moves method

class Truck(Vehicle): # inheriting from Vehicle class
	def moves(self):
		print("Truck is driving on the road")  # overriding the moves method	

class GolfCart(Vehicle): # inheriting from Vehicle class
    pass
# no custom moves method, will use Vehicle's moves method
cessna = Airoplane('Cessna','Skyhawk')# no custom moves method, will use Vehicle's moves method
mack = Truck('Mack','Pinnacle')
golfwagon = GolfCart('Yamaha','GC100') # no custom moves method, will use Vehicle's moves method

#now calling the moves and get_make_model method on each object
cessna.moves()  # Output: Airoplane is flying
cessna.get_make_model()  # Output: Cessna Skyhawk
mack.moves()  # Output: Truck is driving on the road	
mack.get_make_model()  # Output: Mack Pinnacle	
golfwagon.moves()  # Output: Vehicle is moving
golfwagon.get_make_model()  # Output: Yamaha GC100 

# Now let us learn about the super() function in python
class ElectricVehicle(Vehicle):
    def __init__(self, make, model, battery_size):
        super().__init__(make, model)  # call the constructor of the parent Vehicle class
        self.battery_size = battery_size  # initialize additional attribute

    def get_battery_info(self):
        print(f"Battery size: {self.battery_size} kWh")  # method to display battery info	
my_ev = ElectricVehicle('Nissan', 'Leaf', 40)
my_ev.get_make_model()  # Output: Nissan Leaf
my_ev.get_battery_info()  # Output: Battery size: 40 kWh
my_ev.moves()  # Output: Vehicle is moving


###################|||||#################
# Now let us learn about the polymorphism in python Polimorphism is the ability to present the same interface for differing underlying data types. or simply it means that different classes can be treated through the same interface, typically by having methods with the same name. or simply put, polymorphism allows methods to do different things based on the object it is acting upon. more simply, polymorphism allows us to define methods in the child class with the same name as defined in their parent class. When you call the method from an object of the child class, the child class's method is executed instead of the parent class's method. This is particularly useful in scenarios where you want to treat different objects in a similar way but have them behave differently based on their specific types. or even though we give same mesaage but get different output based on the object type
for vehicle in (my_car, cessna, mack, golfwagon, my_ev):

	vehicle.moves()  # calls the appropriate moves method based on the object type
	vehicle.get_make_model()  # calls the get_make_model method from Vehicle class

#Super() helps us to call the constructor of the parent class or simply helps us inherit the attributes and methods from the parent class or if anything is not defined in the child class then it will inherit from the parent class and help in defining the attributes and methods
