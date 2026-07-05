# Lirilì Larilà — cactus-elephant in sandals, running. Blender headless → assets/lirili.glb
# Run: blender --background --python models/lirili.py
# Face +Y forward, feet at z≈0, head near z≈3. Animated legs named LegL / LegR (hip origin).
import bpy, math, os, sys
from mathutils import Vector

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
for c in (bpy.data.meshes, bpy.data.materials):
    for x in list(c): c.remove(x)

def mat(n,rgb,rough=0.6,metal=0.0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value=(*rgb,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal; return m
CACT =mat('Cactus',(0.30,0.55,0.28),0.7)      # cactus green
CACTD=mat('CactusD',(0.20,0.40,0.19),0.75)    # darker ridge
SPINE=mat('Spine',(0.90,0.88,0.60),0.5)       # pale spines
ELE  =mat('Ele',(0.34,0.58,0.32),0.68)        # elephant head (matches cactus tone)
EAR  =mat('Ear',(0.40,0.63,0.36),0.7)
TUSK =mat('Tusk',(0.95,0.93,0.86),0.35)
WHITE=mat('White',(0.95,0.95,0.95),0.3)
BLACK=mat('Black',(0.03,0.03,0.03),0.4)
NAIL =mat('Nail',(0.94,0.92,0.84),0.4)
SANDAL=mat('Sandal',(0.42,0.28,0.16),0.6)     # leather sandal
SOLE =mat('Sole',(0.25,0.18,0.11),0.6)
LEGM =mat('Leg',(0.30,0.55,0.28),0.7)

def a(): return bpy.context.active_object
def setmat(o,m): o.data.materials.clear(); o.data.materials.append(m)
def sel(o):
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
def smooth(o,s=2):
    if s: md=o.modifiers.new('s','SUBSURF'); md.levels=s; md.render_levels=s
    sel(o); bpy.ops.object.shade_smooth()
def applyxf(o): sel(o); bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
def sph(r,loc,seg=24,ri=16): bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=seg,ring_count=ri); return a()
def cyl(r,d,loc,v=20): bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=loc,vertices=v); return a()
def cube(s,loc): bpy.ops.mesh.primitive_cube_add(size=s,location=loc); return a()
def cone(r,d,loc,v=18): bpy.ops.mesh.primitive_cone_add(radius1=r,depth=d,location=loc,vertices=v); return a()
def join(objs,keep):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=keep; bpy.ops.object.join(); return keep
def set_origin(o,pt):
    bpy.context.scene.cursor.location=Vector(pt); sel(o); bpy.ops.object.origin_set(type='ORIGIN_CURSOR'); bpy.context.scene.cursor.location=Vector((0,0,0))

# ---- cactus torso (segmented saguaro trunk) ----
body=cyl(0.6,1.9,(0,0,1.55),28); setmat(body,CACT)
crown=sph(0.6,(0,0,2.5)); crown.scale=(1,1,0.7); applyxf(crown); setmat(crown,CACT)
body=join([body,crown],body); smooth(body,2)
# vertical ridge lines (darker thin cylinders around the trunk)
for i in range(6):
    ang=i*math.radians(60); rx=math.cos(ang)*0.58; ry=math.sin(ang)*0.58
    rg=cyl(0.05,1.7,(rx,ry,1.5),8); setmat(rg,CACTD); smooth(rg,1)
# spines (little pale cones poking out)
import random; random.seed(7)
for i in range(14):
    ang=random.random()*6.283; h=0.7+random.random()*1.6; r=0.6
    sx=math.cos(ang)*r; sy=math.sin(ang)*r
    sp=cone(0.04,0.18,(sx,sy,h),6); sp.rotation_euler=(math.radians(90),0,ang+math.radians(90)); applyxf(sp); setmat(sp,SPINE); smooth(sp,0)
# classic cactus side-arms (bend upward)
for s in (-1,1):
    a1=cyl(0.17,0.7,(s*0.7,0,1.7),14); setmat(a1,CACT)
    a2=cyl(0.15,0.6,(s*0.92,0,2.05),14); setmat(a2,CACT)
    A=join([a1,a2],a1); smooth(A,2); A.name='ArmL' if s<0 else 'ArmR'

# ---- elephant head on top ----
head=sph(0.62,(0,0.1,2.95),26,18); head.scale=(1.0,0.92,0.95); applyxf(head); setmat(head,ELE); smooth(head,2)
# big floppy ears
for s in (-1,1):
    ear=sph(0.42,(s*0.62,-0.05,2.95),18,12); ear.scale=(0.18,1.0,1.05); ear.rotation_euler=(0,0,math.radians(s*18)); applyxf(ear); setmat(ear,EAR); smooth(ear,1)
# trunk: shrinking spheres curving down-forward
tx=[(0,0.55,2.85,0.26),(0,0.78,2.62,0.22),(0,0.92,2.36,0.19),(0,1.0,2.1,0.16),(0,1.02,1.86,0.13)]
trunk=[]
for (x,y,z,r) in tx:
    t=sph(r,(x,y,z),16,12); setmat(t,ELE); trunk.append(t)
trunk=join(trunk,trunk[0]); smooth(trunk,2)
# tusks
for s in (-1,1):
    tu=cone(0.09,0.5,(s*0.24,0.55,2.55),10); tu.rotation_euler=(math.radians(70),0,0); applyxf(tu); setmat(tu,TUSK); smooth(tu,1)
# eyes
for s in (-1,1):
    e=sph(0.13,(s*0.3,0.5,3.1),14,10); setmat(e,WHITE); smooth(e,1)
    p=sph(0.07,(s*0.3,0.6,3.12),10,8); setmat(p,BLACK); smooth(p,1)

# ---- legs + sandals (animated) ----
for s in (-1,1):
    leg=cyl(0.18,1.0,(s*0.3,0,0.58),14); setmat(leg,LEGM)
    sandal=cube(0.5,(s*0.3,0.14,0.1)); sandal.scale=(0.52,1.05,0.22); applyxf(sandal); setmat(sandal,SANDAL)
    sole=cube(0.5,(s*0.3,0.16,0.02)); sole.scale=(0.56,1.1,0.1); applyxf(sole); setmat(sole,SOLE)
    strap=cyl(0.19,0.06,(s*0.3,0.05,0.2),12); strap.rotation_euler=(0,math.radians(90),0); applyxf(strap); setmat(strap,SANDAL)
    L=join([leg,sandal,sole,strap],leg); smooth(L,2)
    set_origin(L,(s*0.3,0,1.08))
    L.name='LegL' if s<0 else 'LegR'

# ---- export ----
root=None
for arg in sys.argv:
    if arg.endswith('lirili.py'): root=os.path.dirname(os.path.dirname(os.path.abspath(arg)))
if not root: root=os.getcwd()
out=os.path.join(root,'assets'); os.makedirs(out,exist_ok=True); path=os.path.join(out,'lirili.glb')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
print('EXPORTED', path)
print('OBJECTS', [o.name for o in bpy.data.objects])
