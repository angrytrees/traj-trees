__author__ = 'Hoang Thanh Lam'
__date__ = '31/03/17'
import Geohash
from error import SquareError
import math

# General idea: if we have a list of points, and the list is sorted according to the geohash of the points, then near
# points in the list are also near to each other in the map. This is due to the property of geohash, if two points share
# very long prefix in their geohash, they tend to be near to each other although not always.


# Since the distance is relatively small, you can use the equirectangular distance approximation
def haversine(point1, point2):
    # radius of the earth in km
    R = 6371
    # get lat and lon
    lon1, lat1 = point1[0], point1[1]
    lon2, lat2 = point2[0], point2[1]
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # formula
    x = (lon2 - lon1) * math.cos( 0.5*(lat2+lat1) )
    y = lat2 - lat1
    d = R * math.sqrt( x*x + y*y )
    return d


def get_geohash_index(points, precision=12):
    """
    get a list of geohash
    :param points: a list of GPS points
    :param precision: the length of a geohash binary string, the longer the string is the more precise the geohash is
    :return: a list of geohash (binary strings)
    """
    geo_index = [Geohash.encode(latitude=p[1], longitude=p[0], precision=precision) for p in points]
    return geo_index


def sort(points, targets):
    """
    sort points and target according to geohash of points
    :param points: a list of gps points
    :param targets: a list of target
    :return: sorted points and targets
    """
    geo_index = get_geohash_index(points)
    tuples = list()
    n = len(geo_index)
    for i in range(n):
        tuples += [(geo_index[i], points[i], targets[i])]

    # sort the tuples according to the order of geohash
    tuples = sorted(tuples, key=lambda x: x[0])

    # create new points and targets in sorted order
    new_points = []
    new_target = []
    for i in range(n):
        new_points += tuples[i][1]
        new_target += tuples[i][2]
    return new_points, new_target


def find_decision_point(points, targets, max_radius=1):
    """
    find the best decision point and radius
    :param points: a list of points
    :param targets: a list of target (np.array)
    :param max_radius: maximum radius to consider (Km)
    :return: the best decision point and radius
    """
    sorted_points, sorted_targets = sort(points, targets)
    best_radius = None
    best_gain_so_far = 0
    best_decision_point = None
    for idx in range(len(sorted_points)):
        radius, gain = find_best_radius(idx, sorted_points, sorted_targets, max_radius)
        if best_gain_so_far < gain:
            best_gain_so_far = gain
            best_decision_point = points[idx]
            best_radius = radius
    return best_decision_point, best_radius


def find_best_radius(idx, points, targets, max_radius=1):
    """
    find the best radius for a point with index idx
    :param idx: index of the decision point
    :param points: a list of gps points, sorted according to geohash order
    :param targets: a list of corresponding targets
    :param max_radius: maximum radius to consider for search
    :return: the best radius and maximum gain
    """
    n = len(points)
    # square error of the points outside the circle, from the beginning all points are outside the circle
    outside = SquareError()
    outside.add_list(targets)
    all_se = outside.sum_of_square_error()

    # square error of the points outside the circle, from the beginning no point is inside the circle
    inside = SquareError()

    left_idx = idx
    right_idx = idx
    current_radius = 0
    gain = 0
    best_radius = -1
    while current_radius < max_radius:
        if left_idx > 0 and right_idx < n-1:
            # if there are elements to the right and to the left
            distance_to_next_left = haversine(points[idx], points[left_idx - 1])
            distance_to_next_right = haversine(points[idx], points[right_idx + 1])
            if distance_to_next_left < distance_to_next_right:
                # move to the left
                current_radius = distance_to_next_left
                while distance_to_next_left == distance_to_next_right:
                    inside.add(points[left_idx])
                    outside.remove(points[left_idx])
                    left_idx -= 1
                    if left_idx == 0:
                        break
                    else:
                        distance_to_next_left = haversine(points[idx], points[left_idx - 1])
                current_radius = haversine(points[idx], points[left_idx])
            elif distance_to_next_left > distance_to_next_right:
                # move to the right
                current_radius = distance_to_next_right
                while distance_to_next_right == current_radius:
                    inside.add(points[right_idx])
                    outside.remove(points[right_idx])
                    right_idx += 1
                    if right_idx == n-1:
                        break
                    else:
                        distance_to_next_right = haversine(points[idx], points[right_idx + 1])
            else:
                # if distance_to_next_left == distance_to_next_right, move to both size until there is no tight
                # move to the left
                current_radius = distance_to_next_left
                while distance_to_next_left == distance_to_next_right:
                    inside.add(points[left_idx])
                    outside.remove(points[left_idx])
                    left_idx -= 1
                    if left_idx == 0:
                        break
                    else:
                        distance_to_next_left = haversine(points[idx], points[left_idx - 1])

                current_radius = distance_to_next_right
                while distance_to_next_right == current_radius:
                    inside.add(points[right_idx])
                    outside.remove(points[right_idx])
                    right_idx += 1
                    if right_idx == n-1:
                        break
                    else:
                        distance_to_next_right = haversine(points[idx], points[right_idx + 1])
        elif left_idx == 0 and right_idx < n-1:
            # if no element to the left but still elements to the right
            distance_to_next_right = haversine(points[idx], points[right_idx + 1])
            current_radius = distance_to_next_right
            while distance_to_next_right == current_radius:
                inside.add(points[right_idx])
                outside.remove(points[right_idx])
                right_idx += 1
                if right_idx == n-1:
                    break
                else:
                    distance_to_next_right = haversine(points[idx], points[right_idx + 1])
        elif right_idx == n-1 and left_idx > 0:
            # if no element on the right but still elements on the left
            distance_to_next_left = haversine(points[idx], points[left_idx - 1])
            current_radius = distance_to_next_left
            while distance_to_next_left == distance_to_next_right:
                inside.add(points[left_idx])
                outside.remove(points[left_idx])
                left_idx -= 1
                if left_idx == 0:
                    break
                else:
                    distance_to_next_left = haversine(points[idx], points[left_idx - 1])

        else:
            break

        # update gain
        outside_se = outside.sum_of_square_error()
        inside_se = inside.sum_of_square_error()
        new_gain = all_se - outside_se - inside_se
        if gain < new_gain:
            gain = new_gain
            best_radius = current_radius
    return best_radius, gain



