# Equation Grapher with Intersections and Area

A desktop application built with Python, Tkinter, and Matplotlib that plots mathematical equations, automatically finds their intersection points, and calculates the area enclosed between the first two functions.

## Features

* **Plot Multiple Equations**: Enter one or more equations in terms of `x` (e.g., `x^2`, `sin(x)`).
* **Dynamic Plotting**: Uses Matplotlib to render a high-quality graph.
* **Automatic Intersection Finding**: Uses SciPy's `fsolve` to numerically find and annotate all intersection points between all plotted curves.
* **Area Calculation**: Automatically calculates and shades the area enclosed between the *first two* valid equations entered, using `np.trapz` for numerical integration.
* **Interactive Toolbar**: Includes the Matplotlib navigation toolbar for zooming, panning, and saving the plot.

## Requirements

* Python 3
* Matplotlib
* NumPy
* SciPy

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Satwik-1204/equation-grapher-app.git](https://github.com/Satwik-1204/equation-grapher-app.git)
    cd equation-grapher-app
    ```

2.  **Install the required libraries:**
    ```bash
    pip install matplotlib numpy scipy
    ```

3.  **Run the application:**
    ```bash
    python graph_plotter.py
    ```

## How to Use

1.  Enter one or more equations in the text box. Use `^` for powers (e.g., `x^2`) and functions like `sin(x)`, `cos(x)`, `exp(x)`, `sqrt(x)`.
2.  Set the desired X and Y axis ranges.
3.  Click the **"Plot Equations"** button.
4.  The graph will display the plots, intersection points (marked with 'o'), and shaded area.
5.  Text results for intersection coordinates and the total calculated area will appear below the button.

## Limitations

* The area calculation is only performed for the **first two equations** in the list.
* The application only plots explicit functions of the form `y = f(x)`.
