from geopy.distance import geodesic

class Vehicle:
    def __init__(self, vehicle_id, start_location):
        self.vehicle_id = vehicle_id
        self.current_location = start_location
        self.total_toll = 0

    def move(self, new_location):
        self.current_location = new_location

    def add_toll(self, toll):
        self.total_toll += toll


class TollPoint:
    def __init__(self, toll_id, location, charge):
        self.toll_id = toll_id
        self.location = location
        self.charge = charge

    def is_near(self, vehicle_location, radius=0.1):
        distance = geodesic(self.location, vehicle_location).km
        return distance <= radius

# Example GPS coordinates (latitude, longitude)
toll_points = [
    TollPoint('Toll1', (22.5726, 88.3639), 5.0),  # Example toll point
    TollPoint('Toll2', (23.0225, 72.5714), 7.0),
]

vehicles = [
    Vehicle('Vehicle1', (22.5726, 88.3639)),  # Starting at a toll point
    Vehicle('Vehicle2', (23.0225, 72.5714)),
]

def simulate_movement(vehicles, toll_points, path):
    for vehicle in vehicles:
        for point in path:
            vehicle.move(point)
            for toll in toll_points:
                if toll.is_near(vehicle.current_location):
                    vehicle.add_toll(toll.charge)
                    print(f"{vehicle.vehicle_id} passed {toll.toll_id} and paid {toll.charge}. Total toll: {vehicle.total_toll}")

# Example path
path = [
    (22.5726, 88.3639),  # Starting point
    (22.5727, 88.3640),  # Near toll point
    (22.5728, 88.3641),
]

simulate_movement(vehicles, toll_points, path)

import folium

def create_map(vehicles, toll_points):
    fmap = folium.Map(location=[22.5726, 88.3639], zoom_start=12)
    
    for toll in toll_points:
        folium.Marker(location=toll.location, popup=f'Toll: {toll.toll_id}, Charge: {toll.charge}').add_to(fmap)
    
    for vehicle in vehicles:
        folium.Marker(location=vehicle.current_location, popup=f'Vehicle: {vehicle.vehicle_id}, Total Toll: {vehicle.total_toll}', icon=folium.Icon(color='blue')).add_to(fmap)
    
    return fmap

# Create and save the map
simulation_map = create_map(vehicles, toll_points)
simulation_map.save("simulation_map.html")
