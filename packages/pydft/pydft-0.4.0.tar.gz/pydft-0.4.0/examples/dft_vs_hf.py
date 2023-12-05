# -*- coding: utf-8 -*-

from pydft import MoleculeBuilder, DFT

co = MoleculeBuilder().get_molecule("CO")
dft = DFT(co, basis='sto3g')
en = dft.scf(1e-4)
print("Total electronic energy: %f Ht" % en)

res = dft.get_matrices()
print(res.keys())