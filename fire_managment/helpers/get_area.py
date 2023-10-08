from geopy.distance import geodesic
from collections import deque
from scipy.spatial import ConvexHull
import utm
import math
# latitude difference to 1 meter (1.0000703876055914) => 0.000010808
# logitude difference to 1 meter (1.000054285773288) => 0.000009016

def generateDistancesFromOneLocation(location, sensors):
    return [math.dist(location.coordinates, sensor.coordinates) for sensor in sensors]

def generateDistancesFromAllToAll(sensors):
    distances = [ generateDistancesFromOneLocation(location, sensors) for location in sensors]
    return distances

def generateAdjacentsList(idx_sensor, distances, max_distance):
    return [idx for idx in range(len(distances)) if idx_sensor != idx and distances[idx][idx_sensor] <= max_distance]

def createGraph(sensors):
    max_distance = 500
    distances = generateDistancesFromAllToAll(sensors)
    return [ generateAdjacentsList(idx_sensor, distances, max_distance) for idx_sensor in range(len(sensors))]

coordinates = [
        ((0.0, 0.0), True),
        ((0.0, 300), True),
        ((0.0, 600), True),
        ((300, 0.0), False),
        ((300, 300), False),
        ((300, 600), True),
        ((600, 0.0), True),
        ((600, 300), True),
        ((600, 600), True),
]

#modificar acesso aos dados dos pontos
def findGroups(sensors):
    groups = []
    graph = createGraph(sensors)
    visited = [sensor.is_burning != 2 for sensor in sensors]
    print(visited)
    for idx_sensor in range(len(sensors)):
        if visited[idx_sensor]:
            continue
        currGroup = []
        q = deque()
        q.append(idx_sensor)
        visited[idx_sensor] = True
        while len(q):
            curr = q.popleft()
            currGroup.append(curr)
            for viz in graph[curr]:
                if visited[viz]:
                    continue
                visited[viz] = True
                q.append(viz)
        groups.append(currGroup)
    return groups

def convLatLonToXY(LatLon):
    valor = utm.from_latlon(*LatLon)
    return valor[0]*1000, valor[1]*1000

def getGroupLines(group, sensors):
    coordinates = [sensors[idx_sensor].coordinates for idx_sensor in group]
    hull = ConvexHull(coordinates)
    lines = []
    for simplex in hull.simplices:
        idx_a = group[simplex[0]]
        coord_a = sensors[idx_a].coordinates
        idx_b = group[simplex[1]]
        coord_b = sensors[idx_b].coordinates
        lines.append((coord_a, coord_b))
    return lines, hull.volume, hull.area