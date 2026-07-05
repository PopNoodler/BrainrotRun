# Generate a raster PNG app icon (gradient bg + Italian tricolore tile) headlessly via Blender.
# Run: blender --background --python models/icon.py   → assets/icon-512.png + icon-192.png
import bpy, os, sys

def lerp(a,b,t): return a+(b-a)*t

def in_round_rect(x,y,x0,y0,w,h,rad):
    if x<x0 or x>=x0+w or y<y0 or y>=y0+h: return False
    if (x<x0+rad or x>=x0+w-rad) and (y<y0+rad or y>=y0+h-rad):
        cx = x0+rad if x<x0+rad else x0+w-1-rad
        cy = y0+rad if y<y0+rad else y0+h-1-rad
        return (x-cx)**2+(y-cy)**2 <= rad*rad
    return True

def render(size):
    W=H=size; s=size/512.0
    fw=int(270*s); fh=int(182*s); fx0=(W-fw)//2; fy0=(H-fh)//2; rad=int(26*s)
    px=[0.0]*(W*H*4)
    for y in range(H):
        tg=y/(H-1)                                   # 0 bottom → 1 top
        bg=(lerp(0.04,0.24,tg), lerp(0.055,0.14,tg), lerp(0.10,0.45,tg))
        for x in range(W):
            r,g,b=bg
            if in_round_rect(x,y,fx0,fy0,fw,fh,rad):
                rel=(x-fx0)/fw
                if   rel<1/3: r,g,b=0.22,0.66,0.34   # green
                elif rel<2/3: r,g,b=0.96,0.96,0.96   # white
                else:         r,g,b=0.88,0.26,0.22   # red
            i=(y*W+x)*4; px[i]=r; px[i+1]=g; px[i+2]=b; px[i+3]=1.0
    img=bpy.data.images.new('icon%d'%size, W, H); img.pixels=px
    root=None
    for a in sys.argv:
        if a.endswith('icon.py'): root=os.path.dirname(os.path.dirname(os.path.abspath(a)))
    if not root: root=os.getcwd()
    out=os.path.join(root,'assets'); os.makedirs(out,exist_ok=True)
    path=os.path.join(out,'icon-%d.png'%size); img.filepath_raw=path; img.file_format='PNG'; img.save()
    print('SAVED', path)

render(512); render(192)
