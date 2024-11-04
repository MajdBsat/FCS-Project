class Driver:
    def __init__(self, workerID, name, startCity):
        self.workerID = workerID
        self.name = name
        self.startCity = startCity

class WeDeliver:
    def __init__(self):
        self.drivers = {}
        self.nextDriverId = 1
        self.cityNetwork = {
            'Akkar': ['Beirut', 'Jbeil'],
            'Saida': ['Zahle'],
            'Jbeil': ['Beirut', 'Akkar'],
            'Beirut': ['Jbeil', 'Akkar'],
            'Zahle': ['Saida']
        }

    def mainMenu(self):
        print("\nHello! Please enter:")
        print("(1) To go to the drivers' menu")
        print("(2) To go to the cities' menu")
        print("(3) To exit the system")
        
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            self.driversMenu()
        elif choice == "2":
            self.citiesMenu()
        elif choice == "3":
            print("Exiting system. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")

    def driversMenu(self):
        while True:
            print("\n--- Drivers' Menu ---")
            print("Enter:")
            print("(1) To view all the drivers")
            print("(2) To add a driver")
            print("(3) Check similar drivers")
            print("(4) To go back to the main menu")

            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.viewAllDrivers()
            elif choice == "2":
                self.addDriver()
            elif choice == "3":
                self.checkSimilarDrivers()
            elif choice == "4":
                self.mainMenu()
            else:
                print("Invalid choice. Please try again.")

    def viewAllDrivers(self):
        if not self.drivers:
            print("No drivers available.")
        else:
            for driver in self.drivers.values():
                print("ID" + str(driver.workerID).zfill(3) + ", " + driver.name + ", " + driver.startCity)

    def addDriver(self):
        name = input("Enter driver name: ")
        startCity = input("Enter start city: ")

        if startCity not in self.cityNetwork:
            addCity = input("The city is not available. Would you like to add it to the database? (yes/no): ").lower()
            if addCity == 'yes':
                self.cityNetwork[startCity] = []
                print("City added successfully.")
            else:
                print("Driver not added. Please provide a valid start city next time.")
                return

        driver = Driver(self.nextDriverId, name, startCity)
        self.drivers[self.nextDriverId] = driver
        print("Added driver: ID" + str(driver.workerID).zfill(3) + ", " + driver.name + ", " + driver.startCity)
        
        self.nextDriverId += 1

    def checkSimilarDrivers(self):
        cityToDrivers = {}

        for driver in self.drivers.values():
            if driver.startCity not in cityToDrivers:
                cityToDrivers[driver.startCity] = []
            cityToDrivers[driver.startCity].append(driver.name)

        for city, drivers in cityToDrivers.items():
            print(city + ": " + ", ".join(drivers))

    def citiesMenu(self):
        while True:
            print("\n--- Cities' Menu ---")
            print("Enter:")
            print("(1) Show cities")
            print("(2) Search city")
            print("(3) Print neighboring cities")
            print("(4) Print drivers delivering to city")
            print("(5) To go back to the main menu")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                self.showCities()
            elif choice == "2":
                self.searchCity()
            elif choice == "3":
                self.printNeighboringCities()
            elif choice == "4":
                self.printDriversToCity()
            elif choice == "5":
                self.mainMenu()
            else:
                print("Invalid choice. Please try again.")

    def showCities(self):
        if not self.cityNetwork:
            print("No cities available.")
        else:
            citiesList = list(self.cityNetwork.keys())
            n = len(citiesList)
            for i in range(n):
                for j in range(0, n-i-1):
                    if citiesList[j] < citiesList[j+1]:
                        citiesList[j], citiesList[j+1] = citiesList[j+1], citiesList[j]

            print("Cities in the database (sorted Z to A):")
            for city in citiesList:
                print(city)

    def searchCity(self):
        key = input("Enter the key to search for in city names: ")
        matchingCities = [city for city in self.cityNetwork.keys() if key in city]

        if matchingCities:
            print("Cities containing '" + key + "': " + ", ".join(matchingCities))
        else:
            print("No cities found containing '" + key + "'.")

    def printNeighboringCities(self):
        cityName = input("Enter the name of the city: ")

        if cityName in self.cityNetwork:
            neighbors = self.cityNetwork.get(cityName, [])
            if neighbors:
                print("Cities reachable from " + cityName + ": " + ", ".join(neighbors))
            else:
                print("No neighboring cities found for " + cityName + ".")
        else:
            print("City '" + cityName + "' is not in the database.")

    def canReachCity(self, startCity, targetCity, visited=None):
        if visited is None:
            visited = set()

        if startCity == targetCity:
            return True

        visited.add(startCity)

        for neighbor in self.cityNetwork.get(startCity, []):
            if neighbor not in visited:
                if self.canReachCity(neighbor, targetCity, visited):
                    return True

        return False

    def printDriversToCity(self):
        cityName = input("Enter the name of the city: ")

        if cityName in self.cityNetwork:
            print("Drivers delivering to " + cityName + ":")
            driversToCity = [
                driver.name for driver in self.drivers.values() 
                if self.canReachCity(driver.startCity, cityName)
            ]

            if driversToCity:
                print(", ".join(driversToCity))
            else:
                print("No drivers can deliver to " + cityName + ".")
        else:
            print("City '" + cityName + "' is not in the database.")

weDeliver = WeDeliver()
weDeliver.mainMenu()
