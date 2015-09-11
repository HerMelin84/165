from sys import argv
import math

def converter():
    print "Fahrenheit to celsius convertion:"
    temp_in_F = float(argv[1])
    print "%.1f" %temp_in_F
    temp_in_C = ((float(temp_in_F))-32)*(5./9)
    print "{:.1f} Fahrenheit is equal to {:.1f} Celsius".format(temp_in_F,temp_in_C)


converter()
