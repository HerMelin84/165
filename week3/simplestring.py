class SimpleString():
    """
    SimpleString encapsules a string.
    """

    def __init__(self):
        """
        Construct new 'SimpleString' object.

        :param string: The string.
        """
        self.string=''
    def getString(self):
        """
        Sets value to 'string' through the commandline(raw_inpu())
        """
        self.string = raw_input("Enter String value: ")
    def printString(self):
        """
        Prints the string value in upper case
        """
        if(self.string!= ''):
            print self.string.upper()
        else:
            print "You have not given it a value yet!"
