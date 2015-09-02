from sys import argv
import math

def converter():
    print "Fahrenheit to celsius convertion:"
    try:
        temp_in_F = argv[1]
        temp_in_C = str(math.ceil(((int(float(temp_in_F)))-32)*(5./9)))
        print (temp_in_F + " Fahrenheit = " + temp_in_C + " Celsius")
        
    except IndexError:
        print "IndexError: No argument given."
        print argv[0]+" <INPUT>"
        print "Example: " + argv[0] + "75.2"
    except ValueError:
        print "ValueError: "
        if ',' in argv[1]:
 
            print "Use " + argv[1].split(',')[0] + "."+argv[1].split(',')[1] + " instead of " + argv[1]


converter()
