import numpy
import random
from nistrng import *

if __name__ == "__main__":
    man_random = [0,0,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,0,1,0,1,0,1,1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1,1,0,0,1,0,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,0,0,0,0,1,1,0,1,0,1,1,1,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,0,0,1,0,1,1,0,1,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1]
    
    extended_random = [] #to 10000 bits
    position = 0
    positions = list(range(len(man_random)))
    #my algorithm is to extend the sequence by taking every second bit, wrapping around when reaching the end
    while len(extended_random) < 10000:
        extended_random.append(man_random[position])
        position = (position + 2) % len(man_random)
        if position == 0 or position == 1:
            positions.pop(0)
            if not positions:
                positions = list(range(len(man_random)))
            position = positions[0]
    
    #combine both sequences into a numpy array
    bits = numpy.array(man_random + extended_random, dtype=int)
    
    #print first 20 bits to check
    print("First 20 bits:", bits[:20])
    
    #check eligible tests
    eligible_battery: dict = check_eligibility_all_battery(bits, SP800_22R1A_BATTERY)
    
    #print eligible tests
    print("Eligible tests from NIST-SP800-22r1a:")
    for name in eligible_battery.keys():
        print("- " + name)
    
    #run tests
    results = run_all_battery(bits, eligible_battery, False)
    
    print("Test results for manual sequence:")
    for result, elapsed_time in results:
        if result.passed:
            print("- PASSED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
        else:
            print("- FAILED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")