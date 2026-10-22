import numpy as np
from PIL import Image
def runs(prof, gap):
    """segments of True in prof separated by >= gap False entries"""
    idx=np.where(prof)[0]
    if len(idx)==0: return []
    segs=[]; s=idx[0]; p=idx[0]
    for i in idx[1:]:
        if i-p>gap: segs.append((s,p)); s=i
        p=i
    segs.append((s,p)); return segs
def load(f):
    im=Image.open(f).convert('RGB'); g=np.asarray(im.convert('L'))
    return im,g
def rowsegs(g,gap,thr=245,x0=0,x1=None):
    m=g[:,x0:x1]<thr
    return runs(m.any(1),gap)
def colsegs(g,y0,y1,gap,thr=245):
    m=g[y0:y1]<thr
    return runs(m.any(0),gap)
