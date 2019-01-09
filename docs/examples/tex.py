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

###############################################################################
# Create an empty ``vtkPolyData``

my_polydata = vtk.vtkPolyData()

###############################################################################
# Create a cube with vertices and triangles as numpy arrays

my_vertices = np.array([[0.0,  0.0,  0.0],
                       [0.0,  0.0,  1.0],
                       [0.0,  1.0,  0.0],
                       [0.0,  1.0,  1.0],
                       [1.0,  0.0,  0.0],
                       [1.0,  0.0,  1.0],
                       [1.0,  1.0,  0.0],
                       [1.0,  1.0,  1.0]])
# the data type for vtk is needed to mention here, numpy.int64
my_triangles = np.array([[0,  6,  4],
                         [0,  2,  6],
                         [0,  3,  2],
                         [0,  1,  3],
                         [2,  7,  6],
                         [2,  3,  7],
                         [4,  6,  7],
                         [4,  7,  5],
                         [0,  4,  5],
                         [0,  5,  1],
                         [1,  5,  7],
                         [1,  7,  3]], dtype='i8')


###############################################################################
# Set vertices and triangles in the ``vtkPolyData``

ut_vtk.set_polydata_vertices(my_polydata, my_vertices)
ut_vtk.set_polydata_triangles(my_polydata, my_triangles)

###############################################################################
# Save the ``vtkPolyData``

# file_name = "my_cube.vtk"
# io_vtk.save_polydata(my_polydata, file_name)
# print("Surface saved in " + file_name)

###############################################################################
# Load the ``vtkPolyData``

# cube_polydata = io_vtk.load_polydata(file_name)
cube_polydata = my_polydata

# set up mapper for custom shaders
mapper = ut_vtk.get_polymapper_from_polydata(cube_polydata)

# # now modify the fragment shader
# mapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,   # in the fragment shader
#     "//VTK::Normal::Dec",  # replace the normal block
#     True,  # before the standard replacements
#     "//VTK::Normal::Dec\n"  # we still want the default
#     "in vec3 colorVSOutput;\n",  # get color
#     False  # only do it once
# )
# mapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,   # in the fragment shader
#     "//VTK::Normal::Impl",  # replace the normal block
#     True,  # before the standard replacements
#     "//VTK::Normal::Impl\n"  # we still want the default calc
#     #"diffuseColor = vec3(1, 0, 0);\n",  # convert from [0, 255] -> [0,1]
#     "diffuseColor = vec3(0, texture(actortexture, 0), 0);\n",  # convert from [0, 255] -> [0,1]
#     False  # only do it once
# )

###############################################################################
# add color based on vertices position

cube_vertices = ut_vtk.get_polydata_vertices(cube_polydata)
colors = cube_vertices * 255
# ut_vtk.set_polydata_colors(cube_polydata, colors)

# print("new surface colors")
# print(ut_vtk.get_polydata_colors(cube_polydata))

###############################################################################
# Visualize surfaces

# get vtkActor
cube_actor = ut_vtk.get_actor_from_polydata(cube_polydata)
cube_actor.SetMapper(mapper)

# cube_actor.SetTexture(tex)

# Create a scene
scene = window.Scene()
scene.add(cube_actor)
scene.set_camera(position=(10, 5, 7), focal_point=(0.5, 0.5, 0.5))
scene.zoom(3)

show_manager = window.ShowManager(scene, size=(600, 600), reset_camera=False)




# floats = vtk.vtkFloatArray()
# floats.SetNumberOfComponents(4)
# floats.InsertNextTuple([0, 1.0, 0, 1.0])

uchars = vtk.vtkUnsignedCharArray()
uchars.SetNumberOfComponents(4)
uchars.InsertNextTuple([0, 255, 0, 1])

# attempt to create vtkTextureObject via vtkDataTransferHelper
# helper = vtk.vtkDataTransferHelper()
# # helper.SetArray(floats)
# helper.SetArray(uchars)

# ren_win = show_manager.window
# helper.SetContext(ren_win)

# extent = [1, 0, 0, 0, 0, 0]
# helper.SetCPUExtent(extent)
# helper.SetGPUExtent(extent)

# helper.Upload(0, None)

# tex_obj = helper.GetTexture()




# attempt to create vtkTextureObject manually
# tex_obj = vtk.vtkTextureObject()
# tex_obj.Create1DFromRaw(1, 4, floats.GetDataType(), floats)  # 10 = VTK_FLOAT, see https://www.vtk.org/doc/nightly/html/vtkType_8h.html
# tex_obj.Create1DFromRaw(1, 4, uchars.GetDataType(), uchars)



# attempt to create vtkTextureObject from PBO
# pbo = vtk.vtkPixelBufferObject()
# ren_win = show_manager.window
# pbo.SetContext(ren_win)
# pbo.Upload1D(uchars.GetDataType(), uchars, 1, 4, 3)


# tex = vtk.vtkTexture()
# tex.SetTextureObject(tex_obj)

# attept to load texture from file
# fileName = '1px_green.png'
fileName = '2x2px.png'

readerFactory = vtk.vtkImageReader2Factory()
textureFile = readerFactory.CreateImageReader2(fileName)
textureFile.SetFileName(fileName)
textureFile.Update()

tex = vtk.vtkTexture()
tex.SetInputConnection(textureFile.GetOutputPort())

cube_actor.SetTexture(tex)
# cube_actor.GetProperty().SetTexture('mytex', tex)


mapper = cube_actor.GetMapper()

# mapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,
#     '//VTK::Coincident::Dec',
#     True,
#     '''
#     //VTK::Coincident::Dec
#     uniform sampler1D mytex
#     ''',
#     False
# )

# mapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,
#     '//VTK::Coincident::Impl',
#     True,
#     '''
#     //VTK::Coincident::Impl
#     fragOutput0 = texture(mytex, 0);
#     ''',
#     False
# )

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



show_manager.initialize()
show_manager.render()
show_manager.start()

# display
# window.show(scene, size=(600, 600), reset_camera=False)
# window.record(scene, out_path='cube.png', size=(600, 600))
