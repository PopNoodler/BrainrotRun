# Tung Tung Tung Sahur — Blender headless model → GLB
# Run: blender --background --python models/sahur.py
# Output: assets/sahur.glb   (Blender Z-up; glTF export converts to Y-up for three.js)
# Animated parts are named LegL / LegR (origin at hip) so the game can swing them.
import bpy, math, os, sys
from mathutils import Vector

# ---------- clean ----------
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
for c in (bpy.data.meshes, bpy.data.materials):
    for x in list(c): c.remove(x)

def mat(name, rgb, rough=0.72, metal=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value=(*rgb,1.0)
    b.inputs['Roughness'].default_value=rough
    b.inputs['Metallic'].default_value=metal
    return m
WOOD =mat('Wood',(0.60,0.38,0.19),0.75)
WOODD=mat('WoodD',(0.40,0.25,0.12),0.82)
BATM =mat('Bat',(0.56,0.37,0.19),0.62)
WHITE=mat('White',(0.94,0.94,0.92),0.32)
BLACK=mat('Black',(0.04,0.03,0.02),0.45)
REDM =mat('Mouth',(0.34,0.06,0.06),0.5)
CLOTH=mat('Cloth',(0.90,0.87,0.78),0.9)
BROW =mat('Brow',(0.18,0.10,0.05),0.8)

def active(): return bpy.context.active_object
def setmat(o,m): o.data.materials.clear(); o.data.materials.append(m)
def sel(o):
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
def smooth(o,subd=2):
    if subd:
        md=o.modifiers.new('subd','SUBSURF'); md.levels=subd; md.render_levels=subd
    sel(o); bpy.ops.object.shade_smooth()
def applyxf(o):
    sel(o); bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
def cyl(r,d,loc,v=24): bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=loc,vertices=v); return active()
def sph(r,loc,s=22,ri=14): bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=s,ring_count=ri); return active()
def cube(sz,loc): bpy.ops.mesh.primitive_cube_add(size=sz,location=loc); return active()
def torus(R,r,loc): bpy.ops.mesh.primitive_torus_add(major_radius=R,minor_radius=r,location=loc); return active()
def join(objs,keep):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=keep; bpy.ops.object.join(); return keep
def set_origin(o,pt):
    bpy.context.scene.cursor.location=Vector(pt); sel(o); bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location=Vector((0,0,0))

# ---------- body (feet at z≈0, head near z≈3), face toward +Y ----------
body=cyl(0.60,2.0,(0,0,1.55),28); setmat(body,WOOD)
# round the top of the log
crown=sph(0.60,(0,0,2.62)); crown.scale=(1,1,0.82); applyxf(crown); setmat(crown,WOOD)
body=join([body,crown],body); smooth(body,2)
# sahur head-wrap band
band=torus(0.58,0.13,(0,0,2.32)); setmat(band,CLOTH); smooth(band,1)
knot=sph(0.13,(0,-0.55,2.34)); setmat(knot,CLOTH); smooth(knot,1)  # knot at back
# ---------- face ----------
face=[]
for i,ex in enumerate((-0.27,0.27)):
    e=sph(0.20,(ex,0.48,2.02),20,14); setmat(e,WHITE); face.append(e)
    p=sph(0.10,(ex*0.92,0.63,2.0),14,10); setmat(p,BLACK); face.append(p)
    hl=sph(0.035,(ex*0.92-0.05,0.66,2.07),8,6); setmat(hl,WHITE); face.append(hl)
    br=cube(0.2,(ex,0.5,2.30)); br.scale=(1.8,0.5,0.42); br.rotation_euler=(0, math.radians(28 if ex<0 else -28),0); applyxf(br); setmat(br,BROW); face.append(br)
mouth=sph(0.25,(0,0.50,1.6),18,12); mouth.scale=(1.05,0.55,0.85); applyxf(mouth); setmat(mouth,REDM); face.append(mouth)
for t in (-1,1):
    th=cube(0.16,(t*0.09,0.66,1.74)); th.scale=(0.8,0.35,0.5); applyxf(th); setmat(th,WHITE); face.append(th)  # teeth
for f in face: smooth(f,1)
# ---------- legs (animated): join leg+foot, origin at hip ----------
for s in (-1,1):
    leg=cyl(0.17,1.0,(s*0.28,0,0.5),16); setmat(leg,WOODD)
    foot=cube(0.5,(s*0.28,0.14,0.08)); foot.scale=(0.52,1.0,0.34); applyxf(foot); setmat(foot,WOODD)
    L=join([leg,foot],leg); smooth(L,2)
    set_origin(L,(s*0.28,0,1.0))       # pivot at hip
    L.name='LegL' if s<0 else 'LegR'
# ---------- arms (static pose): join arm+hand ----------
for s in (-1,1):
    arm=cyl(0.15,0.95,(s*0.70,0,1.5),16); setmat(arm,WOODD)
    hand=sph(0.19,(s*0.70,0,1.02),14,10); setmat(hand,WOODD)
    A=join([arm,hand],arm); smooth(A,2)
    A.rotation_euler=(0,0,math.radians(s*22)); applyxf(A)
    A.name='ArmL' if s<0 else 'ArmR'
# ---------- baseball bat in right hand ----------
handle=cyl(0.09,0.3,(0.95,0.15,1.02),12); setmat(handle,WOODD)
barrel=cyl(0.15,1.3,(0.95,0.15,1.75),14); barrel.scale=(1,1,1); setmat(barrel,BATM)
bat=join([handle,barrel],barrel); smooth(bat,2)
bat.rotation_euler=(math.radians(18),0,0); applyxf(bat); bat.name='Bat'

# ---------- export ----------
here=os.path.dirname(os.path.abspath(bpy.data.filepath)) if bpy.data.filepath else os.getcwd()
# resolve project root from this script's dir
root=None
for a in sys.argv:
    if a.endswith('sahur.py'): root=os.path.dirname(os.path.dirname(os.path.abspath(a)))
if not root: root=os.getcwd()
out=os.path.join(root,'assets'); os.makedirs(out, exist_ok=True)
path=os.path.join(out,'sahur.glb')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
print('EXPORTED', path)
names=[o.name for o in bpy.data.objects]
print('OBJECTS', names)
