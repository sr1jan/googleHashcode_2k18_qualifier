def distance(start, end):
    x = abs(end[0] - start[0])
    y = abs(end[1] - start[1])

    return x + y

def min_steps(ride1, ride2, cumm_steps):
    # ride1_end is origin [0,0]
    if len(ride1) is 2:
        dist = distance(ride1, ride2[1])
        ride2_es = ride2[3][0]
    else:
        dist = distance(ride1[2], ride2[1])
        ride2_es = ride2[3][0]

    if ride2_es - (dist+cumm_steps) >= 0:
        return ride2_es - (dist+cumm_steps)
    else:
        return dist


def next_schedule(schedule, bonus_rides, total_steps):
    c = []
    l = []
    for vehicle in schedule:
        last_ride = rides_completed[schedule[vehicle][0][-1]]
        cumm_steps = schedule[vehicle][1]

        bonus_rides = sorted(bonus_rides, key=lambda x: min_steps(last_ride, x, cumm_steps))
        ride = bonus_rides[0]

        finish_time = cumm_steps + distance(last_ride[2], ride[1]) + distance(ride[1], ride[2])
        if finish_time > total_steps:
            # print(f"{vehicle}, {ride[0]}, {distance(ride[1], ride[2])}, {finish_time}, {ride}")
            c.append({ride[0]})
            l.append(distance(ride[1], ride[2]))
        # else:
            # print(f"{vehicle}, {ride[0]}, {distance(ride[1], ride[2])}, {finish_time}, {ride}")

        # max_dist_rides = sorted(bonus_rides[:21], key=lambda x: distance(x[1], x[2]), reverse=True)

        schedule[vehicle][0].append(ride[0])
        schedule[vehicle][1] = cumm_steps + distance(last_ride[2], ride[1]) + distance(ride[1], ride[2])
        rides_completed[ride[0]] = ride
        del bonus_rides[bonus_rides.index(ride)]

        if(len(bonus_rides) == 0):
            # print(f"rides_wasted:{len(c)}, points:{sum(l)}")
            return schedule, bonus_rides, c, l

    # print(f"rides_wasted:{len(c)}, points:{sum(l)}")
    return schedule, bonus_rides, c, l


# driver code
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

    bonus_rides = sorted(rides, key=lambda x: min_steps([0,0], x, 0) )

    # for ride in bonus_rides[:21]:
    #     print(f"{ride} ~ {distance(ride[1], ride[2])}")
    rides_completed = {}
    schedule = {}
    # first schedule for vehicles at the start of simulation
    for i in range(vh):
        ride = bonus_rides[i]
        dist = distance([0,0], ride[1])
        cumm_steps = dist + distance(ride[1], ride[2])

        # print(f"{i}, {ride[0]}, ride_l:{distance(ride[1], ride[2])}, dist:{dist}, {ride}, wt:{ride[3][0] - dist}")

        schedule[i] = [[ride[0]], cumm_steps]
        rides_completed[ride[0]] = ride
        del bonus_rides[i]

    # iterating for next schedules
    nv = 0
    ln = 0
    while(len(bonus_rides) != 0):
        br_size = len(bonus_rides)
        schedule, bonus_rides, c, l = next_schedule(schedule, bonus_rides, total_steps)
        nv += len(c)
        ln += sum(l)
        if len(bonus_rides) == br_size: break

    # print(f"total not valid rides: {nv}\ntotal points wasted: {ln}")

    # output
    for i in schedule:
        print(len(schedule[i][0]), *schedule[i][0], sep=" ")

    # print(f"total time taken:{time.time() - start}")
