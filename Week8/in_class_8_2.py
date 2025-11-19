import threading
import time

ranges = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]



def runner(id, start, end, result):
    """ Thread running function. """
    total_sum = sum(range(start, end + 1))
    result[id] = total_sum
        
# Launch this many threads
THREAD_COUNT = len(ranges)


threads = []
result = [0] * THREAD_COUNT


for i in range(THREAD_COUNT):
    id = i
    t = threading.Thread(target=runner, args=(id, ranges[i][0], ranges[i][1], result))
    t.start()

    threads.append(t)

for t in threads:
    t.join()


print(result)
print(sum(result))
    

        