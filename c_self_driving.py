def distance(start, end):
    x = abs(end[0] - start[0])
    y = abs(end[1] - start[0])

    return x + y

def next_schedule(schedule, bonus_rides, total_steps):
    for vehicle in schedule:
        last_ride = rides_completed[schedule[vehicle][0][-1]]
        cumm_steps = schedule[vehicle][1]

        # if vehicle <= 61 and ((cumm_steps/total_steps) * 100) < 55.0:
        #     bonus_rides = sorted(bonus_rides, key=lambda x: distance(last_ride[2], x[1]) + distance(x[1], x[2]))
        #     ride = bonus_rides[0]
        # else:
        #     bonus_rides = sorted(bonus_rides, key=lambda x: distance(last_ride[2], x[1]))
        #     max_ride = sorted(bonus_rides[:21], key=lambda x: distance(x[1], x[2]), reverse=True)
        #     ride = max_ride[0]

        bonus_rides = sorted(bonus_rides, key=lambda x: distance(last_ride[2], x[1]))
        ride = bonus_rides[0]

        finish_time = cumm_steps + distance(last_ride[2], ride[1]) + distance(ride[1], ride[2])
        c = 0
        l = 0
        if finish_time > total_steps:
            # print(f"vehicle[{vehicle}]: ride:{ride[0]}, finish_time:{finish_time}")
            c+=1
            l+=distance(ride[1], ride[2])
        # max_dist_rides = sorted(bonus_rides[:21], key=lambda x: distance(x[1], x[2]), reverse=True)

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
        del bonus_rides[0]

        # if vehicle <= 61:
        #     del bonus_rides[0]
        # else:
        #     del bonus_rides[bonus_rides.index(ride)]

        if(len(bonus_rides) == 0): return schedule, bonus_rides, c, l

    return schedule, bonus_rides, c, l


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

    bonus_rides = sorted(rides, key=lambda x: distance([0,0], x[1]))
    # bonus_rides = sorted(rides, key=lambda x: distance(x[1], x[2]), reverse=True)

    # for ride in bonus_rides[:21]:
    #     print(f"{ride} ~ {distance(ride[1], ride[2])}")

    rides_completed = {}
    schedule = {}
    # first schedule for vehicles at the start of simulation
    for i in range(vh):
    #     # if i <= 61:
    #     #     bonus_rides = sorted(bonus_rides, key=lambda x: distance([0,0], x[1]) + distance(x[1], x[2]))
    #     #     ride = bonus_rides[0]
    #     # else:
    #     #     bonus_rides = sorted(bonus_rides, key=lambda x: distance(x[1], x[2]), reverse=True)
    #     #     ride = bonus_rides[0]

        bonus_rides = sorted(bonus_rides, key=lambda x: distance([0,0], x[1]))
        ride = bonus_rides[0]

        cumm_steps = distance([0,0], ride[1]) + distance(ride[1], ride[2])
        schedule[i] = [[ride[0]], cumm_steps]
        rides_completed[ride[0]] = ride
        del bonus_rides[bonus_rides.index(ride)]

        # if i <= 61:
        #     del bonus_rides[0]
        # else:
        #     del bonus_rides[bonus_rides.index(ride)]

    c = 0
    l = 0
    # iterating for next schedules
    while(len(bonus_rides) != 0):
        br_size = len(bonus_rides)
        schedule, bonus_rides, nv, ln = next_schedule(schedule, bonus_rides, total_steps)
        c+=nv
        l+=ln
        if len(bonus_rides) == br_size: break

    print(f"total not valid rides: {c}\ntotal points wasted: {l}")
    # output
    # for i in schedule:
    #     print(len(schedule[i][0]), *schedule[i][0], sep=" ")

    # print(f"total time taken:{time.time() - start}")
