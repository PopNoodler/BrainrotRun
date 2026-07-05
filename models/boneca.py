# Boneca Ambalabu — frog head on a tire body, human legs. Blender headless → assets/boneca.glb
# Run: blender --background --python models/boneca.py
# Face +Y forward, feet at z≈0, head near z≈2.9. Animated legs named LegL / LegR (hip origin).
import bpy, math, os, sys
from mathutils import Vector

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
for c in (bpy.data.meshes, bpy.data.materials):
    for x in list(c): c.remove(x)

def mat(n,rgb,rough=0.6,metal=0.0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value=(*rgb,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal; return m
FROG =mat('Frog',(0.36,0.62,0.26),0.6)
FROGD=mat('FrogD',(0.24,0.44,0.17),0.65)
BELLY=mat('FrogBelly',(0.80,0.82,0.55),0.55)
TIRE =mat('Tire',(0.07,0.07,0.08),0.75)
TREAD=mat('Tread',(0.02,0.02,0.03),0.8)
HUB  =mat('Hub',(0.55,0.57,0.62),0.35,0.8)
WHITE=mat('White',(0.96,0.96,0.96),0.3)
BLACK=mat('Black',(0.03,0.03,0.03),0.4)
MOUTH=mat('Mouth',(0.30,0.08,0.10),0.5)
SKIN =mat('Skin',(0.82,0.60,0.44),0.65)
SHOE =mat('Shoe',(0.14,0.12,0.16),0.5)

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
def torus(R,r,loc): bpy.ops.mesh.primitive_torus_add(major_radius=R,minor_radius=r,location=loc); return a()
def join(objs,keep):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=keep; bpy.ops.object.join(); return keep
def set_origin(o,pt):
    bpy.context.scene.cursor.location=Vector(pt); sel(o); bpy.ops.object.origin_set(type='ORIGIN_CURSOR'); bpy.context.scene.cursor.location=Vector((0,0,0))

# ---- tire torso (upright wheel facing +Y) ----
tire=torus(0.64,0.34,(0,0,1.5)); tire.rotation_euler=(math.radians(90),0,0); applyxf(tire); setmat(tire,TIRE); smooth(tire,2)
# tread blocks around the outer rim
for i in range(16):
    ang=i*math.radians(22.5); tx=math.cos(ang)*0.96; tz=1.5+math.sin(ang)*0.96
    tb=cube(0.5,(tx,0,tz)); tb.scale=(0.12,0.42,0.12); tb.rotation_euler=(0,ang,0); applyxf(tb); setmat(tb,TREAD); smooth(tb,0)
# hubcap both faces
for yy in (-0.28,0.28):
    hub=cyl(0.3,0.1,(0,yy,1.5),18); hub.rotation_euler=(math.radians(90),0,0); applyxf(hub); setmat(hub,HUB); smooth(hub,1)
    for k in range(5):
        ang=k*math.radians(72); bx=math.cos(ang)*0.16; bz=1.5+math.sin(ang)*0.16
        bolt=cyl(0.03,0.14,(bx,yy,bz),8); bolt.rotation_euler=(math.radians(90),0,0); applyxf(bolt); setmat(bolt,BLACK); smooth(bolt,0)

# ---- frog head on top ----
head=sph(0.5,(0,0.05,2.42),26,18); head.scale=(1.05,0.95,0.85); applyxf(head); setmat(head,FROG); smooth(head,2)
chin=sph(0.4,(0,0.28,2.28),18,12); chin.scale=(1.0,0.7,0.6); applyxf(chin); setmat(chin,BELLY); smooth(chin,1)
# bulging eyes on top (classic frog)
for s in (-1,1):
    bump=sph(0.26,(s*0.3,0.0,2.82),18,12); setmat(bump,FROG); smooth(bump,1)
    e=sph(0.2,(s*0.3,0.05,2.9),16,12); setmat(e,WHITE); smooth(e,1)
    p=sph(0.1,(s*0.3,0.18,2.96),12,8); setmat(p,BLACK); smooth(p,1)
# wide mouth (flattened dark torus arc)
mouth=torus(0.34,0.06,(0,0.4,2.3)); mouth.rotation_euler=(math.radians(78),0,0); mouth.scale=(1,0.5,1); applyxf(mouth); setmat(mouth,MOUTH); smooth(mouth,1)
# nostrils
for s in (-1,1):
    n=sph(0.04,(s*0.1,0.46,2.5),8,6); setmat(n,FROGD); smooth(n,0)
# little arms
for s in (-1,1):
    arm=cyl(0.1,0.6,(s*0.66,0.1,1.7),12); arm.rotation_euler=(math.radians(20),0,math.radians(s*30)); applyxf(arm); setmat(arm,FROG)
    hand=sph(0.13,(s*0.84,0.18,1.45),10,8); setmat(hand,FROG)
    A=join([arm,hand],arm); smooth(A,2); A.name='ArmL' if s<0 else 'ArmR'

# ---- human legs + shoes (animated) ----
for s in (-1,1):
    thigh=cyl(0.17,0.7,(s*0.26,0,0.82),14); setmat(thigh,SKIN)
    shin=cyl(0.14,0.6,(s*0.26,0,0.36),14); setmat(shin,SKIN)
    shoe=cube(0.5,(s*0.26,0.16,0.09)); shoe.scale=(0.46,1.0,0.34); applyxf(shoe); setmat(shoe,SHOE)
    L=join([thigh,shin,shoe],thigh); smooth(L,2)
    set_origin(L,(s*0.26,0,1.12))
    L.name='LegL' if s<0 else 'LegR'

# ---- export ----
root=None
for arg in sys.argv:
    if arg.endswith('boneca.py'): root=os.path.dirname(os.path.dirname(os.path.abspath(arg)))
if not root: root=os.getcwd()
out=os.path.join(root,'assets'); os.makedirs(out,exist_ok=True); path=os.path.join(out,'boneca.glb')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
print('EXPORTED', path)
print('OBJECTS', [o.name for o in bpy.data.objects])
