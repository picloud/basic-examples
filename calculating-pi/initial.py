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
    num_in_circle = monte_carlo(total_tests)
    pi = (4 * num_in_circle) / float(total_tests)
    return pi

if __name__ == '__main__':
    pi = calc_pi()
    print 'Pi determined to be %s' % pi
