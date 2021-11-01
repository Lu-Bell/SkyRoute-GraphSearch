from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices


landmark_string = ""
for key, val in landmark_choices.items():
  landmark_string += "{0} - {1}\n".format(key, val)

stations_under_construction = ['Richmond-Brighouse', 'Sea Island Centre']

#A function to greet the user
def greet():
  print("Hi there and welcome to SkyRoute!")
  print("We'll help you find the shortest route between the following Vancouver landmarks:\n" + landmark_string)

#runs the code
def skyroute():
  greet()
  new_route()
  goodbye()
#Asks the user where they want to start and end so we can show them the shortest path
def set_start_and_end(start_point, end_point):
  if start_point is not None:
    change_point = input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both': ")
    if change_point == 'b':
      start_point = get_start()
      end_point = get_end()
    elif change_point == 'o':
      start_point = get_start()
    elif change_point == 'd':
      end_point = get_end()
      set_start_and_end(start_point, end_point)

    else:
      print("Oops, that isn't 'o', 'd', or 'b'...")
  else:
    start_point = get_start()
    end_point = get_end()
  return start_point, end_point
#Gets the start information from the user
def get_start():
  start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
  if start_point_letter in landmark_choices:
    start_point = landmark_choices[start_point_letter]
    return start_point
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    get_start()
#Gets the end point information from the user
def get_end():
  end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
  if end_point_letter in landmark_choices:
    end_point = landmark_choices[end_point_letter]
    return end_point
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    get_end()

def new_route(start_point=None, end_point=None):
  start_point, end_point = set_start_and_end(start_point, end_point)
  shortest_route = get_route(start_point, end_point)
  #clean string that presents the user with the shortest route
  if shortest_route:
    shortest_route_string ='\n'.join(shortest_route)
    print("The shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
  else:
    print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
  #variable that gives the user a chance to learn more about a particular route
  again = input("Would you like to see another route? Enter y/n: ")
  if again == "y":
    #make a recursive call of new_route() with the current values of start_point and end_point passed in.
    show_landmarks()
    new_route(start_point, end_point)

#This function shows the user landmarks
def show_landmarks():
  see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n:")
  if see_landmarks == "y":
    print(landmark_string)

#gets the shorters route by using the bfs algorithm
def get_route(start_point, end_point):
  start_stations = vc_landmarks[start_point]
  end_stations = vc_landmarks[end_point]
  routes = []
  for start in start_stations: 
    for end in end_stations:
      metro_system = get_active_station() if stations_under_construction else vc_metro
      if len(stations_under_construction) > 0:
        possible_route = dfs(metro_system, start, end)
        route = bfs(metro_system, start, end)
      if not possible_route:
        return None
      if route is not None:
        routes.append(route)
  shortest_route = min(routes, key=len)
  return shortest_route

def get_active_station():
  updated_metro = vc_metro
  for stations in stations_under_construction:
    for current, neighbor in vc_metro.items():
      if current != stations:
        updated_metro[current] -= set(stations)
      else:
        updated_metro[current] = set([])
    return updated_metro



def goodbye():
  print("Thanks for using SkyRoute!")
    
skyroute()