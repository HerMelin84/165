pattern='.+(http:.*.xml?)'
line='101	Asak kirke	55	Kyrkje	Kirke	Church	Halden	Ã˜stfold	59.14465	11.45458		http://www.yr.no/stad/Noreg/Ã˜stfold/Halden/Asak_kirke/varsel.xml	http://www.yr.no/sted/Norge/Ã˜stfold/Halden/Asak_kirke/varsel.xml	http://www.yr.no/place/Norway/Ã˜stfold/Halden/Asak_kirke/forecast.xml
101	Berg kirke	36	Kyrkje	Kirke	Church	Halden	Ã˜stfold	59.13783	11.32945		http://www.yr.no/stad/Noreg/Ã˜stfold/Halden/Berg_kirke/varsel.xml	http://www.yr.no/sted/Norge/Ã˜stfold/Halden/Berg_kirke/varsel.xml	http://www.yr.no/place/Norway/Ã˜stfold/Halden/Berg_kirke/forecast.xml'
print e.match(patterns,line).group(1)
