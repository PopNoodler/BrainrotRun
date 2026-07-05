# Tralalero Tralala — blue shark on sneakers. Blender headless → assets/tralalero.glb
# Run: blender --background --python models/tralalero.py
import bpy, math, os, sys
from mathutils import Vector

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
for c in (bpy.data.meshes, bpy.data.materials):
    for x in list(c): c.remove(x)

def mat(n,rgb,rough=0.6,metal=0.0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value=(*rgb,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal; return m
SHARK=mat('Shark',(0.32,0.48,0.62),0.55)
BELLY=mat('Belly',(0.88,0.90,0.92),0.5)
TOOTH=mat('Tooth',(0.96,0.96,0.94),0.3)
MOUTH=mat('Mouth',(0.30,0.05,0.08),0.5)
WHITE=mat('White',(0.95,0.95,0.95),0.3)
BLACK=mat('Black',(0.03,0.03,0.03),0.4)
SNEAK=mat('Sneaker',(0.13,0.34,0.85),0.5)
SOLE =mat('Sole',(0.95,0.95,0.95),0.5)
LEGM =mat('Leg',(0.55,0.45,0.38),0.7)

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

# ---- shark body (long along +Y = forward), standing ~1.5 up on legs ----
body=sph(0.8,(0,0,1.7)); body.scale=(0.9,1.7,0.95); applyxf(body); setmat(body,SHARK)
belly=sph(0.62,(0,0.1,1.45)); belly.scale=(0.85,1.5,0.6); applyxf(belly); setmat(belly,BELLY)
snout=cone(0.5,0.9,(0,1.5,1.75)); snout.rotation_euler=(math.radians(90),0,0); applyxf(snout); setmat(snout,SHARK)
body=join([body,belly,snout],body); smooth(body,2)
# mouth (dark) + teeth
mouth=sph(0.42,(0,1.15,1.5),18,12); mouth.scale=(0.9,0.7,0.5); applyxf(mouth); setmat(mouth,MOUTH); smooth(mouth,1)
teeth=[]
for i in range(6):
    t=cone(0.06,0.16,(-0.3+i*0.12,1.45,1.62),8); t.rotation_euler=(math.radians(180),0,0); applyxf(t); setmat(t,TOOTH); teeth.append(t)
    t2=cone(0.06,0.16,(-0.3+i*0.12,1.45,1.4),8); applyxf(t2); setmat(t2,TOOTH); teeth.append(t2)
for t in teeth: smooth(t,0)
# eyes
for ex in (-0.42,0.42):
    e=sph(0.16,(ex,0.95,2.05),16,12); setmat(e,WHITE); smooth(e,1)
    p=sph(0.09,(ex*1.05,1.06,2.08),12,8); setmat(p,BLACK); smooth(p,1)
# dorsal fin (top)
dorsal=cone(0.5,1.1,(0,-0.1,2.55),4); dorsal.rotation_euler=(math.radians(-18),0,math.radians(45)); dorsal.scale=(0.15,1,1); applyxf(dorsal); setmat(dorsal,SHARK); smooth(dorsal,1)
# tail
tail=cone(0.7,1.0,(0,-1.7,1.9),4); tail.rotation_euler=(math.radians(90),0,math.radians(45)); tail.scale=(0.18,1,1); applyxf(tail); setmat(tail,SHARK); smooth(tail,1)
# pectoral fins
for s in (-1,1):
    f=cone(0.45,0.9,(s*0.75,0.4,1.4),4); f.rotation_euler=(math.radians(90),0,math.radians(45)); f.scale=(0.14,1,0.8); f.rotation_euler=(0,math.radians(s*60),math.radians(20)); applyxf(f); setmat(f,SHARK); smooth(f,1)
# ---- legs + blue sneakers (animated) ----
for s in (-1,1):
    leg=cyl(0.16,1.0,(s*0.32,0,0.6),14); setmat(leg,LEGM)
    shoe=cube(0.5,(s*0.32,0.18,0.12)); shoe.scale=(0.5,1.05,0.4); applyxf(shoe); setmat(shoe,SNEAK)
    sole=cube(0.5,(s*0.32,0.2,0.03)); sole.scale=(0.54,1.1,0.14); applyxf(sole); setmat(sole,SOLE)
    L=join([leg,shoe,sole],leg); smooth(L,2)
    set_origin(L,(s*0.32,0,1.1))
    L.name='LegL' if s<0 else 'LegR'

# ---- export ----
root=None
for arg in sys.argv:
    if arg.endswith('tralalero.py'): root=os.path.dirname(os.path.dirname(os.path.abspath(arg)))
if not root: root=os.getcwd()
out=os.path.join(root,'assets'); os.makedirs(out,exist_ok=True); path=os.path.join(out,'tralalero.glb')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
print('EXPORTED', path)
