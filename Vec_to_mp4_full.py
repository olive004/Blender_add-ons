#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 10:21:36 2019

@author: oliviagallup
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 10:21:36 2019

@author: oliviagallup
"""

import bpy
import mathutils
from mathutils import *
from math import *
import numpy as np

# GLOBAL VAR'S
filepath_vector = '/Users/oliviagallup/Desktop/Laser_Cutz/Snake-y.svg'    # Pathname of svg to import
# Color
mat_color =  [0.308071, 0.482746, 0.089438]      # RGB color scheme of obj
engraved_mat_color = [1.000000, 0.995445, 0.000000]
bg_color = [0.006513, 0.046783, 0.268293]       # RGB color of horizon (in 'world' settings)
emit = 0.7         # Fluorescence of obj
alpha = 0.324925      # Main (alpha) transparency of obj
frame_count = 36
render_mode = 'SKY'     # Background color can be either 'SKY' or 'TRANSPARENT'
output_filepath  = '/Users/oliviagallup/Desktop/Blendr/Animations/Snake-y'   # Directory to output the png's to



# FUNCTIONS
def replace_material(object_name,old_material_name,new_material_name):         # From https://blender.stackexchange.com/questions/53366/how-can-i-replace-a-material-from-python
    """
    replace a material in blender.
    params:
        object - object for which we are replacing the material
        old_material - The old material name as a string
        new_material - The new material name as a string
    """
    ob = bpy.data.objects[object_name]
    om = bpy.data.materials[old_material_name]
    nm = bpy.data.materials[new_material_name]
    # Iterate over the material slots and replace the material
    for s in ob.material_slots:
        if s.material.name == om:
            s.material = nm






# INITIATION
# Delete all starting objects
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)   # delete all default obj

# Import and add necessary objects
bpy.ops.import_curve.svg(filepath= filepath_vector)
# Maybe add a join option at this point if we are importing more than one file (select all currently presents objects, which should only be what we imported, and join them

# Obj Names
obj_cutting_edge_n = bpy.data.objects[0].name         # Name of first object 'Curve' by default; the back-most vector in the svg will be the first imported, make sure this is the cut-out vector
obj_engravings = bpy.data.objects[1:]   # List of objects that are not the cut vector, ie the engravings or rasters
obj_engravings_n = obj_engravings    # Initializing array of engraved objects names
loop_count =0
for i in obj_engravings:        # For extracting names of the engraved objects
    obj_engravings_n[loop_count] = i.name
    loop_count = loop_count +1

bpy.ops.object.camera_add()
bpy.ops.object.lamp_add(type='HEMI')
bpy.ops.object.lamp_add(type='POINT')

most_recent_mat_index = (np.size(bpy.data.materials) - 1)
obj_mat = bpy.data.materials[most_recent_mat_index].name


# Joining Vectors
# Select all vectors you want to join, make sure one of them is active. Then join them rather than grouping or parenting them.
# # Trying to change the context to bpy.context.area.type = "VIEW_3D" results in blender quitting
for i in obj_engravings_n:      # Select engraving vectors
    print(i)
    bpy.data.objects[i].select = True     # Blender 2.79 doesn't have bpy.ops.object.select_name(name ="")
# bpy.ops.object.group_link(group=engravings_Group_name)

engraved_obj = bpy.data.objects[obj_engravings_n[0]]   # The name of the active object becomes name of joined obj
bpy.context.scene.objects.active = engraved_obj      # Make object active; 2.8 uses the function context.view_layer.objects.active = obj for this
engraved_obj_n = engraved_obj.name
bpy.ops.object.join()

# New Material for engraving vectors
# bpy.ops.material.new()
engraved_mat = bpy.data.materials.new("engraved_mat")
engraved_mat.diffuse_color = engraved_mat_color


# replace_material(engraved_obj_n, obj_mat, engraved_mat.name)          # Doesn't work :'(
bpy.data.objects[engraved_obj_n].material_slots[0].material = engraved_mat






# STARTING LOCATIONS
# Camera Loc
bpy.data.objects["Camera"].location[0] = 0
bpy.data.objects["Camera"].location[1] = -6.50764
bpy.data.objects["Camera"].location[2] = 5.343665
# Camera Rot
bpy.data.objects["Camera"].rotation_euler[0] = ((71.1593/180)*pi )
bpy.data.objects["Camera"].rotation_euler[1] = 0
bpy.data.objects["Camera"].rotation_euler[2] = 0

# Hemi Loc
bpy.data.objects["Hemi"].location[0] = -7.830763
bpy.data.objects["Hemi"].location[1] = -7.267582
bpy.data.objects["Hemi"].location[2] = 6.088027
# Hemi Rot
bpy.data.objects["Hemi"].rotation_euler[0] = (-183.814/180)*pi
bpy.data.objects["Hemi"].rotation_euler[1] = (-182.788/180)*pi
bpy.data.objects["Hemi"].rotation_euler[2] = (-163.741/180)*pi

# Lamp point Loc
bpy.data.objects["Point"].location[0] = 4.076245
bpy.data.objects["Point"].location[1] = 1.005454
bpy.data.objects["Point"].location[2] = 5.903862


# Obj Loc
bpy.data.objects[engraved_obj_n].parent = bpy.data.objects[obj_cutting_edge_n]

bpy.data.objects[obj_cutting_edge_n].location[0] = 0
bpy.data.objects[obj_cutting_edge_n].location[1] = 1.326495
bpy.data.objects[obj_cutting_edge_n].location[2] = 2.818986
# Obj Rot
bpy.data.objects[obj_cutting_edge_n].rotation_euler[0] = (90/180)*pi
bpy.data.objects[obj_cutting_edge_n].rotation_euler[1] = 0
bpy.data.objects[obj_cutting_edge_n].rotation_euler[2] = 0
# Obj origin: MUST come after being moved, otherwise engraving and body won't line up
bpy.context.scene.objects.active = bpy.data.objects[obj_cutting_edge_n]
bpy.data.objects[obj_cutting_edge_n].select = True
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')

# Engraved Obj Loc: Slightly inside body object
curr_y_location = bpy.data.objects[engraved_obj_n].location[1]
bpy.data.objects[engraved_obj_n].location[1] = curr_y_location + 0.02

# Engraved Obj origin
# bpy.context.scene.objects.active = bpy.data.objects[engraved_obj_n]
# bpy.data.objects[engraved_obj_n].select = True
# bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')



# OBJECT CHAR'S
# Body Obj Scaling:         Scaling all imported obj's by percentage
final_size = 70
scaling_factor = np.zeros(3)
for i in range(2):      # calculating scaling factor
    curr_dimension = bpy.data.objects[obj_cutting_edge_n].scale[i]
    scaling_factor[i] = (final_size * 1) / (curr_dimension)

for i in range(2):      # scaling body obj
    curr_dimension = bpy.data.objects[obj_cutting_edge_n].scale[i]
    bpy.data.objects[obj_cutting_edge_n].scale[i] = scaling_factor[i]*(curr_dimension) # xyz same scale-up
# bpy.data.objects[obj_cutting_edge_n].scale[1] = 70    # y scale
# bpy.data.objects[obj_cutting_edge_n].scale[2] = 70    # z scale

# # Engraved Obj Scaling
# for i in range(2):
#     curr_dimension = bpy.data.objects[engraved_obj_n].scale[i]
#     bpy.data.objects[engraved_obj_n].scale[i] = scaling_factor[i]*(curr_dimension) # xyz same scale-up
# # bpy.data.objects[engraved_obj_n].scale[0] = 70    # x scale
# # bpy.data.objects[engraved_obj_n].scale[1] = 70    # y scale
# # bpy.data.objects[engraved_obj_n].scale[2] = 70    # z scale

# Material settings
bpy.data.materials[obj_mat].specular_intensity = 0.6      # light intensity
bpy.data.materials[obj_mat].specular_hardness = 35        # hardness
bpy.data.materials[obj_mat].emit = emit
bpy.data.materials[obj_mat].raytrace_transparency.gloss_factor = 0.550388      # gloss factor
bpy.data.materials[obj_mat].use_transparency = True
bpy.data.materials[obj_mat].transparency_method = 'RAYTRACE'
bpy.data.materials[obj_mat].alpha = alpha           # transparency
bpy.data.materials[obj_mat].diffuse_color = mat_color     # RGBK
bpy.data.materials[obj_mat].raytrace_transparency.depth = 4         # refraction depth


# Extrude
bpy.context.scene.objects.active = bpy.data.objects[obj_cutting_edge_n]
bpy.data.objects[obj_cutting_edge_n].select = True
bpy.ops.object.convert(target='MESH')

bpy.ops.object.mode_set(mode='EDIT')    # change to edit mode
bpy.ops.mesh.select_all(action='TOGGLE')     # select all vertices of mesh

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -0.356), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})     # phat funciton to extrude in z direction by an amount

bpy.ops.object.mode_set(mode='OBJECT')    # change to edit mode





# KEYFRAMES
# Start:        Must be careful about which object is active and selected while a keyframe is being inserted
bpy.data.scenes["Scene"].frame_start = 1
bpy.data.scenes["Scene"].frame_current = bpy.data.scenes["Scene"].frame_start
bpy.ops.anim.keyframe_insert_menu(type='Rotation')
# Engraved obj Start
# bpy.data.objects[engraved_obj_n].select = True              # Select and make active engraved obj
# bpy.context.scene.objects.active = bpy.data.objects[engraved_obj_n]
# bpy.ops.anim.keyframe_insert_menu(type='Rotation')

# End
bpy.data.scenes["Scene"].frame_end = frame_count
bpy.data.scenes["Scene"].frame_current = bpy.data.scenes["Scene"].frame_end

# bpy.data.objects[engraved_obj_n].rotation_euler[2] = ((359/180)*pi)           # deg/180 *pi
# bpy.ops.anim.keyframe_insert_menu(type='Rotation')

bpy.data.objects[obj_cutting_edge_n].select = True              # Select and make active body obj
bpy.context.scene.objects.active = bpy.data.objects[obj_cutting_edge_n]
bpy.data.objects[obj_cutting_edge_n].rotation_euler[2] = ((359/180)*pi)           # deg/180 *pi
bpy.ops.anim.keyframe_insert_menu(type='Rotation')

#Interpolation for animation
# area = bpy.context.area
# old_type = area.type
# area.type = 'GRAPH_EDITOR'
# bpy.ops.graph.select_all_toggle()
# bpy.ops.graph.interpolation_type(type='SINE')
# area.type = old_type

fcurves = bpy.data.objects[obj_cutting_edge_n].animation_data.action.fcurves
for fcurve in fcurves:
    for kf in fcurve.keyframe_points:
        kf.interpolation = 'LINEAR'
fcurves = bpy.data.objects[engraved_obj_n].animation_data.action.fcurves
for fcurve in fcurves:
    for kf in fcurve.keyframe_points:
        kf.interpolation = 'LINEAR'


# OUTPUT
bpy.data.scenes["Scene"].render.resolution_x = 2080
bpy.data.scenes["Scene"].render.resolution_y = 2080
bpy.data.scenes["Scene"].render.filepath = output_filepath
bpy.data.scenes["Scene"].render.image_settings.file_format = 'FFMPEG'
bpy.data.scenes["Scene"].render.ffmpeg.format = "MPEG4"
bpy.data.scenes["Scene"].render.ffmpeg.codec = "H264"
bpy.data.scenes["Scene"].render.ffmpeg.constant_rate_factor = "LOSSLESS"
bpy.data.scenes["Scene"].render.ffmpeg.ffmpeg_preset = "ULTRAFAST"
bpy.ops.script.python_file_run(filepath="/Applications/Blender/blender.app/Contents/Resources/2.79/scripts/presets/ffmpeg/h264_in_MP4.py")

bpy.data.worlds["World"].horizon_color = bg_color     # Background color
bpy.data.scenes["Scene"].render.alpha_mode = render_mode       #'TRANSPARENT'

bpy.context.screen.scene = bpy.data.scenes[0]
bpy.context.scene.camera = bpy.data.objects['Camera']
# bpy.ops.render.render(animation=True)



# Slime:
# mat_color = [0 ,1, 0.0]      # RGB color scheme of obj
# bg_color =  [0.266261, 0.050876, 0.058000]      # RGB color of horizon (in 'world' settings)
# emit = 0.2          # Fluorescence of obj
# alpha = 0.324925      # Main (alpha) transparency of obj
# frame_count = 36
# render_mode = 'SKY'     # Background color can be either 'SKY' or 'TRANSPARENT'
# output_filepath  = '/Users/oliviagallup/Desktop/Blendr/Animations/test'




