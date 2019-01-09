import vtk

fileName = '2x2px.png'

colors = vtk.vtkNamedColors()

# Load in the texture map. A texture is any unsigned char image. If it
# is not of this type, you will have to map it through a lookup table
# or by using vtkImageShiftScale.
#
readerFactory = vtk.vtkImageReader2Factory()
textureFile = readerFactory.CreateImageReader2(fileName)
textureFile.SetFileName(fileName)
textureFile.Update()

atext = vtk.vtkTexture()
atext.SetInputConnection(textureFile.GetOutputPort())
atext.InterpolateOff()

# Create a plane source and actor. The vtkPlanesSource generates
# texture coordinates.
#
plane = vtk.vtkPlaneSource()

planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(plane.GetOutputPort())

planeMapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Coincident::Impl',
    True,
    '''
    //VTK::Coincident::Impl
    vec4 mycolor = texture(texture_0, vec2(1000, 10000)); // Read texture color
    mycolor = vec4(mycolor.r,mycolor.g,mycolor.b,1.0); // Update color based on texture nbr of components 
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