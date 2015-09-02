from sys import argv

def line_counter():
    lc = 0
    for i in argv[1:]:
        with open(i) as f:
            for counter,line in enumerate(f):    
                lc = counter+1
        print i +": " + str(lc)    
            
line_counter()
