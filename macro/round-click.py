import pyautogui as pag
import time
from numpy.random import uniform, randn

# sleep parameters
mean = 4
std = 1
min_wait = 3

# position parameters
pos_noise = 4

# probability of long sleep (10min)
p_sleep = 0.001

def sample_time(mean, std, min_wait):
    # Sample time to wait
    # Wait at least for min_wait sec
    return min_wait + abs((mean - min_wait) + std*randn())


def sleep_long():
    start = time.time()
    while (time.time()-start) < 600:
        print(f"sleep_long: 10-min break... slept {int(time.time()-start)}s until now")
        time.sleep(1)


while True:
    start = time.time()
    time.sleep(sample_time(mean, std, min_wait))
    dx = uniform(-pos_noise, pos_noise)
    dy = uniform(-pos_noise, pos_noise)
    pag.click(505+dx, 566+dy, clicks=2, interval=0., button='left')
    print(f"Action 1: position noise {(dx, dy)}, slept {time.time()-start}s")

    start = time.time()
    time.sleep(sample_time(mean, std, min_wait))
    dx = uniform(-pos_noise, pos_noise)
    dy = uniform(-pos_noise, pos_noise)
    pag.click(562+dx, 549+dy, clicks=2, interval=0., button='left')
    print(f"Action 2: position noise {(dx, dy)}, slept {time.time()-start}s")

    start = time.time()
    time.sleep(sample_time(mean, std, min_wait))
    dx = uniform(-pos_noise, pos_noise)
    dy = uniform(-pos_noise, pos_noise)
    pag.click(320+dx, 555+dy, clicks=2, interval=0., button='left')
    print(f"Action 3: position noise {(dx, dy)}, slept {time.time()-start}s")

    x = uniform(0, 1)
    if x < p_sleep:
        sleep_long()


