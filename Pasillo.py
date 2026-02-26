import bpy
import math
from mathutils import Vector

# -----------------------------
# PARÁMETROS
# -----------------------------

segmentos = 100
largo_segmento = 2.0
ancho_pasillo = 5.0
angulo_total = -370
altura_pared = 2.5

animacion_frames = 5

# -----------------------------
# LIMPIAR ESCENA
# -----------------------------

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# -----------------------------
# MATERIALES
# -----------------------------

def crear_material(nombre, color):
    mat = bpy.data.materials.new(nombre)
    mat.diffuse_color = (*color, 1)
    return mat

mat_pared_negra = crear_material("ParedNegra",(0.1,0.1,0.1))
mat_pared_naranja = crear_material("ParedNaranja",(1.0,0.3,0.0))
mat_suelo = crear_material("Suelo",(0.2,0.2,0.2))

# -----------------------------
# CURVATURA MATEMÁTICA
# -----------------------------

angulo_rad_total = math.radians(angulo_total)
angulo_por_segmento = angulo_rad_total / segmentos
radio = largo_segmento / angulo_por_segmento

centros = []

# -----------------------------
# GENERAR PASILLO
# -----------------------------

for i in range(segmentos):

    angulo = i * angulo_por_segmento

    cx = math.cos(angulo) * radio
    cy = math.sin(angulo) * radio
    centro = Vector((cx, cy, 0))
    centros.append(centro)

    lateral = Vector((math.cos(angulo), math.sin(angulo), 0))
    mitad = ancho_pasillo / 2

    # SUELO
    bpy.ops.mesh.primitive_plane_add(size=1, location=centro)
    suelo = bpy.context.object
    suelo.scale = (mitad, largo_segmento/2, 1)
    suelo.rotation_euler[2] = angulo
    suelo.data.materials.append(mat_suelo)

   # PARED IZQUIERDA (ALTERNA COLOR - AHORA ES CUBO REAL)
    tam_cubo = largo_segmento * 0.5

    pos_izq = centro + lateral * mitad
    bpy.ops.mesh.primitive_cube_add(location=(pos_izq.x,pos_izq.y,tam_cubo))
    izq = bpy.context.object

    # Escala UNIFORME = cubo verdadero
    izq.scale = (tam_cubo, tam_cubo, tam_cubo)

    izq.rotation_euler[2] = angulo

    if i % 2 == 0:
        izq.data.materials.append(mat_pared_naranja)
    else:
        izq.data.materials.append(mat_pared_negra)
    
       # PARED DERECHA (CUBO REAL)
    tam_cubo = largo_segmento * 0.5

    pos_der = centro - lateral * mitad
    bpy.ops.mesh.primitive_cube_add(location=(pos_der.x,pos_der.y,tam_cubo))
    der = bpy.context.object

    # Escala UNIFORME = cubo verdadero
    der.scale = (tam_cubo, tam_cubo, tam_cubo)

    der.rotation_euler[2] = angulo
    der.data.materials.append(mat_pared_negra)
# -----------------------------
# CREAR CURVA GUÍA
# -----------------------------

curve_data = bpy.data.curves.new("RutaCamara", type='CURVE')
curve_data.dimensions = '3D'
curve_data.twist_mode = 'Z_UP'
curve_data.use_path = True
curve_data.path_duration = animacion_frames
curve_data.resolution_u = 64

spline = curve_data.splines.new('POLY')
spline.use_endpoint_u = True
spline.points.add(len(centros)-1)

for i,p in enumerate(centros):
    spline.points[i].co = (p.x, p.y, 0, 1)

curve_obj = bpy.data.objects.new("RutaCamara", curve_data)
bpy.context.collection.objects.link(curve_obj)

curve_data.use_path = True
curve_data.path_duration = animacion_frames

# -----------------------------
# ASEGURAR QUE LA CURVA ESTÁ LIMPIA
# -----------------------------

curve_obj.location = (0, 0, 0)
curve_obj.rotation_euler = (0, 0, 0)
curve_obj.scale = (1, 1, 1)

curve_data.resolution_u = 64
curve_data.twist_mode = 'Z_UP'

# -----------------------------
# CREAR EMPTY
# -----------------------------

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
rig = bpy.context.object
rig.name = "RigCamara"

con = rig.constraints.new(type='FOLLOW_PATH')
con.target = curve_obj
con.use_fixed_location = True
con.use_curve_follow = True
con.forward_axis = 'FORWARD_Y'
con.up_axis = 'UP_Z'

# -----------------------------
# CREAR LA CÁMARA
# -----------------------------

bpy.ops.object.camera_add(location=(0, 0, 0))
cam = bpy.context.object
cam.name = "Camara"

cam.parent = rig
cam.location = (0, 0, 1.7)

bpy.context.scene.camera = cam

cam.rotation_euler = (
    math.radians(89),
    math.radians(-1),
    math.radians(-1)
)

# -----------------------------
# ANIMAR
# -----------------------------

bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

bpy.context.scene.frame_set(1)
con.offset_factor = 0.0
con.keyframe_insert(data_path="offset_factor", frame=1)

bpy.context.scene.frame_set(animacion_frames)
con.offset_factor = 1.0
con.keyframe_insert(data_path="offset_factor", frame=animacion_frames)

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = animacion_frames
scene.frame_set(1)
