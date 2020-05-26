import vtk
from fury.utils import rgb_to_vtk
import numpy as np

fileName = '2x2px.png'

colors = vtk.vtkNamedColors()

# Load in the texture map. A texture is any unsigned char image. If it
# is not of this type, you will have to map it through a lookup table
# or by using vtkImageShiftScale.
#
# readerFactory = vtk.vtkImageReader2Factory()
# textureFile = readerFactory.CreateImageReader2(fileName)
# textureFile.SetFileName(fileName)
# textureFile.Update()

# atext = vtk.vtkTexture()
# atext.SetInputConnection(textureFile.GetOutputPort())
# atext.InterpolateOff()


atext = vtk.vtkTexture()
atext.InterpolateOff()

arr2 = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [0, 255, 255]]])
arr = 255 * np.random.randn(2, 2, 3)
# arr = 255 * np.random.randn(512, 512, 3)
# arr[:256] = np.array([255, 0, 0])
grid = rgb_to_vtk(arr2.astype(np.uint8))
# for i in range(6):
#     atext.SetInputDataObject(i, grid)
atext.SetInputDataObject(grid)


# Create a plane source and actor. The vtkPlanesSource generates
# texture coordinates.
#
plane = vtk.vtkPlaneSource()
# plane = vtk.vtkCubeSource()

planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(plane.GetOutputPort())

# planeMapper.AddShaderReplacement(
#     vtk.vtkShader.Vertex,
#     '//VTK::Color::Dec',
#     True,
#     '''
#     //VTK::Color::Dec
#     uniform sampler2D texture_0;
#     ''',
#     False
# )

# planeMapper.AddShaderReplacement(
#     vtk.vtkShader.Vertex,
#     '//VTK::ValuePass::Impl',
#     True,
#     '''
#     //VTK::ValuePass::Impl

#     vec4 color = texture(texture_0, tcoordMC);

#     mat4 translateMat = mat4(1.0, 0.0, 0.0, 0.0,
#                              0.0, 1.0, 0.0, 0.0,
#                              0.0, 0.0, 1.0, 0.0,
#                              0.0, 0.0, sin(1000*vertexMC.x), 1.0);

    
#     vec4 myVertexMC = translateMat * vertexMC;

#     vertexVCVSOutput = MCVCMatrix * myVertexMC;
#     gl_Position = MCDCMatrix * myVertexMC;
#     ''',
#     False
# )

# planeMapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,
#     '//VTK::Coincident::Impl',
#     True,
#     '''
#     //VTK::Coincident::Impl
#     vec4 mycolor = texture(texture_0, vec2(0.1, 0.9)); // Read texture color
#     mycolor = vec4(mycolor.rgb, 1.0); // Update color based on texture nbr of components 
#     fragOutput0 = mycolor;
#     ''',
#     False
# )

planeMapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Coincident::Impl',
    True,
    '''
    //VTK::Coincident::Impl
    //vec4 mycolor = texture(texture_0, vec2(0.1, 0.1)); // Read texture color
    //vec4 mycolor = texelFetch(texture_0, ivec2(1, 0), 0); // texelFetch uses ints in texel space
    // texcoord origin at bottom-left

    vec4 mycolor = texture(texture_0, tcoordVCVSOutput);
    //vec4 mycolor = texelFetch(texture_0, ivec2(gl_FragCoord.xy), 0);
    mycolor = vec4(mycolor.rgb, 1.0); // Update color based on texture nbr of components 

    //vec4 mycolor = vec4(1.0, 0.0, 0.0, 1.0);
    fragOutput0 = mycolor;
    ''',
    False
)

# vec4 tcolor_0 = texture(texture_0, tcoordVCVSOutput); // Read texture color
# tcolor_0 = vec4(tcolor_0.r,tcolor_0.g,tcolor_0.b,1.0); // Update color based on texture nbr of components 
# vec4 tcolor = tcolor_0; // BLENDING: None (first texture) 

# fragOutput0 = clamp(fragOutput0,0.0,1.0) * tcolor;

#   if (fragOutput0.a <= 0.0)
#     {
#     discard;
#     }

# debug block
# planeMapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,
#     '//VTK::Coincident::Impl',
#     True,
#     '''
#     //VTK::Coincident::Impl
#     foo = abs(bar);
#     ''',
#     False
# )

planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)
planeActor.SetTexture(atext)

# Create the RenderWindow, Renderer and Interactor.
renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size.
renderer.AddActor(planeActor)
renderer.SetBackground(colors.GetColor3d("SlateGray"))
renWin.SetSize(640, 480)

# render the image
renWin.Render()

renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-30)
renderer.GetActiveCamera().Roll(-20)
renderer.ResetCameraClippingRange()
renWin.Render()
iren.Start()
