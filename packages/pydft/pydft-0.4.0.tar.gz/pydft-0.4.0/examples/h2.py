# -*- coding: utf-8 -*-
from pydft import MoleculeBuilder,DFT

#
# Example: Calculate total electronic energy for CO using standard
#          settings.
#

CO = MoleculeBuilder().from_name("H2")
dft = DFT(CO, basis='sto3g')
en = dft.scf(1e-4)
print("Total electronic energy: %f Ht" % en)