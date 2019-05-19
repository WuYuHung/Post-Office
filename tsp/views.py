"""Simple travelling salesman problem between cities."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from math import asin, cos, radians, sin, sqrt

from django.http import HttpResponse

def create_matrix(coordinates):
    def haversine(lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371
        return c * r * 1000
    matrix = list()
    for i in coordinates:
        distances = list()
        for j in coordinates:
            distances.append(haversine(i[1], i[0], j[1], j[0]))
        matrix.append(distances)
    return matrix

def create_data_model(coordinates):
    """Stores the data for the problem."""
    matrix = create_matrix(coordinates)
    data = {}
    data['distance_matrix'] = matrix # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def print_solution(manager, routing, assignment, indexs):
    """Prints assignment on console."""
    print('Objective: {} meters'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = f'Route for vehicle {str(indexs)}:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}meters\n'.format(route_distance)
    return route_distance


def main(requests):
    clusters = list()
    total_distance = 0
    for index, i in enumerate(clusters):
        """Entry point of the program."""
        # Instantiate the data problem.
        data = create_data_model(i)

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(data['distance_matrix']), data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)


        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        total_distance += print_solution(manager, routing, assignment, index)

    return HttpResponse(total_distance)