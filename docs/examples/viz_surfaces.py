"""
==================
Visualize surfaces
==================

Here is a simple tutorial that shows how to visualize surfaces using DIPY. It
also shows how to load/save, get/set and update ``vtkPolyData`` and show
surfaces.

``vtkPolyData`` is a structure used by VTK to represent surfaces and other data
structures. Here we show how to visualize a simple cube but the same idea
should apply for any surface.
"""

import numpy as np

###############################################################################
# Import useful functions from ``dipy.viz.utils``

import dipy.io.vtk as io_vtk
import fury.utils as ut_vtk
from fury import window

# Conditional import machinery for vtk
# Allow import, but disable doctests if we don't have vtk
from dipy.utils.optpkg import optional_package
vtk, have_vtk, setup_module = optional_package('vtk')






reader = vtk.vtkPolyDataReader()
reader.SetFileName('C:/Users/dmreagan/Downloads/100307_white_rh.vtk')


subdivider = vtk.vtkLoopSubdivisionFilter()
subdivider.SetNumberOfSubdivisions(2)
subdivider.SetInputConnection(reader.GetOutputPort())


mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(subdivider.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().BackfaceCullingOn()
# actor.SetScale(0.08, 0.08, 0.08)





# geom_shader_file = open("fury/shaders/line.geom", "r")
# geom_shader_code = geom_shader_file.read()

# poly_mapper.SetGeometryShaderCode(geom_shader_code)

# @vtk.calldata_type(vtk.VTK_OBJECT)
# def vtkShaderCallback(caller, event, calldata=None):
#     program = calldata
#     if program is not None:
#         program.SetUniformf("linewidth", linewidth)

# poly_mapper.AddObserver(vtk.vtkCommand.UpdateShaderEvent,
#                         vtkShaderCallback)

mapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Coincident::Impl',
    True,
    '''
    //VTK::Coincident::Impl
    if (df > 0.35) discard;
    fragOutput0 = vec4(1, 1, 1, 1);
    ''',
    False
)

# debug block
# mapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,
#     '//VTK::Coincident::Impl',
#     True,
#     '''
#     //VTK::Coincident::Impl
#     foo = abs(bar);
#     ''',
#     False
# )



# renderer and scene
renderer = window.Renderer()
renderer.add(actor)
# renderer.set_camera(position=(10, 5, 7), focal_point=(0.5, 0.5, 0.5))
# renderer.zoom(3)

# display
window.show(renderer, size=(600, 600), reset_camera=False)
# window.record(renderer, out_path='cube.png', size=(600, 600))
