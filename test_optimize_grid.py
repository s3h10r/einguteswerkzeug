#!/usr/bin/env python3
from contactsheet import get_factors, get_optimized_grid
from contactsheet import euclid




for i in range(1,20): #test
    res = get_optimized_grid(i)
    if res:
        print(i,res)
        assert(res[0]*res[1] == i)
