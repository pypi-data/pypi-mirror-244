# General Info

# Installation 
```bash
>>> pip install OskarFieldModule
```

# Importing
```python
>>> import Field
```


Functions for calculating and plotting electromagnetic fields and potentials in 3d.

# Functions

## Efield, Epot
Field and potential from line charge parallel to x, y or z axis. Can be placed anywhere in 3D


## EfieldCircle, EpotCircle 
Field and potential from circle charge in origin

## BfieldLine
Field from line current parallel to x, y or z axis. Can be placed anywhere in 3D

## BfieldCircle
Field from circular current in origin

## PlotVector
Plots vector field. Customize colorscheme, density, and figsize

## PlotContour
Plots vector field. Customize colorscheme, levels, norm and figsize

## PlotCircle
Plots circle just using radius
    
# See example code below:

## Single Point Charge
```Python 
>>> L = 2
>>> N = 10
>>> Q = [1.0]
>>> r_Q = np.array([[0.0, 0.0, 0.0]])
>>> plane = 'xy'

>>> rx, ry, Ex, Ey = CalculateEfield(L, N, Q, r_Q, plane)
>>> PlotVector(rx, ry, Ex, Ey, 'quiver', show = True)

>>> N = 100
>>> rx, ry, V = CalculateEpot(L, N, Q, r_Q, plane)
>>> PlotContour(rx, ry, V, show=True)
## Double Point Charge Example     

>>> L = 2
>>> N = 100
>>> Q = [2.0, -2.0]
>>> r_Q = [-1, 1]
>>> r_Q = np.array([[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
>>> plane = 'xy'

>>> rx, ry, Ex, Ey = CalculateEfield(L, N, Q, r_Q, plane)
>>> PlotVector(rx, ry, Ex, Ey, 'stream', show = True, broken_streamlines = False)
```
### Point Charge Field
<img src="src/Example_Figures/PointCharge.jpg" width="400"/>

### Point Charge Potential
<img src="src/Example_Figures/PointChargeContour.jpg" width="400"/>

### Double Point Charge Field
<img src="src/Example_Figures/DoublePointCharge.jpg" width="400"/>


<!-- See [point charge field](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/PointCharge.pdf), [point charge potential](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/PointChargeContour.pdf) & [double point charge field](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/DoublePointCharge.pdf) -->

## Double Line Charge Example       
```Python
>>> L = 2
>>> N = 50
>>> line_charges = [-1, 1]
>>> line_lengths = [1, 1]
>>> line_center_coords = [[0, 0, -1], [0, 0, 1]]
>>> axis = ['x', 'x']
>>> plane = 'xz'

>>> rx, rz, Ex, Ez = CalculateEfieldLine(L, N, line_charges, line_lengths, line_center_coords, axis, plane)
>>> rx, rz, V = CalculateEpotLine(L, N, line_charges, line_lengths, line_center_coords, axis, plane)

>>> PlotVector(rx, rz, Ex, Ez, 'stream', broken_streamlines = False, show = True)
>>> PlotContour(rx, rz, V, show = True, norm = 'linear') 
```
### Line Charge Field
<img src="src/Example_Figures/DoubleLineCharge.jpg" width="400"/>

### Line Charge Potential
<img src="src/Example_Figures/DoubleLineChargeContour.jpg" width="400"/>

<!-- See [line charge field](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/DoubleLineCharge.pdf) & [line charge potential](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/DoubleLineChargeContour.pdf) -->

## Circular Charge Example
```python
>>> L = 5
>>> N = 100
>>> circle_charge = [5]
>>> radius = [2]
>>> plane = 'yz'
>>> plane_circles = ['yz']
>>> ry, rz, Ey, Ez = CalculateEfieldCircle(L, N, circle_charge, radius, plane, plane_circles)
>>> PlotVector(ry, rz, Ey, Ez, 'stream', show = False, equal = True)

>>> t = np.linspace(0, 2*np.pi, 100)
>>> plt.plot(radius[0]*np.cos(t), radius[0]*np.sin(t))
>>> plt.show()

>>> N = 500
>>> ry, rz, V = CalculateEpotCircle(L, N, circle_charge, radius, plane, plane_circles)
>>> PlotContour(ry, rz, V, show = False, equal = True)

>>> t = np.linspace(0, 2*np.pi, 100)
>>> plt.plot(radius[0]*np.cos(t), radius[0]*np.sin(t))
>>> plt.show()
```
### Circular Charge Field
<img src="src/Example_Figures/CircularCharge.jpg" width="400"/>

### Circular Charge Potential
<img src="src/Example_Figures/CircularChargeContour.jpg" width="400"/>

<!-- See [circular charge field](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/CircularCharge.pdf) & [circular charge potential](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/CircularChargeContour.pdf) -->

## Line Current Example
```python
>>> L = 5
>>> N = 24
>>> line_currents = [5]
>>> line_lengths = [1]
>>> line_center_coords = [[0.0, 0.0, 0.0]]
>>> axis = ['x']
>>> plane = 'yz'

>>> rx, rz, Bx, Bz = CalculateBfieldLine(L, N, line_currents, line_lengths, line_center_coords, axis, plane)

>>> PlotVector(rx, rz, Bx, Bz, 'quiver', title = 'Magnetic Field from Lin e Current', show = True)
```
### Line Current Magnetic Field
<img src="src/Example_Figures/LineCurrent.jpg" width="400"/>

<!-- See [B-field from line current](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/LineCurrent.pdf) -->

## Circular Current Example
```python
>>> L = 8
>>> N = 40
>>> circle_currents = [5]
>>> radii = [5]
>>> plane = 'xz'
>>> circle_planes = ['xy']
>>> rx, rz, Bx, Bz = CalculateBfieldCircle(L, N, circle_currents, radii, plane, circle_planes)

>>> PlotVector(rx, rz, Bx, Bz, 'stream', broken_streamlines=False, show = True, cmap = 'inferno', density = .5)   
```
### Circular Current Magnetic Field
<img src="src/Example_Figures/CircularCurrent.jpg" width="400"/>
<!-- See [B-field from circular current](https://github.com/Oskar-Idland/Oskar-Field-Module/blob/main/src/Example_Figures/CircularCurrent.pdf) -->

[GitHub](https://github.com/Oskar-Idland/Oskar-Field-Module)
