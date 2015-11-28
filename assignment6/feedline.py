import sys,os
from getchar import getchar
from StringIO import StringIO
from subprocess import Popen




def feedline(command, namespace=vars().copy(), buffer=None):
    """
    Feedline function that executes the command and returns the output.
    ! Will execute a sh command. 
    ? Will execute a help command
    % Will save the the buffer parameter to a given file.
    
    Args:
        command (string): the command to be executed.
        namespace (dict): dictionary equal to the existing namespace. 
        buffer (list): A list of previously typed commands
    Returns:
        The output of the command, both on error and success.

    """
    # Swap stdout with a StringIO instance
    oldio, sys.stdout = sys.stdout, StringIO()
    if command[0]=='!':     # it's a 'magic' command. shell-command that is. 
        try:
            Popen(command[1:],shell=True,stderr=oldio)
        except Exception as e:
            return "{}\n".format(sys.exc_info())
    elif command[0]=='?':   # It's a help command.
        try:
            command=command[1:]
            exec("help({})".format(command), namespace)
        except Exception as e:
            sys.stdout = oldio
            return "{}\n".format(sys.exc_info())
    elif '%save' in command:# it's the save command.
        sys.stdout = oldio
        return savefile(command,buffer)
        
    else:                   # regular python command. 
        try:
            if '=' in command:
                newargs=command.replace(" ","")      # remove spaces.
                newargs=newargs.split("=")           # split on the equal sight. 
                namespace[newargs[0]]=newargs[1]     # add the left expression to the namespace.
                if type(newargs[1])==int:            # check if it's an int.
                    command=command.replace(newargs[0],"int({})".format(newargs[1]))                    
                elif type(newargs[1])==float:        # check if it's a float. 
                    command=command.replace(newargs[0],"float({})".format(newargs[1]))                    
            exec(command, namespace)                 # execute. 
        except Exception as e:                       # error. 
            sys.stdout = oldio
            return "{}\n".format(sys.exc_info())     # return error. 
                                                     # Get stdout buffer
    out = sys.stdout.getvalue()                      # It was not an error
                                                     # Reset stdout
    sys.stdout = oldio                               # swap back. 
                                                     # return captured stdout
    return out


def savefile(command,buffer):
    """
    Function that saves the buffer to the given filename.
    !!! This overwrites the current file. 
    
    Args:
        command (string): the save command containing the filename
        buffer (list): the buffer to be saved.
    Returns:
        If the save was successful or not.
    """
    if len(command)<7:          # Should at least be 7 characters long.
        return "Error: Session was not saved.\n"
    filename=command[6:]        # Get the filename
    file = open(filename, 'w+') # open file, w+ means overwriting it if it exists.
    file.write(buffer)          # write to file
    file.close()                # close.
    return "Session was saved to {}.\n".format(filename)

if __name__ == "__main__":
    import doctest
    doctest.testmod()


