import os
from dynamoData import *
#test to make sure we're creating plotting data files for our plotting function to later parse

#assume we start initially without our dat files

#create .dat files with makeDat function in dynamoData
def test_DatFiles():
    makeDat("lineDLG.dat","dlg","lineLog")
    makeDat("capDLG.dat","dlg","capacityLog")

    makeDat("lineCarrillo.dat","carrillo","lineLog")
    makeDat("capCarrillo.dat","carrillo","capacityLog")

    makeDat("lineOrtega.dat","ortega","lineLog")
    makeDat("capOrtega.dat","ortega","capacityLog")

    assert os.path.exists('lineDLG.dat')
    assert os.path.exists('capDLG.dat')
    assert os.path.exists('lineCarrillo.dat')
    assert os.path.exists('capCarrillo.dat')
    assert os.path.exists('lineOrtega.dat')
    assert os.path.exists('capOrtega.dat')

#now remove the dat files for future testing
os.remove('lineDLG.dat')
os.remove('capDLG.dat')
os.remove('lineCarrillo.dat')
os.remove('capCarrillo.dat')
os.remove('lineOrtega.dat')
os.remove('capOrtega.dat')
