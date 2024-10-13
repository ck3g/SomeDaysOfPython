class Restaurant:
    """Holds information about a restaurant"""

    def __init__(self, restaurant_name, cousine_type):
        self.restaurant_name = restaurant_name
        self.cousine_type = cousine_type

    def describe_restaurant(self):
        print(f"{self.restaurant_name} - {self.cousine_type}")

    def open_restaurant(self):
        print("Restaurant is now open!")


restaurant = Restaurant("Dönner King", "Turkish")

print(restaurant.restaurant_name)
print(restaurant.cousine_type)

restaurant.describe_restaurant()
restaurant.open_restaurant()
