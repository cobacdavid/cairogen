import cairo as _cairo
import math as _math
import numpy as _np
from PIL import Image


def bg(img, color):
    ctx = _cairo.Context(img)
    ctx.save()
    f_col = ctx.set_source_rgba if len(color) == 4 else ctx.set_source_rgb
    f_col(*color)
    ctx.paint()
    ctx.restore()


def is_in(xy, poly):
    """Determine if the point is in the path.
    de https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
    Args:
    x -- x coordinate of point.
    y -- y coordinate of point.
    poly -- a list of tuples [(x, y), (x, y), ...]

    Returns:
      True if the point is in the poly
    """

    num = len(poly)
    i = 0
    j = num - 1
    c = False
    x, y = xy
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) *
                 (y - poly[i][1]) / (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c


def est_inclus_dans(p, q):
    pbis = enrichir_chemin(p)
    dansq = True
    i = 0
    while dansq and i < len(pbis):
        dansq = is_in(pbis[i], q)
        i += 1
    return dansq


def enrichir_chemin(p, N=19, T=100):
    # N = 9 pour T = 100 unités de distance
    # 9 pts supp -> segment coupé en 10
    q = []
    np = len(p)
    for i in range(np):
        A = p[i]
        B = p[(i + 1) % np]
        q.append(A)
        d = dist(A, B)
        # pour éviter 0, on ajoute .5
        n = round(d / T + .5) * N
        for i in range(n):
            q.append((A[0] + (i + 1) / (n + 1) * (B[0] - A[0]),
                      A[1] + (i + 1) / (n + 1) * (B[1] - A[1])))
    return q


def est_separe(p, q):
    pbis = enrichir_chemin(p)
    dansq = False
    i = 0
    while not dansq and i < len(pbis):
        dansq = is_in(*pbis[i], q)
        i += 1

    if dansq:
        return False

    qbis = enrichir_chemin(q)
    dansp = False
    i = 0
    while not dansp and i < len(qbis):
        dansp = is_in(*qbis[i], p)
        i += 1

    return not dansp


def dist(A, B):
    return sum((b - a) ** 2 for a, b in zip(A, B)) ** .5


def aire(tab_pts):
    """https://fr.wikipedia.org/wiki/Aire_d%27un_polygone
    """
    n = len(tab_pts)
    # on ferme le chemin si ce n'est pas fait
    x1, y1 = tab_pts[0]
    x2, y2 = tab_pts[-1]
    if not _math.isclose(x1, x2) or not _math.isclose(y1, y2):
        tab_pts += [tab_pts[0]]
    #
    n = len(tab_pts)
    x = [tab_pts[i][0] for i in range(n)]
    y = [tab_pts[i][1] for i in range(n)]
    somme = 0
    for i in range(n - 1):
        somme += (x[i]*y[i+1] - x[i+1]*y[i])
    # on enlève l'élément ajouté
    if len(tab_pts) > n:
        tab_pts.pop()
    #
    return abs(.5 * somme)


def midpoint(A, B):
    return tuple([(a + b) / 2 for a, b in zip(A, B)])


def image_noise(fichier, Wdest, Hdest):
    img = Image.open(fichier)
    img = img.convert("L").resize((Wdest, Hdest))
    img.save("nb.jpg")
    return _np.array(img)
