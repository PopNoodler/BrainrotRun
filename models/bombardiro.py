# Bombardiro Crocodilo — crocodile-headed military bomber, running on booted legs.
# Blender headless → assets/bombardiro.glb    Run: blender --background --python models/bombardiro.py
# Face +Y forward, feet at z≈0, head near z≈3.1. Animated legs named LegL / LegR (hip origin).
import bpy, math, os, sys
from mathutils import Vector

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
for c in (bpy.data.meshes, bpy.data.materials):
    for x in list(c): c.remove(x)

def mat(n,rgb,rough=0.6,metal=0.0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value=(*rgb,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal; return m
CROC =mat('Croc',(0.28,0.42,0.20),0.62)     # military green scales
CROCD=mat('CrocD',(0.19,0.30,0.13),0.7)      # darker back ridge
BELLY=mat('Belly',(0.82,0.84,0.66),0.55)     # cream belly
TOOTH=mat('Tooth',(0.96,0.96,0.92),0.3)
MOUTH=mat('Mouth',(0.28,0.06,0.08),0.5)
WHITE=mat('White',(0.95,0.95,0.95),0.3)
BLACK=mat('Black',(0.03,0.03,0.03),0.4)
METAL=mat('Metal',(0.52,0.55,0.60),0.35,0.85)   # bomber wings / nose
STEEL=mat('Steel',(0.34,0.37,0.42),0.4,0.8)
BOOT =mat('Boot',(0.10,0.10,0.12),0.5)
GOGG =mat('Goggle',(0.55,0.38,0.18),0.45)        # aviator leather
GLASS=mat('Glass',(0.20,0.55,0.75),0.15,0.4)
BOMB =mat('Bomb',(0.16,0.17,0.20),0.45,0.6)

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

# ---- torso: upright bomber fuselage body (green croc) ----
body=sph(0.62,(0,0,1.72)); body.scale=(0.82,0.92,1.28); applyxf(body); setmat(body,CROC)
belly=sph(0.5,(0,0.42,1.6)); belly.scale=(0.7,0.4,1.05); applyxf(belly); setmat(belly,BELLY)
body=join([body,belly],body); smooth(body,2)
# back ridge scutes (dorsal bumps)
for i in range(4):
    sc=cone(0.13,0.2,(0,-0.5,1.15+i*0.42),4); sc.rotation_euler=(math.radians(90),0,math.radians(45)); sc.scale=(0.5,1,1); applyxf(sc); setmat(sc,CROCD); smooth(sc,1)

# ---- bomber WINGS (metal) out the sides + tail fin ----
for s in (-1,1):
    w=cube(0.5,(s*0.95,-0.05,1.75)); w.scale=(1.7,0.16,0.6); applyxf(w); setmat(w,METAL); smooth(w,0)
    tip=cone(0.16,0.4,(s*1.75,-0.05,1.75),4); tip.rotation_euler=(0,math.radians(s*90),0); applyxf(tip); setmat(tip,STEEL); smooth(tip,0)
    # under-wing bomb
    bmb=sph(0.16,(s*0.9,-0.05,1.5)); bmb.scale=(0.9,0.9,1.5); applyxf(bmb); setmat(bmb,BOMB); smooth(bmb,1)
    fin=cube(0.4,(s*0.55,-0.05,1.5)); fin.scale=(0.05,0.3,0.5); applyxf(fin); setmat(fin,STEEL); smooth(fin,0)
tailfin=cube(0.5,(0,-0.55,2.35)); tailfin.scale=(0.08,0.5,0.7); applyxf(tailfin); setmat(tailfin,METAL); smooth(tailfin,0)

# ---- crocodile HEAD with long snout ----
head=sph(0.5,(0,0.15,2.72)); head.scale=(0.82,1.05,0.72); applyxf(head); setmat(head,CROC)
snout_u=cube(0.5,(0,0.85,2.62)); snout_u.scale=(0.72,1.5,0.34); applyxf(snout_u); setmat(snout_u,CROC)
snout_l=cube(0.5,(0,0.8,2.4)); snout_l.scale=(0.66,1.35,0.24); applyxf(snout_l); setmat(snout_l,CROC)
head=join([head,snout_u,snout_l],head); smooth(head,2)
mouth=cube(0.5,(0,0.85,2.5)); mouth.scale=(0.6,1.3,0.06); applyxf(mouth); setmat(mouth,MOUTH); smooth(mouth,0)
# croc teeth (top + bottom rows)
teeth=[]
for i in range(7):
    tx=-0.28+i*0.093
    t=cone(0.05,0.16,(tx,0.5+i*0.02,2.53),6); t.rotation_euler=(math.radians(180),0,0); applyxf(t); setmat(t,TOOTH); teeth.append(t)
    b=cone(0.05,0.14,(tx,0.5+i*0.02,2.47),6); applyxf(b); setmat(b,TOOTH); teeth.append(b)
for t in teeth: smooth(t,0)
# raised eyes on top of head (croc style) + aviator goggles
for ex in (-0.28,0.28):
    socket=sph(0.19,(ex,0.05,3.02),16,12); socket.scale=(1,1,0.85); applyxf(socket); setmat(socket,CROC); smooth(socket,1)
    e=sph(0.12,(ex,0.12,3.08),14,10); setmat(e,WHITE); smooth(e,1)
    p=sph(0.06,(ex,0.2,3.1),10,8); setmat(p,BLACK); smooth(p,1)
    gl=sph(0.15,(ex,0.16,2.98),14,10); gl.scale=(1,0.4,1); applyxf(gl); setmat(gl,GLASS); smooth(gl,1)
# aviator cap strap across head
strap=cyl(0.5,0.12,(0,0.0,2.98),18); strap.rotation_euler=(math.radians(90),0,0); strap.scale=(0.85,0.85,1); applyxf(strap); setmat(strap,GOGG); smooth(strap,1)

# ---- short croc arms ----
for s in (-1,1):
    arm=cyl(0.13,0.7,(s*0.62,0.15,1.7),12); arm.rotation_euler=(0,math.radians(s*38),0); applyxf(arm); setmat(arm,CROC)
    hand=sph(0.16,(s*0.85,0.15,1.42),12,8); setmat(hand,CROC)
    A=join([arm,hand],arm); smooth(A,2); A.name='ArmL' if s<0 else 'ArmR'

# ---- legs + military boots (animated) ----
for s in (-1,1):
    leg=cyl(0.17,1.05,(s*0.3,0,0.6),14); setmat(leg,CROC)
    boot=cube(0.5,(s*0.3,0.16,0.12)); boot.scale=(0.5,1.05,0.42); applyxf(boot); setmat(boot,BOOT)
    sole=cube(0.5,(s*0.3,0.18,0.02)); sole.scale=(0.54,1.1,0.12); applyxf(sole); setmat(sole,BLACK)
    L=join([leg,boot,sole],leg); smooth(L,2)
    set_origin(L,(s*0.3,0,1.1))
    L.name='LegL' if s<0 else 'LegR'

# ---- export ----
root=None
for arg in sys.argv:
    if arg.endswith('bombardiro.py'): root=os.path.dirname(os.path.dirname(os.path.abspath(arg)))
if not root: root=os.getcwd()
out=os.path.join(root,'assets'); os.makedirs(out,exist_ok=True); path=os.path.join(out,'bombardiro.glb')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
print('EXPORTED', path)
print('OBJECTS', [o.name for o in bpy.data.objects])
