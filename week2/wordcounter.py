from sys import argv
def word_counter():
    for i in argv[1:]:
        with open(i) as f:
            lc = 0
            for c,line in enumerate(f):    
                for line in line.split():
                    lc += 1
        print i +": " + str(lc)    
word_counter()

