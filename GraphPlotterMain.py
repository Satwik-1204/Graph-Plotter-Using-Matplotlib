import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from math import *
import numpy as np
from scipy.optimize import fsolve
class GraphPlotterApp:
 def __init__(self, root):
  self.root = root
  self.root.title("Equation Grapher with Intersections and Area")
  self.equations = []
  self.canvas = tk.Canvas(self.root)
  self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
  self.frame = tk.Frame(self.canvas)
  self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
  self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
  self.canvas.configure(yscrollcommand=self.scroll_y.set)
  self.canvas.pack(side="left", fill="both", expand=True)
  self.scroll_y.pack(side="right", fill="y")
  self.create_widgets(self.frame)
 def create_widgets(self, parent):
  tk.Label(parent, text="Enter equations (use ^ for power, e.g. x^2):").pack()
  self.equation_text = tk.Text(parent, height=5, width=50)
  self.equation_text.pack()
  range_frame = tk.Frame(parent)
  range_frame.pack()
  tk.Label(range_frame, text="x-min:").grid(row=0, column=0)
  self.xmin_entry = tk.Entry(range_frame, width=5)
  self.xmin_entry.insert(0, "-10")
  self.xmin_entry.grid(row=0, column=1)
  tk.Label(range_frame, text="x-max:").grid(row=0, column=2)
  self.xmax_entry = tk.Entry(range_frame, width=5)
  self.xmax_entry.insert(0, "10")
  self.xmax_entry.grid(row=0, column=3)
  tk.Label(range_frame, text="y-min:").grid(row=0, column=4)
  self.ymin_entry = tk.Entry(range_frame, width=5)
  self.ymin_entry.insert(0, "-10")
  self.ymin_entry.grid(row=0, column=5)
  tk.Label(range_frame, text="y-max:").grid(row=0, column=6)
  self.ymax_entry = tk.Entry(range_frame, width=5)
  self.ymax_entry.insert(0, "10")
  self.ymax_entry.grid(row=0, column=7)
  tk.Button(parent, text="Plot Equations", command=self.plot_equations).pack(pady=10)
  self.info_label = tk.Label(parent, text="", justify="left")
  self.info_label.pack()
  self.fig, self.ax = plt.subplots(figsize=(8, 6))
  self.canvas_plot = FigureCanvasTkAgg(self.fig, master=parent)
  self.canvas_plot.get_tk_widget().pack()
  self.toolbar = NavigationToolbar2Tk(self.canvas_plot, parent)
  self.toolbar.update()
  self.canvas_plot._tkcanvas.pack()
 def eval_safe(self, expr, x_val):
  return eval(expr, {"x": x_val, "sin": sin, "cos": cos, "tan": tan, "exp": exp, "log": log, "sqrt": sqrt, "pi": pi})
 def get_color(self, i, total):
  cmap = cm.get_cmap('tab20', total)
  return cmap(i)
 def plot_equations(self):
  self.ax.clear()
  self.info_label.config(text="")
  self.equations = [line.strip() for line in self.equation_text.get("1.0", "end").splitlines() if line.strip()]
  if len(self.equations) == 0:
   messagebox.showerror("Input Error", "Please enter at least one equation.")
   return
  try:
   x_min = float(self.xmin_entry.get())
   x_max = float(self.xmax_entry.get())
   y_min = float(self.ymin_entry.get())
   y_max = float(self.ymax_entry.get())
  except:
   messagebox.showerror("Range Error", "Invalid range values entered.")
   return
  x = np.linspace(x_min, x_max, 500)
  valid_eqns = []
  eqns_clean = []
  y_values = []
  for i, eq in enumerate(self.equations):
   try:
    eq_clean = eq.replace("^", "**")
    y = [self.eval_safe(eq_clean, xi) for xi in x]
    self.ax.plot(x, y, label=f"y = {eq}", color=self.get_color(i, len(self.equations)))
    valid_eqns.append(eq)
    eqns_clean.append(eq_clean)
    y_values.append(y)
   except Exception as e:
    messagebox.showwarning("Equation Error", f"Skipping equation '{eq}': {e}")
  info = ""
  intersections = []
  for i in range(len(eqns_clean)):
   for j in range(i + 1, len(eqns_clean)):
    eq1 = eqns_clean[i]
    eq2 = eqns_clean[j]
    def diff(x_val):
     return self.eval_safe(eq1, x_val) - self.eval_safe(eq2, x_val)
    guesses = np.linspace(x_min, x_max, 50)
    roots = []
    for g in guesses:
     try:
      root = fsolve(diff, g, xtol=1e-6)[0]
      if x_min <= root <= x_max and all(abs(root - r) > 1e-3 for r in roots):
       roots.append(round(root, 6))
     except:
      continue
    for r in roots:
     try:
      y_r = self.eval_safe(eq1, r)
      self.ax.plot(r, y_r, 'ko')
      self.ax.annotate(f'({r:.2f}, {y_r:.2f})', (r, y_r), fontsize=8)
      info += f"Intersection of y = {valid_eqns[i]} and y = {valid_eqns[j]}: ({r:.2f}, {y_r:.2f})\n"
      intersections.append(r)
     except:
      continue
  if len(eqns_clean) >= 2 and len(intersections) >= 2:
   try:
    eq1 = eqns_clean[0]
    eq2 = eqns_clean[1]
    def area_diff(x_val):
     return self.eval_safe(eq1, x_val) - self.eval_safe(eq2, x_val)
    roots = []
    for g in np.linspace(x_min, x_max, 50):
     try:
      root = fsolve(area_diff, g, xtol=1e-6)[0]
      if x_min <= root <= x_max and all(abs(root - r) > 1e-3 for r in roots):
       roots.append(round(root, 6))
     except:
      continue
    roots = sorted(roots)
    total_area = 0
    for i in range(len(roots) - 1):
     x_fill = np.linspace(roots[i], roots[i + 1], 200)
     y1_fill = [self.eval_safe(eq1, xi) for xi in x_fill]
     y2_fill = [self.eval_safe(eq2, xi) for xi in x_fill]
     area = np.trapz(np.abs(np.array(y1_fill) - np.array(y2_fill)), x_fill)
     total_area += area
     self.ax.fill_between(x_fill, y1_fill, y2_fill, color='lightcoral', alpha=0.4)
    info += f"\nArea enclosed between y = {valid_eqns[0]} and y = {valid_eqns[1]}: {total_area:.4f}"
   except Exception as e:
    info += f"\nError computing area: {e}"
  self.ax.set_xlim(x_min, x_max)
  self.ax.set_ylim(y_min, y_max)
  self.ax.axhline(0, color='black', linewidth=0.5)
  self.ax.axvline(0, color='black', linewidth=0.5)
  self.ax.grid(True)
  self.ax.legend()
  self.canvas_plot.draw()
  self.info_label.config(text=info.strip())
if __name__ == "__main__":
 root = tk.Tk()
 app = GraphPlotterApp(root)
 root.mainloop()
