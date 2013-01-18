import cloud
import random
total_tests = 500000000

def monte_carlo(num_test):
    """Throw num_test darts at a square.
    Return how many appear within the quarter circle"""
    
    num_in_circle = 0
    for _ in xrange(num_test):
        x = random.random()
        y = random.random()
        if x*x + y*y < 1.0:  #within the quarter circle
            num_in_circle += 1
    return num_in_circle

def calc_pi():
    """Almost correct way"""

    num_jobs = 8
    tests_per_call = total_tests/num_jobs

    # list of job ids for all jobs we're spawning
    jids = []
    for _ in range(num_jobs):
        # call() does not block, so jobs run in parallel
        jid = cloud.call(monte_carlo, tests_per_call, _type='c2')
        jids.append(jid)

    # aggregate the number of darts that land in the circle
    # across all jobs that we spawned
    num_in_circle = 0
    for jid in jids:
        num_in_circle += cloud.result(jid)

    pi = (4 * num_in_circle) / float(total_tests)
    return pi

if __name__ == '__main__':
    pi = calc_pi()
    print 'Pi determined to be %s' % pi
