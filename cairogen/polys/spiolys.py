from . import Poly
from ..lines import Segment
import random as _random


class Spiolys:
    def __init__(self, poly, condPolys):
        self._poly_init = poly
        # fonction qui prend en argument deux polygones et qui les
        # valide
        self._condPolys = condPolys

    def sep(self):
        pts = self._poly_init.poly
        gone = len(pts)
        #
        polysValides = False
        while not polysValides:
            # on cherche deux points sur des segments différents
            indice_pt1 = _random.random() * gone
            indice_pt2 = _random.random() * gone
            while int(indice_pt2) == int(indice_pt1):
                indice_pt2 = _random.random() * gone
            #
            min_ind = min(indice_pt1, indice_pt2)
            max_ind = max(indice_pt1, indice_pt2)
            # on définit nos deux nouveaux points
            pt1 = Segment(pts[int(min_ind)],
                          pts[int(min_ind) + 1]).point(min_ind % 1)
            pt2 = Segment(pts[int(max_ind)],
                          pts[(int(max_ind) + 1) % gone]).point(max_ind % 1)
            # on définit nos deux nouveaux polygones
            # on part de pt1 (premier dans l'ordre des absc. curv.)
            # jusqu'à pt2
            poly1 = [pt1]
            i = 1
            while int(min_ind) + i < max_ind:
                poly1 += [pts[int(min_ind) + i]]
                i += 1
            poly1 += [pt2]
            gone_poly1 = len(poly1)
            # on part de pt2 et on arrive à pt1
            poly2 = [pt2]
            # 3 + gone + 1 côtés sur les deux polys
            # on en a déjà mis gone_poly1
            # et on en a aussi déjà 2  (pt1 et pt2)
            poly2 += [pts[(int(max_ind) + i) % gone]
                      for i in range(1, (3 + gone + 1) - gone_poly1 + 1 - 2)]
            poly2 += [pt1]
            polysValides = self._condPolys(poly1, poly2)
        #
        return (Spiolys(Poly(poly1), self._condPolys),
                Spiolys(Poly(poly2), self._condPolys))
        
