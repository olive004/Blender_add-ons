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
filepath_vector = '/Users/oliviagallup/Desktop/Laser_Cutz/croc.svg'    # Pathname of svg to import
# Color
mat_color = [0 ,1, 0.0]      # RGB color scheme of obj
bg_color = [1,0,0]       # RGB color of horizon (in 'world' settings)
emit = 0.3          # Fluorescence of obj
alpha = 0.324925      # Main (alpha) transparency of obj
frame_count = 36
render_mode = 'SKY'     # Background color can be either 'SKY' or 'TRANSPARENT'
output_filepath  = '/Users/oliviagallup/Desktop/Blendr/Animations/croc'   # Directory to output the png's to

# INITIATION
# Delete all starting objects
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)   # delete obj

# Import and add necessary objects
bpy.ops.import_curve.svg(filepath= filepath_vector)
# Maybe add a join option at this point if we are importing more than one file (select all currently presents objects, which should only be what we imported, and join them

obj_name = bpy.data.objects[0].name         # Object Name
most_recent_mat_index = (np.size(bpy.data.materials) - 1)
obj_mat = bpy.data.materials[most_recent_mat_index].name

bpy.ops.object.camera_add()
bpy.ops.object.lamp_add(type='HEMI')
bpy.ops.object.lamp_add(type='POINT')




# STARTING LOCATIONS
# Camera Loc
bpy.data.objects["Camera"].location[0] = 0
bpy.data.objects["Camera"].location[1] = -6.50764
bpy.data.objects["Camera"].location[2] = 5.343665
# Camera Rot
bpy.data.objects["Camera"].rotation_euler[0] = ((63.5593/180)*pi )
bpy.data.objects["Camera"].rotation_euler[1] = 0
bpy.data.objects["Camera"].rotation_euler[2] = 0

# Obj origin
bpy.context.scene.objects.active = bpy.data.objects[obj_name]
bpy.data.objects[obj_name].select = True
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
# Obj Loc
bpy.data.objects["Curve"].location[0] = 0
bpy.data.objects["Curve"].location[1] = -1.854945
bpy.data.objects["Curve"].location[2] = 2.901128
# Obj Rot
bpy.data.objects["Curve"].rotation_euler[0] = (90/180)*pi
bpy.data.objects["Curve"].rotation_euler[1] = 0
bpy.data.objects["Curve"].rotation_euler[2] = 0

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





# OBJECT CHAR'S
# Scaling
bpy.data.objects[obj_name].scale[0] = 70    # x scale
bpy.data.objects[obj_name].scale[1] = 70    # y scale
bpy.data.objects[obj_name].scale[2] = 70    # z scale
# Material settings
bpy.data.materials[obj_mat].specular_intensity = 0.6      # light intensity
bpy.data.materials[obj_mat].specular_hardness = 35        # hardness
bpy.data.materials[obj_mat].emit = 0.2
bpy.data.materials[obj_mat].raytrace_transparency.gloss_factor = 0.550388      # gloss factor
bpy.data.materials[obj_mat].use_transparency = True
bpy.data.materials[obj_mat].transparency_method = 'RAYTRACE'
bpy.data.materials[obj_mat].alpha = alpha           # transparency
bpy.data.materials[obj_mat].diffuse_color = mat_color     # RGBK
bpy.data.materials[obj_mat].raytrace_transparency.depth = 4         # refraction depth


# Extrude
bpy.context.scene.objects.active = bpy.data.objects[obj_name]
bpy.data.objects[obj_name].select = True
bpy.ops.object.convert(target='MESH')

bpy.ops.object.mode_set(mode='EDIT')    # change to edit mode
bpy.ops.mesh.select_all(action='TOGGLE')     # select all vertices of mesh

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.216), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})     # phat funciton to extrude in z direction by an amount

bpy.ops.object.mode_set(mode='OBJECT')    # change to edit mode





# KEYFRAMES
# Start
bpy.data.scenes["Scene"].frame_start = 1
bpy.data.scenes["Scene"].frame_current = bpy.data.scenes["Scene"].frame_start
bpy.ops.anim.keyframe_insert_menu(type='Rotation')

# End
bpy.data.scenes["Scene"].frame_end = frame_count
bpy.data.scenes["Scene"].frame_current = bpy.data.scenes["Scene"].frame_end
bpy.data.objects[obj_name].rotation_euler[2] = ((359/180)*pi)           # deg/180 *pi
bpy.ops.anim.keyframe_insert_menu(type='Rotation')

#Interpolation for animation
area = bpy.context.area
old_type = area.type
area.type = 'GRAPH_EDITOR'
bpy.ops.graph.select_all_toggle()
bpy.ops.graph.interpolation_type(type='SINE')
area.type = old_type



# OUTPUT
bpy.data.scenes["Scene"].render.resolution_x = 1080
bpy.data.scenes["Scene"].render.resolution_y = 1080
bpy.data.scenes["Scene"].render.filepath = output_filepath
bpy.data.scenes["Scene"].render.image_settings.file_format = 'PNG'
bpy.data.scenes["Scene"].render.image_settings.color_depth = '16'

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




