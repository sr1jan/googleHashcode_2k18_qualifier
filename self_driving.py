# TODO
#

def distance(start, end):
    x = abs(end[0] - start[0])
    y = abs(end[1] - start[0])

    return x + y

def bonus(ride1, ride2, cumm_steps):
    # ride1_end is origin [0,0]
    if len(ride1) is 2:
        dist = distance(ride1, ride2[1])
        ride2_es = ride2[3][0]
    else:
        dist = distance(ride1[2], ride2[1])
        ride2_es = ride2[3][0]

    if dist is 0:
        return True
    elif dist+cumm_steps == ride2_es:
        return True
    else:
        return False

def next_schedule(schedule, bonus_rides, total_steps):
    # assigning next ride to each vehicle according min distance
    # from current vehicle pos to next ride starting point
    # and also the bonus

    for vehicle in schedule:
        # schedule[vehicle][0][-1] gives the last ride's index completed by a vehicle
        # using above value we can retrive the ride info from rides_completed list
        last_ride = rides_completed[schedule[vehicle][0][-1]]
        cumm_steps = schedule[vehicle][1]
        # min_dist_ride = [distance from vehicle's cur pos to next ride, cumm_steps till next_ride, next_ride index]
        # min_dist_ride = [distance(last_ride[2], bonus_rides[0][1]),
        #                 cumm_steps+distance(last_ride[2],bonus_rides[0][1]),
        #                 bonus_rides[0][0]]
        min_dist_ride = [0,0,0]
        bonus_rides = sorted(bonus_rides, key=lambda x: distance(last_ride[2], x[1]))
        ride = []
        for i, next_ride in enumerate(bonus_rides):
            dist_next_ride = distance(last_ride[2], next_ride[1])
            cumm_dist_next_ride = cumm_steps + dist_next_ride + distance(next_ride[1], next_ride[2])
            if cumm_dist_next_ride <= total_steps:
                min_dist_ride[0], min_dist_ride[1], min_dist_ride[2] =  dist_next_ride, cumm_dist_next_ride, next_ride[0]
                ride = next_ride
                ride_index = i

        if len(ride) is 0: continue

        schedule[vehicle][0].append(min_dist_ride[2])
        schedule[vehicle][1] = min_dist_ride[1]
        rides_completed[ride[0]] = ride
        del bonus_rides[ride_index]

        if(len(bonus_rides) == 0): return schedule, bonus_rides

    return schedule, bonus_rides


if __name__ == '__main__':
    import time
    start = time.time()
    simulation_data = list(map(int, list(input().split())))
    vh, total_rides, bonus, total_steps = simulation_data[2], simulation_data[3], simulation_data[4], simulation_data[5]

    rides = []
    for i in range(total_rides):
       ride_details = (list(map(int, list(input().split()))))
       rides.append([i, [ride_details[0], ride_details[1]], [ride_details[2], ride_details[3]], [ride_details[4], ride_details[5]]])

    # print(f'{simulation_data}\n')

    # sorting in descending order based on ride length
    sorted_rides = sorted(rides, key=lambda x: distance(x[1], x[2]), reverse=True)

    # print("Sorted Rides:")
    count = 0
    bonus_rides = []
    for ride in sorted_rides:
        dist = distance([0,0], ride[1])
        if dist > ride[3][0]: continue
        bonus_rides.append(ride)
        # count += 1
        # print(f"{ride} ~ dfo:{distance([0,0], ride[1])}, ride_length:{distance(ride[1], ride[2])}")

    # print(f"total rides: {count}/{total_rides}, total vehicles: {vh}")

    rides_completed = {}
    schedule = {}
    # assigning top bonus rides with max ride length to each vehicle
    # first schedule for vehicles at the start of simulation
    for i in range(vh):
        for j,ride in enumerate(bonus_rides):
            cumm_steps = distance([0,0], ride[1]) + distance(ride[1], ride[2])
            if cumm_steps <= total_steps:
                schedule[i] = [[ride[0]], cumm_steps]
                rides_completed[ride[0]] = ride
                del bonus_rides[j]
                break
            continue

    while(len(bonus_rides) != 0):
        br_size = len(bonus_rides)
        schedule, bonus_rides = next_schedule(schedule, bonus_rides, total_steps)
        if len(bonus_rides) == br_size: break

    for i in schedule:
        print(len(schedule[i][0]), *schedule[i][0], sep=" ")

    # print(f"total time taken:{time.time() - start}")
