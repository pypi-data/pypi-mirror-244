# -*- coding: utf-8 -*-
from pydft import MoleculeBuilder,DFT

#
# Example: Calculate total electronic energy for CO using standard
#          settings.
#

CO = MoleculeBuilder().from_name("CO")
dft = DFT(CO, basis='sto3g')
en = dft.scf(1e-4)
print("Total electronic energy: %f Ht" % en)