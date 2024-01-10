import sys
#sys.path.append('/usr/local/lib/python3/dist-packages')
import adios2
import vtk
import numpy as np

# Initialize renderer and window
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

colors = vtk.vtkNamedColors()
backgroundColor = colors.GetColor3d("DarkSlateGray")
actorColor = colors.GetColor3d("Tomato")
axis1Color = colors.GetColor3d("Salmon")
axis2Color = colors.GetColor3d("PaleGreen")
axis3Color = colors.GetColor3d("LightSkyBlue")

cubeAxesActor = vtk.vtkCubeAxesActor()
cubeAxesActor.SetUseTextActor3D(1)
cubeAxesActor.SetCamera(renderer.GetActiveCamera())
cubeAxesActor.GetTitleTextProperty(0).SetColor(axis1Color)
cubeAxesActor.GetTitleTextProperty(0).SetFontSize(48)
cubeAxesActor.GetLabelTextProperty(0).SetColor(axis1Color)

cubeAxesActor.GetTitleTextProperty(1).SetColor(axis2Color)
cubeAxesActor.GetLabelTextProperty(1).SetColor(axis2Color)

cubeAxesActor.GetTitleTextProperty(2).SetColor(axis3Color)
cubeAxesActor.GetLabelTextProperty(2).SetColor(axis3Color)

cubeAxesActor.DrawXGridlinesOn()
cubeAxesActor.DrawYGridlinesOn()
cubeAxesActor.DrawZGridlinesOn()
cubeAxesActor.SetGridLineLocation(cubeAxesActor.VTK_GRID_LINES_FURTHEST)

cubeAxesActor.XAxisMinorTickVisibilityOff()
cubeAxesActor.YAxisMinorTickVisibilityOff()
cubeAxesActor.ZAxisMinorTickVisibilityOff()

cubeAxesActor.SetFlyModeToStaticEdges()
cubeAxesActor.SetBounds(-0.001, 0.001,-0.001, 0.001,-0.001, 0.001)
renderer.AddActor(cubeAxesActor)


filename = "/home/cc/warpx_run/diags/diagbeam1/openpmd_000200.bp"

with adios2.open(filename, "r") as fr:
    for fstep in fr:
    #x = fr.read("/data/1000/particles/beam/momentum/x")
        print(fr)
        # inspect variables in current step
        step_vars = fstep.available_variables()
        # print variables information
        for name, info in step_vars.items():
            print("variable_name: " + name)
            for key, value in info.items():
                print("\t" + key + ": " + value)
                print("\n")

        x = fstep.read("/data/200/fields/B/x")
        y = fstep.read("/data/200/fields/B/y")
        z = fstep.read("/data/200/fields/B/z")
        print(len(x))
        for i in range(0,len(x)):
            print(x[i])
        particle_types = ["beam", "driver", "plasma_e", "plasma_p"]

        for p_type in particle_types:
            x = fstep.read("/data/200/particles/"+p_type+"/position/x")
            y = fstep.read("/data/200/particles/"+p_type+"/position/y")
            z = fstep.read("/data/200/particles/"+p_type+"/position/z")
            xm = fstep.read("/data/200/particles/"+p_type+"/momentum/x")
            ym = fstep.read("/data/200/particles/"+p_type+"/momentum/y")
            zm = fstep.read("/data/200/particles/"+p_type+"/momentum/z")
            #print(xm, ym)
            mmt = []
            if len(x) == 0:
                continue
            points = vtk.vtkPoints()
            for i in range(len(x)):
                points.InsertNextPoint(x[i], y[i], z[i])
                mmt.append(np.linalg.norm([xm[i], ym[i], zm[i]])) 
            print(mmt[-1])
            print(xm[-1], ym[-1], zm[-1])
            lookUpTable = vtk.vtkLookupTable()
            lookUpTable.SetTableRange(min(mmt),max(mmt))
            lookUpTable.Build()
            uCharArray = vtk.vtkUnsignedCharArray()
            uCharArray.SetNumberOfComponents(3)
            uCharArray.SetName("colors")
        # Create a PolyData object and set the points to it
            polydata = vtk.vtkPolyData()
            polydata.SetPoints(points)
            

            for i in range(polydata.GetNumberOfPoints()):
                point = polydata.GetPoint(i)
    # Get the color from lookup table
                color = [0]*3
                lookUpTable.GetColor(mmt[i],color)
    # Convert each color to 255
                for j in range(len(color)):
                    color[j] = int(255 * color[j])
                uCharArray.InsertTypedTuple(i,color)


# # Set Scalars
            polydata.GetPointData().SetScalars(uCharArray)
        # Create a vertex glyph and set the PolyData object to it
            vertex_glyph = vtk.vtkVertexGlyphFilter()
            vertex_glyph.SetInputData(polydata)
            vertex_glyph.Update()
       
            #colorSeries = vtk.vtkColorSeries()
            #colorSeries.SetColorScheme(vtk.vtkColorSeries.BREWER_DIVERGING_SPECTRAL_11)

            #lut = vtk.vtkLookupTable()
            #colorSeries.BuildLookupTable(lut, vtk.vtkColorSeries.ORDINAL)
        # Map to window coordinates
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(vertex_glyph.GetOutputPort())
            #mapper.SetLookupTable(lut)
        # Create an actor and set the mapper to it
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
        
            renderer.AddActor(actor)

print("finish loading data")      
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()
colors = vtk.vtkNamedColors()

renderer.SetBackground(backgroundColor)
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(640, 480)
renderWindow.SetOffScreenRendering(1)
renderWindow.Render()

windowToImage = vtk.vtkWindowToImageFilter()
windowToImage.SetInput(renderWindow)

writer = vtk.vtkPNGWriter()
writer.SetFileName("test.png")
writer.SetInputConnection(windowToImage.GetOutputPort())
writer.Write()

