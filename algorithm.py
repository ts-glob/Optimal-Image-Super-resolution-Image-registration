# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 01:49:43 2020

@author: tsoyg
"""

import искажение
import восстановление
import увеличение
import согласование
import комплексирование


def process():
    искажение.distortion()
    восстановление.filtration()
    увеличение.expansion()
    согласование.registration()
    комплексирование.restoration()
