# Graficacion-Proyecto-integrador-unidad-1
proyecto de pasillo curvo con animacion de camara

## Descripción del Proyecto

Este proyecto consiste en la creación de un **escenario 3D procedural en Blender** mediante Python, donde se genera automáticamente un **pasillo curvo** compuesto por módulos repetitivos.
Como mejora al ejercicio original, se agregó una **animación de cámara** que recorre el camino a través del pasillo siguiendo una trayectoria definida matemáticamente.

El objetivo fue integrar:

* Modelado procedural
* Uso de scripts en Blender (`bpy`)
* Matemáticas aplicadas a gráficos 3D
* Animación automática mediante curvas

---

## Tecnologías Utilizadas

| Herramienta          | Uso                                 |
| -------------------- | ----------------------------------- |
| Blender              | Entorno de modelado y animación 3D  |
| Python (`bpy`)       | Automatización del modelado         |
| Mathutils            | Cálculo de vectores y posiciones    |
| Geometría Procedural | Generación automática del escenario |

---

## ¿Qué es el Modelado Procedural?

El **modelado procedural** consiste en generar objetos mediante reglas matemáticas y programación en lugar de modelarlos manualmente.

Ventajas:
* Escenarios escalables
* Cambios instantáneos modificando parámetros
* Reutilización del código
* Precisión geométrica
* Automatización completa

---

##  Parámetros Editables del Proyecto

Estos valores controlan todo el escenario:

```python
segmentos = 100          # Cantidad de módulos del pasillo
largo_segmento = 2.0     # Tamaño de cada sección
ancho_pasillo = 5.0      # Anchura del pasillo
angulo_total = -370      # Curvatura total del recorrido
altura_pared = 2.5       # Altura visual de las paredes
animacion_frames = 5     # Duración de la animación
```

Modificar estos parámetros cambia:

* Longitud del pasillo
* Intensidad de la curva
* Velocidad de la cámara

---

## Generación del Pasillo

El pasillo se construye mediante un **bucle (`for`)** que repite la creación de módulos:

Cada iteración genera:

* Un suelo (`Plane`)
* Una pared izquierda (cubo)
* Una pared derecha (cubo)

### Suelo

Se crea con:

```python
bpy.ops.mesh.primitive_plane_add()
```

Se rota según el ángulo del segmento para seguir la curva.

---

### Paredes con Volumen Real

Las paredes ahora son **cubos verdaderos**, no planos escalados:

```python
bpy.ops.mesh.primitive_cube_add()
izq.scale = (tam_cubo, tam_cubo, tam_cubo)
```

Esto da sensación de estructura sólida.

---

### Alternancia de Colores

Las paredes izquierdas alternan colores usando el índice del bucle:

```python
if i % 2 == 0:
    material_naranja
else:
    material_negro
```

Esto mejora la percepción de movimiento cuando la cámara avanza.

---

## Curvatura Matemática del Pasillo

La curva no se dibuja manualmente.
Se calcula con trigonometría:

```python
cx = cos(angulo) * radio
cy = sin(angulo) * radio
```

Esto posiciona cada módulo sobre un arco circular perfecto.

Resultado:
➡ El pasillo gira suavemente sin deformaciones.

---

##  Creación de la Ruta de la Cámara

Se genera una **curva guía invisible** usando:

```python
curve_data = bpy.data.curves.new(type='CURVE')
```

Luego se agregan puntos coincidiendo con el centro de cada segmento:

```python
spline.points[i].co = (p.x, p.y, 0, 1)
```

Esta curva será el camino que seguirá la cámara.

---

## Sistema de Animación

Para mover la cámara correctamente se crea un objeto intermedio llamado **Rig** (`Empty`):

```python
bpy.ops.object.empty_add(type='PLAIN_AXES')
```

Este objeto recibe la restricción:

```python
FOLLOW_PATH
```

Que lo obliga a desplazarse por la curva.

La cámara se hace hija del Rig:

```python
cam.parent = rig
```

Esto permite:
✔ Movimiento suave
✔ Orientación automática
✔ Simulación tipo “recorrido cinematográfico”

---

## Animación Automática

La animación se controla con el parámetro:

```python
con.offset_factor = 0.0 → inicio
con.offset_factor = 1.0 → final
```

Se insertan keyframes:

```python
con.keyframe_insert()
```

La interpolación se configura en **LINEAR** para evitar aceleraciones artificiales:

```python
keyframe_new_interpolation_type = 'LINEAR'
```

Resultado:
➡ La cámara avanza a velocidad constante atravesando el pasillo.

---

<img width="982" height="526" alt="image" src="https://github.com/user-attachments/assets/efb92370-46e6-4c8e-b6e0-388e24988932" />


## Resultado Final

El script produce:

* Un pasillo curvo generado completamente por código.
* Paredes volumétricas alternadas en color.
* Un recorrido automático de cámara.
* Una animación lista para renderizar.

<img width="980" height="493" alt="image" src="https://github.com/user-attachments/assets/34145bbb-25a8-496b-bf1b-c734d5d497a8" />

## Conclusión

El proyecto demuestra cómo la programación puede integrarse con el modelado 3D para crear escenas completas sin intervención manual.
El uso de técnicas procedurales permite construir entornos dinámicos, modificables y escalables, fundamentales en áreas como videojuegos, simulación y animación digital.
