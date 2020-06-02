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

plane.SetPoint1(0.5, -0.5, 0)
plane.SetPoint2(-0.5, 0.5, 0)

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
    '//VTK::Picking::Impl',
    True,
    '''
    //VTK::Picking::Impl
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

# add debug text based on https://www.shadertoy.com/view/4s3fzl
planeMapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Coincident::Dec',
    True,
    '''
    //VTK::Coincident::Dec
    const int font[] = int[](
        0x69f99, 0x79797, 0xe111e, 0x79997, 0xf171f, 0xf1711, 0xe1d96, 0x99f99, 
        0xf444f, 0x88996, 0x95159, 0x1111f, 0x9f999, 0x9bd99, 0x69996, 0x79971,
        0x69b5a, 0x79759, 0xe1687, 0xf4444, 0x99996, 0x999a4, 0x999f9, 0x99699,
        0x99e8e, 0xf843f, 0x6bd96, 0x46444, 0x6942f, 0x69496, 0x99f88, 0xf1687,
        0x61796, 0xf8421, 0x69696, 0x69e84, 0x66400, 0x0faa9, 0x0000f, 0x00600,
        0x0a500, 0x02720, 0x0f0f0, 0x08421, 0x33303, 0x69404, 0x00032, 0x00002,
        0x55000, 0x00000, 0x00202, 0x42224, 0x24442);
    
    #define CH_A 0
    #define CH_B 1
    #define CH_C 2
    #define CH_D 3
    #define CH_E 4
    #define CH_F 5
    #define CH_G 6
    #define CH_H 7
    #define CH_I 8
    #define CH_J 9
    #define CH_K 10
    #define CH_L 11
    #define CH_M 12
    #define CH_N 13
    #define CH_O 14
    #define CH_P 15
    #define CH_Q 16
    #define CH_R 17
    #define CH_S 18
    #define CH_T 19
    #define CH_U 20
    #define CH_V 21
    #define CH_W 22
    #define CH_X 23
    #define CH_Y 24
    #define CH_Z 25
    #define CH_0 26
    #define CH_1 27
    #define CH_2 28
    #define CH_3 29
    #define CH_4 30
    #define CH_5 31
    #define CH_6 32
    #define CH_7 33
    #define CH_8 34
    #define CH_9 35
    #define CH_APST 36
    #define CH_PI   37
    #define CH_UNDS 38
    #define CH_HYPH 39
    #define CH_TILD 40
    #define CH_PLUS 41
    #define CH_EQUL 42
    #define CH_SLSH 43
    #define CH_EXCL 44
    #define CH_QUES 45
    #define CH_COMM 46
    #define CH_FSTP 47
    #define CH_QUOT 48 
    #define CH_BLNK 49
    #define CH_COLN 50
    #define CH_LPAR 51
    #define CH_RPAR 52

    const ivec2 MAP_SIZE = ivec2(4,5);

    //vec2 iResolution = vec2(640.0, 480.0);
    vec2 iResolution = vec2(1.0, 1.0);

    /*
        Draws a character, given its encoded value, a position, size and
        current [0..1] uv coordinate.
    */
    int drawChar( in int character, in vec2 pos, in vec2 size, in vec2 uv )
    {
        
        // Subtract our position from the current uv so that we can
        // know if we're inside the bounding box or not.
        uv-=pos;
        
        // Divide the screen space by the size, so our bounding box is 1x1.
        uv /= size;    
        
        // Multiply the UV by the bitmap size so we can work in
        // bitmap space coordinates.
        uv *= vec2(MAP_SIZE);

        // Compute bitmap texel coordinates
        ivec2 iuv = ivec2(round(uv));
        
        // Bounding box check. With branches, so we avoid the maths and lookups    
        if( iuv.x<0 || iuv.x>MAP_SIZE.x-1 ||
            iuv.y<0 || iuv.y>MAP_SIZE.y-1 ) return 0;

        // Compute bit index
        int index = MAP_SIZE.x*iuv.y + iuv.x;
        
        // Get the appropriate bit and return it.
        return (font[character]>>index)&1;

    }

    /*
        Prints a float as an int. Be very careful about overflow.
        This as a side effect will modify the character position,
        so that multiple calls to this can be made without worrying
        much about kerning.
    */
    int drawIntCarriage( in int val, inout vec2 pos, in vec2 size, in vec2 uv, in int places )
    {
        // Create a place to store the current values.
        int res = 0;
        // Surely it won't be more than 10 chars long, will it?
        // (MAX_INT is 10 characters)
        for( int i = 0; i < 10; ++i )
        {
            // If we've run out of film, cut!
            if(val == 0 && i >= places) break;
            // The current lsd is the difference between the current
            // value and the value rounded down one place.
            int digit = val % 10;
            // Draw the character. Since there are no overlaps, we don't
            // need max().
            res |= drawChar(CH_0+digit,pos,size,uv);
            // Move the carriage.
            pos.x -= size.x*1.2;
            // Truncate away this most recent digit.
            val /= 10;
        }
        return res;
    }

    /*
        Draws an integer to the screen. No side-effects, but be ever vigilant
        so that your cup not overfloweth.
    */
    int drawInt( in int val, in vec2 pos, in vec2 size, in vec2 uv )
    {
        vec2 p = vec2(pos);
        float s = sign(float(val));
        val *= int(s);
        
        int c = drawIntCarriage(val,p,size,uv,1);
        if( s<0.0 ) c |= drawChar(CH_HYPH,p,size,uv);
        return c;
    }

    /*
        Prints a fixed point fractional value. Be even more careful about overflowing.
    */
    int drawFixed( in float val, in int places, in vec2 pos, in vec2 size, in vec2 uv )
    {
        float fval, ival;
        fval = modf(val, ival);
        
        vec2 p = vec2(pos);
        
        // Draw the floating point part.
        int res = drawIntCarriage( int( fval*pow(10.0,float(places)) ), p, size, uv, places );
        // The decimal is tiny, so we back things up a bit before drawing it.
        p.x += size.x*.4;
        res |= drawChar(CH_FSTP,p,size,uv); p.x-=size.x*1.2;
        // And after as well.
        p.x += size.x *.1;
        // Draw the integer part.
        res |= drawIntCarriage(int(ival),p,size,uv,1);
        return res;
    }

    int text( in vec2 uv, const float size )
    {
        vec2 charSize = vec2( size*vec2(MAP_SIZE)/iResolution.y );
        vec2 charSizeSmall = charSize / 2.0;
        float spaceSize = float( size*float(MAP_SIZE.x+1)/iResolution.y );
            
        // and a starting position.
        vec2 charPos = vec2(-0.25, -0.02);

        // Draw some text!
        int chr = 0;
        // Bitmap text rendering!
        chr += drawChar( CH_D, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_E, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_B, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_U, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_G, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_BLNK, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_T, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_E, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_X, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_T, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_EXCL, charPos, charSize, uv); charPos.x += spaceSize;

        // top left: red
        charPos = vec2(-0.45, 0.25);

        vec4 tl = texture(texture_0, vec2(0.1, 0.9));
        chr += drawChar( CH_LPAR, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(tl.r), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_COMM, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(tl.g), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_COMM, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(tl.b), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_RPAR, charPos, charSize, uv); charPos.x += spaceSize;

        // top right: green
        charPos = vec2(0.05, 0.25);

        vec4 tr = texture(texture_0, vec2(0.9, 0.9));
        chr += drawChar( CH_LPAR, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(tr.r), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_COMM, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(tr.g), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_COMM, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(tr.b), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_RPAR, charPos, charSize, uv); charPos.x += spaceSize;

        // bottom left: blue
        charPos = vec2(-0.45, -0.25);

        vec4 bl = texture(texture_0, vec2(0.1, 0.1));
        chr += drawChar( CH_LPAR, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(bl.r), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_COMM, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(bl.g), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_COMM, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(bl.b), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_RPAR, charPos, charSize, uv); charPos.x += spaceSize;

        // bottom right: cyan
        charPos = vec2(0.05, -0.25);

        vec4 br = texture(texture_0, vec2(0.9, 0.1));
        chr += drawChar( CH_LPAR, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(br.r), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_COMM, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(br.g), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_COMM, charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawInt(int(br.b), charPos, charSize, uv); charPos.x += spaceSize;
        chr += drawChar( CH_RPAR, charPos, charSize, uv); charPos.x += spaceSize;
        
        return chr;
    }

    ''',
    False
)

planeMapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Coincident::Impl',
    True,
    '''
    //VTK::Coincident::Impl
    //fragOutput0 = vec4(1.0, 0.0, 0.0, 0.5);

    // Get Y-normalized UV coords.
	// vec2 uv = fragCoord / iResolution.y;
    vec2 uv = vertexVCVSOutput.xy / iResolution.y;

    // Draw some text!
    //float txt = float( text(uv, .3.5) );
    float txt = float( text(uv, .01) );

    if (txt != 0.0) {
        fragOutput0 = vec4(txt,txt,txt,1.0);
    }
    ''',
    False
)

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
# renderer.GetActiveCamera().Elevation(-30)
# renderer.GetActiveCamera().Roll(-20)
renderer.ResetCameraClippingRange()
renWin.Render()
iren.Start()
