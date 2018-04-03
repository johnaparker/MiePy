"""
point sources
"""

import numpy as np
import miepy
from miepy.sources.source_base import source

#TODO: implement for any polarization
class point_dipole(source):
    def __init__(self, location, polarization, amplitude=1):
        super().__init__(amplitude)

        self.location = location

        polarization = np.asarray(polarization, dtype=np.complex)
        self.polarization = polarization
        self.polarization /= np.linalg.norm(polarization)
    
    #TODO: VSH should allow spherical=False or cartesian=True
    def E(self, r, k):
        N, _ = miepy.vsh.VSH(1,0)
        r, theta, phi = miepy.coordinates.cart_to_sph(*r, origin=self.location)
        N_cart = miepy.coordinates.vec_sph_to_cart(N(r, theta, phi, k), theta, phi) 
        return self.amplitude*N_cart

    def H(self, r, k):
        _, M = miepy.vsh.VSH(1,0)
        r, theta, phi = miepy.coordinates.cart_to_sph(*r, origin=self.location)
        return self.amplitude*M(r, theta, phi, k)

    def structure_of_mode(self, n, m, r, k):
        rad, theta, phi = miepy.coordinates.cart_to_sph(*r, origin=self.location)
        p = miepy.vsh.A_translation(m, n, 1, 0, rad, theta, phi, k,
                 mode=miepy.vsh.VSH_mode.outgoing)

        q = miepy.vsh.B_translation(m, n, 1, 0, rad, theta, phi, k,
                 mode=miepy.vsh.VSH_mode.outgoing)

        return (p,q)