def distance(start, end):
    x = abs(end[0] - start[0])
    y = abs(end[1] - start[0])

    return x + y

def next_schedule(schedule, bonus_rides, total_steps):
    for vehicle in schedule:
        last_ride = rides_completed[schedule[vehicle][0][-1]]
        cumm_steps = schedule[vehicle][1]

        if vehicle <= 61 and ((cumm_steps/total_steps) * 100) < 55.0:
            bonus_rides = sorted(bonus_rides, key=lambda x: distance(last_ride[2], x[1]) + distance(x[1], x[2]))
            ride = bonus_rides[0]
        else:
            bonus_rides = sorted(bonus_rides, key=lambda x: distance(last_ride[2], x[1]))
            max_ride = sorted(bonus_rides[:21], key=lambda x: distance(x[1], x[2]), reverse=True)
            ride = max_ride[0]

#         bonus_rides = sorted(bonus_rides, key=lambda x: distance(last_ride[2], x[1]))
#         max_dist_rides = sorted(bonus_rides[:21], key=lambda x: distance(x[1], x[2]), reverse=True)

        # min_dist_ride = [distance from vehicle's cur pos to next ride, cumm_steps till next_ride, next_ride index]
        # min_dist_ride = [distance(last_ride[2], bonus_rides[0][1]),
        #                 cumm_steps+distance(last_ride[2],bonus_rides[0][1]),
        #                 bonus_rides[0][0]]
        # ride = bonus_rides[0]

        # for i, next_ride in enumerate(bonus_rides[1:6]):
        #     ride_length = distance(next_ride[1], next_ride[2])
        #     if ride_length > distance(ride[1], ride[2]):
        #         ride_index = 0
        #         continue

        #     dist_next_ride = distance(last_ride[2], next_ride[1])
        #     cumm_dist_next_ride = cumm_steps + dist_next_ride + ride_length
        #     if cumm_dist_next_ride <= total_steps:
        #         min_dist_ride[0], min_dist_ride[1], min_dist_ride[2] =  dist_next_ride, cumm_dist_next_ride, next_ride[0]
        #         ride = next_ride
        #         ride_index = i

        # if len(ride) is 0: continue

        # schedule[vehicle][0].append(min_dist_ride[2])
        # schedule[vehicle][1] = min_dist_ride[1]
        # rides_completed[ride[0]] = ride
        # del bonus_rides[ride_index]

        # schedule[vehicle][0].append(max_dist_rides[0][0])
        # schedule[vehicle][1] = cumm_steps + distance(last_ride[2], max_dist_rides[0][1]) + distance(max_dist_rides[0][1], max_dist_rides[0][2])
        # rides_completed[max_dist_rides[0][0]] = max_dist_rides[0]
        # del bonus_rides[bonus_rides.index(max_dist_rides[0])]

        schedule[vehicle][0].append(ride[0])
        schedule[vehicle][1] = cumm_steps + distance(last_ride[2], ride[1]) + distance(ride[1], ride[2])
        rides_completed[ride[0]] = ride
        if vehicle <= 61:
            del bonus_rides[0]
        else:
            del bonus_rides[bonus_rides.index(ride)]

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

    # ignore the name bonus_rides
    bonus_rides = sorted_rides

    rides_completed = {}
    schedule = {}
    # first schedule for vehicles at the start of simulation
    for i in range(vh):
        if i <= 61:
            bonus_rides = sorted(bonus_rides, key=lambda x: distance([0,0], x[1]) + distance(x[1], x[2]))
            ride = bonus_rides[0]
        else:
            bonus_rides = sorted(bonus_rides, key=lambda x: distance(x[1], x[2]), reverse=True)
            ride = bonus_rides[0]

        cumm_steps = distance([0,0], ride[1]) + distance(ride[1], ride[2])
        schedule[i] = [[ride[0]], cumm_steps]
        rides_completed[ride[0]] = ride
        if i <= 61:
            del bonus_rides[0]
        else:
            del bonus_rides[bonus_rides.index(ride)]

    while(len(bonus_rides) != 0):
        br_size = len(bonus_rides)
        schedule, bonus_rides = next_schedule(schedule, bonus_rides, total_steps)
        if len(bonus_rides) == br_size: break

    rides_taken = 0
    for i in schedule:
        rides_taken += len(schedule[i][0])
        # print(len(schedule[i][0]))
        print(len(schedule[i][0]), *schedule[i][0], sep=" ")
    # print(f"total ride taken: {rides_taken}")

    # print(f"total time taken:{time.time() - start}")
