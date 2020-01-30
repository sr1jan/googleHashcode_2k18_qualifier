def distance(start, end):
    x = abs(end[0] - start[0])
    y = abs(end[1] - start[0])

    return x + y

def next_schedule(schedule, bonus_rides, total_steps):
    # assigning next ride to each vehicle according min distance
    # from current vehicle pos to next ride starting point
    # and also the bonus

    for vehicle in schedule:
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

    sorted_rides = sorted(rides, key=lambda x: distance([0,0], x[1]))

#     if bonus > 2:
#         count = 0
#         bonus_rides = []
#         for ride in sorted_rides:
#             dist = distance([0,0], ride[1])
#             if dist > ride[3][0]: continue
#             bonus_rides.append(ride)
#             # count += 1
#     else:
#         bonus_rides = sorted_rides

    # ignore the name bonus_rides
    bonus_rides = sorted_rides

    rides_completed = {}
    schedule = {}
    # first schedule for vehicles at the start of simulation
    for i in range(vh):
        cumm_steps = distance([0,0], bonus_rides[i][1]) + distance(bonus_rides[i][1], bonus_rides[i][2])
        schedule[i] = [[bonus_rides[i][0]], cumm_steps]
        rides_completed[bonus_rides[i][0]] = bonus_rides[i]
        del bonus_rides[i]

    while(len(bonus_rides) != 0):
        br_size = len(bonus_rides)
        schedule, bonus_rides = next_schedule(schedule, bonus_rides, total_steps)
        if len(bonus_rides) == br_size: break

    for i in schedule:
        print(len(schedule[i][0]), *schedule[i][0], sep=" ")

    # print(f"total time taken:{time.time() - start}")
