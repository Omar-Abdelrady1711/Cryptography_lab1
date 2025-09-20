import numpy
import random
from nistrng import *

def LFSR(degree:int, length:int):
    #generate random number (not exceeding the number of bits specifed)
    bits = random.randint(1, (1 << degree) - 1)
    #the zero is gonna loop over itself so just random gen again
    while bits == 0:
        bits = random.randint(1, (1 << degree) - 1)
    #just a checker 
    print("the random number is: ", bits )
    
    #create a random coefficients list, these coefficients are the taps and they always xor toegther with the LSB
    #they have a length of degree-1 since the LSB is always included
    coefficients = [random.randint(0,1) for _ in range(degree-1)]
    #same as bits, having all zero coefficients will loop over itself
    while sum(coefficients)==0:
        coefficients = [random.randint(0,1) for _ in range(degree-1)]
    print("the random coeff is: ", coefficients )    
    
    #the shifter is basically the taps we selected based on the random coefficients
    shifter=[]
    for i in range(len(coefficients)):
            if coefficients[i]:
                shifter.append(i+1)
    print("For degree", degree, "- the shifter has:", shifter)
    
    #this holds the generated sequence in string type for the testing inside the nist
    sequence=[]
    for _ in range(length):
        state=bits&1
        sequence.append(state)
        bit = state
        for shift in shifter:
            bit ^=  (bits >> (degree-shift)) & 1
        bits= (bits >> 1) | (bit <<(degree-1))  
   # Convert to numpy array for NIST
    test_sequence = numpy.array(sequence, dtype=int)
    return test_sequence



if __name__ == "__main__":
  
    length = 10000
    degrees= [4,7,9,12,16,20] #degrees to test
    
    for degree in degrees:
        print("\nRunning LFSR for degree:", degree)
        
        sequence = LFSR(degree, length)
        
        print("First 20 bits of sequence:", sequence[:20])
        
        eligible_battery: dict = check_eligibility_all_battery(sequence, SP800_22R1A_BATTERY)
        print("Eligible tests from NIST-SP800-22r1a for degree", degree, ":")
        
        for name in eligible_battery.keys():
            print("-", name)
        
        results = run_all_battery(sequence, eligible_battery, False)
        print("Test results for degree", degree, ":")
        
        for result, elapsed_time in results:
            if result.passed:
                print("- PASSED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
            else:
                print("- FAILED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
        
    
