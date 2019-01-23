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
# Import useful functions

from fury import window, utils
from fury.io import save_polydata, load_polydata
from fury.utils import vtk

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

utils.set_polydata_vertices(my_polydata, my_vertices)
utils.set_polydata_triangles(my_polydata, my_triangles)

###############################################################################
# Save the ``vtkPolyData``

# file_name = "my_cube.vtk"
# save_polydata(my_polydata, file_name)
# print("Surface saved in " + file_name)

###############################################################################
# Load the ``vtkPolyData``

# cube_polydata = load_polydata(file_name)

###############################################################################
# add color based on vertices position

# cube_vertices = utils.get_polydata_vertices(cube_polydata)
cube_vertices = utils.get_polydata_vertices(my_polydata)
colors = cube_vertices * 255
# utils.set_polydata_colors(cube_polydata, colors)
utils.set_polydata_colors(my_polydata, colors)

# print("new surface colors")
# print(utils.get_polydata_colors(cube_polydata))



# vtk_colors = numpy_support.numpy_to_vtk(colors, deep=True,
#                                             array_type=vtk.VTK_UNSIGNED_CHAR)
# vtk_colors.SetNumberOfComponents(3)
# vtk_colors.SetName("RGB")
# polydata.GetPointData().SetScalars(vtk_colors)


from vtk.util import numpy_support as ns

normalized_colors = colors / 255.0
normalized_colors_vtk = ns.numpy_to_vtk(normalized_colors,
                                        deep=True,
                                        array_type=vtk.VTK_UNSIGNED_CHAR)
normalized_colors_vtk.SetName('normalized_colors_vtk')

my_polydata.GetPointData().AddArray(normalized_colors_vtk)


# set up mapper for custom shaders
# mapper = utils.get_polymapper_from_polydata(my_polydata)
cube_actor = utils.get_actor_from_polydata(my_polydata)
mapper = cube_actor.GetMapper()

# send color values to shaders
mapper.MapDataArrayToVertexAttribute(
    "color",
    mapper.GetInput().GetPointData().GetScalars().GetName(),
    vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS,
    -1
)

mapper.MapDataArrayToVertexAttribute(
    'colorNorm',
    'normalized_colors_vtk',
    vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS,
    -1
)

mapper.AddShaderReplacement(
    vtk.vtkShader.Vertex,
    "//VTK::Normal::Impl",  # replace the Normal block
    True,  # before the standard replacements
    '''
    //VTK::Normal::Impl  // we still want the default
    vec4 myVertexMC = vertexMC;
    myVertexMC.xyz = vertexMC.xyz + (colorNorm.gbr - 0.5);
    ''',
    False  # only do it once
)
mapper.AddShaderReplacement(
    vtk.vtkShader.Vertex,
    "//VTK::ValuePass::Dec",  # replace the ValuePass block
    True,  # before the standard replacements
    '''
    //VTK::ValuePass::Dec  // we still want the default
    in vec3 color;  // get vertex attribute
    in vec3 colorNorm;
    out vec3 colorVSOutput; // output to frag shader
    ''',
    False  # only do it once
)
mapper.AddShaderReplacement(
    vtk.vtkShader.Vertex,
    "//VTK::ValuePass::Impl",  # replace the ValuePass block
    True,  # before the standard replacements
    '''
    //VTK::ValuePass::Impl  // we still want the default
    colorVSOutput = colorNorm;  // pass through attribute
    vertexVCVSOutput = MCVCMatrix * myVertexMC;
    gl_Position = MCDCMatrix * myVertexMC;
    ''',
    False  # only do it once
)
# now modify the fragment shader
mapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,   # in the fragment shader
    "//VTK::Normal::Dec",  # replace the normal block
    True,  # before the standard replacements
    '''
    //VTK::Normal::Dec  // we still want the default
    in vec3 colorVSOutput;  // get color
    uniform vec2 windowSize;

    // draw circle
    float circle(in vec2 _st, in float _radius){
        vec2 l = _st-vec2(0.5);
        return 1. - smoothstep(_radius-(_radius*0.01),
                               _radius+(_radius*0.01),
                               dot(l,l)*4.0);
    }
    ''',
    False  # only do it once
)
mapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,   # in the fragment shader
    "//VTK::Normal::Impl",  # replace the normal block
    True,  # before the standard replacements
    '''
    //VTK::Normal::Impl  // we still want the default calc
    //diffuseColor = diffuseIntensity * vec3(1, 0, 0);  // make all frags red
    diffuseColor = diffuseIntensity * colorVSOutput; // use input color

    vec2 st = gl_FragCoord.xy / windowSize; // normalized window coordinates
    st *= 50;
    st = fract(st);
    
    // if close to camera, circlify it
    if (vertexVCVSOutput.z > -12) {
        diffuseColor *= vec3(circle(st, 0.25));
    }
    ''',
    False  # only do it once
)

# debug block
# mapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,   # in the fragment shader
#     "//VTK::Coincident::Impl",  # replace the normal block
#     True,  # before the standard replacements
#     "//VTK::Coincident::Impl\n"  # we still want the default calc
#     "foo = bar;\n",  # convert from [0, 255] -> [0, 1]
#     False  # only do it once
# )






###############################################################################
# Visualize surfaces

# get vtkActor
# cube_actor = utils.get_actor_from_polydata(cube_polydata)
# cube_actor = utils.get_actor_from_polydata(my_polydata)

# Create a scene
scene = window.Scene()
scene.add(cube_actor)
scene.set_camera(position=(10, 5, 7), focal_point=(0.5, 0.5, 0.5))
scene.zoom(3)




@vtk.calldata_type(vtk.VTK_OBJECT)
def vtkShaderCallback(caller, event, calldata=None):
    window_size = scene.GetRenderWindow().GetSize()
    program = calldata
    if program is not None:
        program.SetUniform2f("windowSize", [window_size[0], window_size[1]])

mapper.AddObserver(vtk.vtkCommand.UpdateShaderEvent,
                   vtkShaderCallback)





# display
window.show(scene, size=(600, 600), reset_camera=False)
# window.record(scene, out_path='cube.png', size=(600, 600))
