from feedline import feedline
from getchar import getchar 
import sys

namespace = vars().copy()   
    

def prompt():
    """
    Prompt function for initializing the shell.
    Let's you navigate the string, adds some color to the output.
    It remebers previous given commands. Possible to save the session to file by doing %save filename
    
    When navigating the history, it prints it in a new line everytime. This can easily be changed
    by clearing the sys.stdin and writing it again. The example in the assigment did it my way, so I stuck
    by it. 
    
    cur_pos is the current position. 
    tmpcount is the counter for navigating the history. 
    cmd_count is the command count. 
    Colors are self explanatory. 
    ! Will execute a sh command. 
    ? Will execute a help command
    % Will save the the buffer parameter to a given file.
    

    """
    input=""            # Buffer for line
    tmpcount=-1         # Counter for history. Default is -1 for simplicity. 
    RED='\x1b[31;1m'    # Red for error
    RED2='\x1b[91m'     # Red for error message
    GREEN='\x1b[92;1m'  # 'In []'
    BLUE='\x1b[94;1m'   # Blue for 'Out []'
    MAGENTA='\x1b[95;1m'# Magenta for navigation history. 
    RESET= '\x1b[0m'    # RESET to default
    ARROW='\x1b'        # First byte of an arrow key  
    cmd_count=0;        # Number of commands
    history=list()      # The command history
    cur_pos=0           # Current position in the line. 
    print "Welcome to mypython.py:"
    print "!sh-command  Will execute a sh command. \n?object      Will execute a help command\n%save x      Will save the the buffer parameter to a given file(x)."
    sys.stdout.write("{0}In [{1}]{2} ".format(GREEN,cmd_count,RESET))
    while(True):

        Arrow=True                  # assume it's an arrow, by default
        char=getchar()              # get a character from stdin. 
        if char==ARROW:             # arrow key was pressed. 
            char+=sys.stdin.read(2) # read the next 2 bytes.
            if char=='\x1b[A':      # up arrow was pressed.
                cur_pos=0
                if tmpcount==0:     # already on the first command. fifo-list(stack)
                    continue

                if cmd_count>0:     # not on the first command
                    tmpcount= (cmd_count-1) if tmpcount==-1  else (tmpcount-1 if tmpcount>0 else 0)
                    sys.stdout.write("\n{0}In [{1}] {2}{3} {4}".format(GREEN,cmd_count,MAGENTA,history[tmpcount],RESET))
                    input=history[tmpcount]
                
            elif char=='\x1b[B':    # the down arrow was pressed
                cur_pos=0
                if not tmpcount==-1 and tmpcount<(cmd_count-1): # makes sure we're in the history somewhere
                    tmpcount=tmpcount+1
                    sys.stdout.write("\n{0}In [{1}] {2}{3} {4}".format(GREEN,cmd_count,MAGENTA,history[tmpcount],RESET))
                    input=history[tmpcount]

                elif tmpcount==(cmd_count-1): #we're at the last command. same as ctrl+d
                    sys.stdout.write("\r{0}In [{1}]{2} \033[K".format(GREEN,cmd_count,RESET))
                    input=""
                else:                    # not in the history
                    continue

            elif char=='\x1b[C':         # right arrow was pressed
                if cur_pos>0:
                    sys.stdout.write("\033[C")
                    cur_pos-=1
                continue

            elif char=='\x1b[D':         # left arrow was pressed
                if cur_pos<len(input):
                    cur_pos+=1
                    sys.stdout.write("\033[D")
                continue
        else:
            if hex(ord(char))=='0x4':    # ctrl+D
                if not input:            # nothing in the line, exit
                    print "{0}exiting..".format(RESET)
                    sys.exit(0) 

                else:                    # something in the line, clear it. 
                    input=""
                    sys.stdout.write("\r{0}In [{1}]{2} \033[K".format(GREEN,cmd_count,RESET))

            elif hex(ord(char))=='0x7f': # backspace
                if cur_pos==0:
                    input=input[:-1]
                    sys.stdout.write("\r{0}In [{1}]{2} {3}\033[K".format(GREEN,cmd_count,RESET,input))

                else:
                    input=input[:-cur_pos-1]+input[-cur_pos:]        # remove one char
                    sys.stdout.write("\r{0}In [{1}]{2} {3}\033[K".format(GREEN,cmd_count,RESET,input))
                    sys.stdout.write('\033[D'*cur_pos) #setting the cursor back

            else:                                      # just a char
                if char:
                    if cur_pos==0:                     # the end of the line
                        tmpcount=-1                    # reset tmpcount
                        sys.stdout.write(char)         # print char to screen
                        Arrow=False                    # an arrow was not pressed
                    else:                              # not at the end of the line
                        input=input[:-cur_pos]+char+input[-cur_pos:] 
                        sys.stdout.write("\r{0}In [{1}]{2} {3}\033[K".format(GREEN,cmd_count,RESET,input))
                        sys.stdout.write('\033[D'*cur_pos) # setting the cursor back to where it was

        if char in "\r\n": # enter was pressed
            cur_pos=0      # reset posision

            if not input:  # line was empty, print out standard message without counting
                sys.stdout.write("\n{0}In [{1}]{2} ".format(GREEN,cmd_count,RESET))
                continue
            else:          # line was not empty


                if 'exit' in input or 'quit' in input:
                    sys.stdout.write("\n\033[K".format(GREEN,cmd_count,RESET))
                    print "{0}exiting...".format(RESET)
                    sys.exit(0)

                history.append(input) 


                if input[0]=='!' or input[0]=='?' or input[0]=='%': # one of the "special" commands
                    out=feedline(input,namespace,history)
                else:
                    out=feedline(input,namespace) 


                if 'Error' in out:         # some kind of error message
                    sys.stdout.write("\n{0}Out[{1}]{2} {3}{4}{5}\n".format(RED,cmd_count,RESET,RED2,out,RESET))    
                elif out:                  # not an error
                    sys.stdout.write("\n{0}Out[{1}] {2}{3}".format(BLUE,cmd_count,RESET,out))
                else:                      # no output 
                    sys.stdout.write("\n")

                cmd_count+=1                                        # count commands
                sys.stdout.write("{0}In [{1}] {2}".format(GREEN,cmd_count,RESET))

                input=""
                continue

        if not Arrow:    # if not an arrow key add to line
            input += char 

if __name__== "__main__":
    prompt()
