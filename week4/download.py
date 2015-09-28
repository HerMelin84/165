import urllib

testfile = urllib.URLopener()
testfile.retrieve("http://www.uio.no/studier/emner/matnat/ifi/INF2220/h15/obligatoriske-oppgaver/oblig-1/dictionary.txt", "dictionary.txt")
