import numpy as np
import math
class Point:
    def area(self,p,p1):
        a=np.array(p)
        b=np.array(p1)
        c=b-a
        d=math.hypot(c[0],c[1])
        return (d)
