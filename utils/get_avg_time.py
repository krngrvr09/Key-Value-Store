import statistics
def parse_time(line):
    # Extract the minutes and seconds from the time line
    minutes, seconds = line.strip().split()[1].split('m')
    seconds = float(seconds[:-1])  # Remove 's' from seconds
    minutes = int(minutes)
    total_seconds = minutes * 60 + seconds
    return total_seconds

def main():
    filename = "latency_1m.txt"  # Replace with your file's name

    real_times = []
    user_times = []
    sys_times = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        if len(lines[i])<2:
            i+=1
            continue
        real_time = parse_time(lines[i])
        user_time = parse_time(lines[i+1])
        sys_time = parse_time(lines[i+2])

        real_times.append(real_time)
        user_times.append(user_time)
        sys_times.append(sys_time)

        i += 4  # Move to the next block of times

    median_real = statistics.median(real_times)
    median_user = statistics.median(user_times)
    median_sys = statistics.median(sys_times)

    variance_real = statistics.variance(real_times)
    variance_user = statistics.variance(user_times)
    variance_sys = statistics.variance(sys_times)

    print("Median Real Time:", median_real)
    print("Median User Time:", median_user)
    print("Median Sys Time:", median_sys)

    print("variance Real Time:", variance_real)
    print("variance User Time:", variance_user)
    print("variance Sys Time:", variance_sys)

if __name__ == "__main__":
    main()
