# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:53:58 2020

@author: malot
"""

import tomopy
import pylab
import time


def main():
    #obj = tomopy.shepp3d()
    ang = tomopy.angles(180)
    #sim = tomopy.project(obj, ang)
    rec = tomopy.recon(sim, ang, algorithm='art')
    pylab.imshow(rec[64], cmap='gray')
    pylab.show()



if __name__ == '__main__':
    main()