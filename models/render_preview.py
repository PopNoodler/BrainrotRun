# Re-create the in-game three.js buildSahur() from primitives in Blender and render a PNG,
# so the model's silhouette/likeness can be inspected. Approximate (shading differs from WebGL).
# Run: blender --background --python models/render_preview.py  -> assets/preview_sahur.png
import bpy, math, os, sys
from mathutils import Vector

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
for c in (bpy.data.meshes, bpy.data.materials):
    for x in list(c): c.remove(x)

def mat(n, rgb):
    m = bpy.data.materials.new(n); m.use_nodes=True
    m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*rgb,1)
    m.diffuse_color=(*rgb,1)   # workbench MATERIAL color
    return m
WOOD=mat('wood',(0.79,0.54,0.31)); WOODD=mat('woodD',(0.54,0.34,0.19))
CLOTH=mat('cloth',(0.91,0.89,0.82)); WHITE=mat('white',(0.95,0.95,0.94))
BLACK=mat('black',(0.06,0.05,0.04)); MOUTH=mat('mouth',(0.29,0.06,0.06)); BROW=mat('brow',(0.23,0.14,0.07))

def T(x,y,z): return (x, -z, y)          # three.js (Y-up, faces +Z) -> Blender (Z-up, faces -Y)
def setm(o,m): o.data.materials.clear(); o.data.materials.append(m)
def sph(r,loc,sc=None,m=WOOD):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=T(*loc)); o=bpy.context.active_object
    if sc: o.scale=(sc[0],sc[2],sc[1])
    bpy.ops.object.shade_smooth(); setm(o,m); return o
def cyl(r,d,loc,m=WOOD,rot=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d,location=T(*loc)); o=bpy.context.active_object
    if rot: o.rotation_euler=rot
    bpy.ops.object.shade_smooth(); setm(o,m); return o
def box(w,h,d,loc,m=WOOD,rz=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=T(*loc)); o=bpy.context.active_object
    o.scale=(w,d,h)                        # three (w,h,d) -> blender (x,y=d,z=h)
    if rz: o.rotation_euler=(0,0,rz)
    setm(o,o.data.materials and WOOD or WOOD); setm(o,m); return o

# body: taller/leaner wooden club (bat-like), rounded top — no headband
cyl(0.46,1.9,(0,1.75,0),WOOD); sph(0.46,(0,0.85,0),m=WOOD); sph(0.47,(0,2.78,0),(1,0.72,1),WOOD)
# subtle taper: a slightly wider base ring
sph(0.5,(0,0.95,0),(1,0.5,1),WOODD)
# face (higher on the club, eyes closer)
for ex in (-0.22,0.22):
    sph(0.17,(ex,2.22,0.36),m=WHITE); sph(0.085,(ex*0.92,2.2,0.5),m=BLACK); sph(0.03,(ex*0.92-0.04,2.26,0.55),m=WHITE)
    box(0.3,0.08,0.09,(ex,2.44,0.36),BROW,rz=(0.5 if ex<0 else -0.5))
sph(0.22,(0,1.86,0.36),(1,0.8,0.5),MOUTH)
box(0.3,0.06,0.04,(0,1.97,0.5),WHITE); box(0.3,0.06,0.04,(0,1.76,0.5),WHITE)
# thin arms down-ish + hands
for s in (-1,1):
    cyl(0.11,0.8,(s*0.56,1.75,0),WOODD,rot=(0,s*0.9,0)); sph(0.15,(s*0.78,1.28,0),m=WOODD)
# little bat in hand
cyl(0.13,1.1,(0.85,1.5,0.2),WOODD,rot=(math.radians(30),0,0))
# thin legs + feet
for s in (-1,1):
    cyl(0.14,0.7,(s*0.24,0.45,0),WOODD); box(0.24,0.15,0.46,(s*0.24,0.1,0.12),WOODD)

# ---- camera + light + render (workbench, material colors) ----
bpy.ops.object.camera_add(location=(0,-7.2,1.55)); cam=bpy.context.active_object
cam.rotation_euler=(math.radians(90),0,0); cam.data.lens=60; bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='SUN',location=(-4,-6,8)); bpy.context.active_object.data.energy=3
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='STUDIO'; sc.display.shading.color_type='MATERIAL'
sc.render.resolution_x=360; sc.render.resolution_y=470; sc.render.film_transparent=False
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.16,0.11,0.29,1)
root=None
for a in sys.argv:
    if a.endswith('render_preview.py'): root=os.path.dirname(os.path.dirname(os.path.abspath(a)))
if not root: root=os.getcwd()
sc.render.filepath=os.path.join(root,'assets','preview_sahur.png')
bpy.ops.render.render(write_still=True)
print('RENDERED', sc.render.filepath)
