# Re-create in-game three.js buildX() specs in Blender and render a PNG to inspect likeness.
# Approximate (shading differs from WebGL) but silhouette/proportion transfer.
# Run: blender --background --python models/render_preview.py -- <name>   (name: sahur|tralalero)
import bpy, math, os, sys
from mathutils import Vector

NAME = 'tralalero'
if '--' in sys.argv:
    extra = sys.argv[sys.argv.index('--')+1:]
    if extra: NAME = extra[0]

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
for c in (bpy.data.meshes, bpy.data.materials):
    for x in list(c): c.remove(x)

def mat(n, rgb):
    m = bpy.data.materials.new(n); m.use_nodes=True
    m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*rgb,1)
    m.diffuse_color=(*rgb,1)
    return m
WOOD=mat('wood',(0.79,0.54,0.31)); WOODD=mat('woodD',(0.54,0.34,0.19))
WHITE=mat('white',(0.95,0.95,0.94)); BLACK=mat('black',(0.06,0.05,0.04))
MOUTH=mat('mouth',(0.29,0.06,0.06)); BROW=mat('brow',(0.23,0.14,0.07))
BLUE=mat('blue',(0.25,0.5,0.75)); BELLY=mat('belly',(0.88,0.9,0.92))
TOOTH=mat('tooth',(0.96,0.96,0.94)); SNEAK=mat('sneak',(0.18,0.43,0.94)); SOLE=mat('sole',(0.95,0.95,0.95))
CROC=mat('croc',(0.3,0.48,0.23)); CROCD=mat('crocD',(0.2,0.35,0.16)); CROCB=mat('crocB',(0.85,0.82,0.66))
METAL=mat('metal',(0.54,0.57,0.6)); BOOT=mat('boot',(0.1,0.1,0.12))
CACT=mat('cact',(0.3,0.6,0.27)); CACTD=mat('cactD',(0.2,0.44,0.17)); SPINE=mat('spine',(0.9,0.88,0.56))
ELE=mat('ele',(0.35,0.63,0.31)); TUSK=mat('tusk',(0.95,0.93,0.87)); SKIN=mat('skin',(0.82,0.6,0.44))

def T(x,y,z): return (x, -z, y)          # three.js (Y-up, faces +Z) -> Blender (Z-up, faces -Y)
def setm(o,m): o.data.materials.clear(); o.data.materials.append(m)
def sph(r,loc,sc=None,m=WOOD):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=T(*loc)); o=bpy.context.active_object
    if sc: o.scale=(sc[0],sc[2],sc[1])   # three (sx,sy,sz)->blender (sx,sz,sy)
    bpy.ops.object.shade_smooth(); setm(o,m); return o
def cyl(r,d,loc,m=WOOD,rot=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=T(*loc)); o=bpy.context.active_object
    if rot: o.rotation_euler=rot
    bpy.ops.object.shade_smooth(); setm(o,m); return o
def cone(r,d,loc,m=WOOD,rot=None,sc=None):
    bpy.ops.mesh.primitive_cone_add(radius1=r,depth=d,location=T(*loc)); o=bpy.context.active_object
    if sc: o.scale=(sc[0],sc[2],sc[1])
    if rot: o.rotation_euler=rot
    bpy.ops.object.shade_smooth(); setm(o,m); return o
def box(w,h,d,loc,m=WOOD,rz=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=T(*loc)); o=bpy.context.active_object
    o.scale=(w,d,h)
    if rz: o.rotation_euler=(0,0,rz)
    setm(o,m); return o

def build_sahur():
    cyl(0.46,1.9,(0,1.75,0),WOOD); sph(0.46,(0,0.85,0),m=WOOD); sph(0.47,(0,2.78,0),(1,0.72,1),WOOD)
    for ex in (-0.22,0.22):
        sph(0.17,(ex,2.22,0.36),m=WHITE); sph(0.085,(ex*0.92,2.2,0.5),m=BLACK); sph(0.03,(ex*0.92-0.04,2.26,0.55),m=WHITE)
        box(0.3,0.08,0.09,(ex,2.44,0.36),BROW,rz=(0.5 if ex<0 else -0.5))
    sph(0.22,(0,1.86,0.36),(1,0.8,0.5),MOUTH)
    box(0.3,0.06,0.04,(0,1.97,0.5),WHITE); box(0.3,0.06,0.04,(0,1.76,0.5),WHITE)
    for s in (-1,1):
        cyl(0.12,0.72,(s*0.56,1.75,0),WOODD,rot=(0,s*0.9,0)); sph(0.16,(s*0.78,1.28,0),m=WOODD)
    cyl(0.13,1.1,(0.85,1.5,0.2),WOODD,rot=(math.radians(30),0,0))
    for s in (-1,1):
        cyl(0.14,0.7,(s*0.24,0.45,0),WOODD); box(0.24,0.15,0.46,(s*0.24,0.1,0.12),WOODD)

def build_tralalero():
    # streamlined torpedo shark body (long snout->tail), belly, pointed snout
    sph(0.68,(0,1.8,-0.1),(0.8,0.95,2.5),BLUE)
    sph(0.5,(0,1.55,0.5),(0.74,0.8,1.8),BELLY)
    cone(0.4,1.2,(0,1.75,1.75),BLUE,rot=(math.radians(90),0,0))              # long pointed snout (front)
    # mouth + teeth (front underside)
    sph(0.4,(0,1.55,1.2),(0.95,0.55,0.55),MOUTH)
    for i in range(6):
        tx=-0.28+i*0.112
        cone(0.05,0.15,(tx,1.66,1.4),TOOTH,rot=(math.radians(90),0,0))
        cone(0.05,0.13,(tx,1.46,1.38),TOOTH,rot=(math.radians(-90),0,0))
    # eyes (upper front head)
    for ex in (-0.34,0.34):
        sph(0.14,(ex,2.02,0.8),m=WHITE); sph(0.07,(ex,2.04,0.9),m=BLACK)
    # dorsal fin (mid-back top) + big caudal tail + pectoral fins
    cone(0.5,1.05,(0,2.5,-0.1),BLUE,sc=(0.28,1,1))
    cone(0.62,1.15,(0,1.95,-1.95),BLUE,sc=(0.24,1.15,1))
    for s in (-1,1):
        cone(0.42,0.95,(s*0.66,1.5,0.35),BLUE,rot=(0,0,math.radians(s*62)),sc=(0.22,1,0.85))
    # legs + blue sneakers
    for s in (-1,1):
        cyl(0.16,1.0,(s*0.32,0.6,-0.1),BLUE); box(0.34,0.22,0.62,(s*0.32,0.14,0.08),SNEAK); box(0.38,0.1,0.68,(s*0.32,0.04,0.1),SOLE)

def build_bombardiro():
    # chunky military-green croc torso
    cyl(0.52,1.2,(0,1.7,0),CROC); sph(0.52,(0,1.15,0),m=CROC); sph(0.5,(0,2.3,0.05),(1,0.95,1),CROC)
    sph(0.4,(0,1.55,0.42),(0.7,1.1,0.4),CROCB)
    for i in range(4): cone(0.12,0.22,(0,1.1+i*0.42,-0.5),CROCD,sc=(0.5,1,1))
    # bomber wings + engines + tail fin
    for s in (-1,1):
        box(1.7,0.13,0.55,(s*1.0,1.7,-0.1),METAL); sph(0.15,(s*0.95,1.48,-0.1),m=BOOT)
    box(0.12,0.7,0.55,(0,2.35,-0.6),METAL)
    # big crocodile head + LONG toothy snout jutting forward (the signature)
    sph(0.5,(0,2.55,0.15),(0.95,0.85,0.95),CROC)
    box(0.56,0.3,1.7,(0,2.5,1.0),CROC)                  # upper snout (long)
    box(0.5,0.16,1.5,(0,2.28,0.95),CROC)                # lower jaw
    box(0.44,0.06,1.35,(0,2.4,0.95),CROCD)              # dark mouth line
    for i in range(8):
        z=0.4+i*0.17
        cone(0.045,0.14,(0.18,2.42,z),TOOTH,rot=(math.radians(180),0,0)); cone(0.045,0.14,(-0.18,2.42,z),TOOTH,rot=(math.radians(180),0,0))
        cone(0.045,0.12,(0.18,2.3,z),TOOTH); cone(0.045,0.12,(-0.18,2.3,z),TOOTH)
    for s in (-1,1):
        sph(0.15,(s*0.24,2.95,0.08),m=CROC); sph(0.11,(s*0.24,3.0,0.12),m=WHITE); sph(0.055,(s*0.24,3.02,0.2),m=BLACK)
    box(0.6,0.1,0.2,(0,2.86,0.2),CROCD)                 # goggle strap
    for s in (-1,1): sph(0.04,(s*0.12,2.56,1.78),m=CROCD)   # nostrils at snout tip
    for s in (-1,1):
        cyl(0.17,0.9,(s*0.3,0.5,0),CROC); box(0.3,0.2,0.6,(s*0.3,0.12,0.16),BOOT)

def build_lirili():
    # cactus torso + ridge lines + spines
    cyl(0.6,1.35,(0,1.7,0),CACT); sph(0.6,(0,1.02,0),m=CACT); sph(0.6,(0,2.38,0),m=CACT)
    for i in range(8):
        a=i*math.pi/4; cyl(0.07,1.75,(math.cos(a)*0.57,1.6,math.sin(a)*0.57),CACTD)
    for i in range(16):
        a=i*2.399; h=0.95+((i*0.13)%1.5)
        cone(0.045,0.18,(math.cos(a)*0.63,h,math.sin(a)*0.63),SPINE,rot=(0,0,math.radians(90)))
    # cactus side-arms (up, saguaro)
    for s in (-1,1):
        cyl(0.15,0.5,(s*0.72,1.75,0),CACT); cyl(0.13,0.4,(s*0.92,2.15,0),CACT)
    # elephant head + ears + trunk + tusks + eyes
    sph(0.56,(0,2.85,0.05),(1,0.92,0.95),ELE)
    for s in (-1,1): sph(0.42,(s*0.62,2.85,-0.05),(0.18,1,1),ELE)
    for i in range(5): sph(0.25-i*0.032,(0,2.78-i*0.24,0.5+i*0.11),m=ELE)
    for s in (-1,1): cone(0.08,0.45,(s*0.22,2.5,0.5),TUSK,rot=(math.radians(66),0,0))
    for ex in (-0.3,0.3):
        sph(0.12,(ex,3.0,0.42),m=WHITE); sph(0.06,(ex,3.02,0.51),m=BLACK)
    # legs + sandals
    for s in (-1,1):
        cyl(0.17,0.9,(s*0.3,0.5,0),CACT); box(0.28,0.14,0.5,(s*0.3,0.1,0.14),SKIN)

{'sahur':build_sahur,'tralalero':build_tralalero,'bombardiro':build_bombardiro,'lirili':build_lirili}.get(NAME, build_sahur)()

# ---- camera (track-to target) + light + workbench render ----
bpy.ops.object.empty_add(location=(0,0,1.4)); tgt=bpy.context.active_object
bpy.ops.object.camera_add(location=(4.2,-5.6,2.4)); cam=bpy.context.active_object
tc=cam.constraints.new('TRACK_TO'); tc.target=tgt; tc.track_axis='TRACK_NEGATIVE_Z'; tc.up_axis='UP_Y'
cam.data.lens=52; bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='SUN',location=(-4,-6,9)); bpy.context.active_object.data.energy=3.2
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='STUDIO'; sc.display.shading.color_type='MATERIAL'
sc.render.resolution_x=400; sc.render.resolution_y=460
sc.world=bpy.data.worlds.new('w'); sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.16,0.11,0.29,1)
root=None
for a in sys.argv:
    if a.endswith('render_preview.py'): root=os.path.dirname(os.path.dirname(os.path.abspath(a)))
if not root: root=os.getcwd()
sc.render.filepath=os.path.join(root,'assets','preview_%s.png'%NAME)
bpy.ops.render.render(write_still=True)
print('RENDERED', sc.render.filepath)
