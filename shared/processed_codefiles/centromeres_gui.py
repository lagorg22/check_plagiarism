class CentromereAnalysisApp:
def __init__(self, root):
self.root = root
self.root.title("Centromere Distance Analysis")
self.root.geometry("500x300")
self.root.resizable(False, False)
self.data = None
self.result_df = None
self.input_file_path = None
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)
title_label = ttk.Label(main_frame, text="Centromere to Nuclear Periphery Distance Analysis",
font=("Arial", 14, "bold"))
title_label.pack(pady=(0, 20))
self.status_var = tk.StringVar()
self.status_var.set("Please upload a CSV file to begin analysis")
status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="gray")
status_label.pack(pady=(0, 20))
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)
upload_button = ttk.Button(button_frame, text="Upload CSV", command=self.upload_csv, width=20)
upload_button.grid(row=0, column=0, padx=10, pady=10)
self.calculate_button = ttk.Button(button_frame, text="Calculate", command=self.calculate_distances,
width=20, state=tk.DISABLED)
self.calculate_button.grid(row=1, column=0, padx=10, pady=10)
self.export_button = ttk.Button(button_frame, text="Export CSV", command=self.export_csv,
width=20, state=tk.DISABLED)
self.export_button.grid(row=2, column=0, padx=10, pady=10)
self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
self.progress.pack(pady=(20, 0), fill=tk.X)
def upload_csv(self):
file_path = filedialog.askopenfilename(
title="Select CSV file",
filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)
if file_path:
try:
self.progress['value'] = 10
self.root.update_idletasks()
self.data = pd.read_csv(file_path)
self.input_file_path = file_path
self.progress['value'] = 100
self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
self.calculate_button.config(state=tk.NORMAL)
messagebox.showinfo("Success", "CSV file loaded successfully!")
except Exception as e:
self.progress['value'] = 0
messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")
def calculate_distances(self):
if self.data is None:
messagebox.showerror("Error", "Please upload a CSV file first")
return
try:
self.progress['value'] = 10
self.root.update_idletasks()
self.data['Y'] = -self.data['Y']
nucleus = self.data.iloc[-1]
n_X = nucleus['X']
n_Y = nucleus['Y']
n_DiameterMax = nucleus['Feret']  # Major axis
n_DiameterMin = nucleus['MinFeret']  # Minor axis
n_RotAngle = nucleus['FeretAngle']  # Rotation angle in degrees
n_RadiusMax = n_DiameterMax / 2
n_RadiusMin = n_DiameterMin / 2
centromeres = self.data.iloc[:-1].copy()
self.progress['value'] = 30
self.root.update_idletasks()
distances_to_center = []
distances_to_edge_radial = []
distances_to_edge_shortest = []
distance_ratios = []
inside_ellipse = []
total_rows = len(centromeres)
for idx, centromere in centromeres.iterrows():
x = centromere['X']
y = centromere['Y']
d_center = self.distance_to_center(x, y, n_X, n_Y)
distances_to_center.append(d_center)
d_edge_radial = self.distance_to_edge(x, y, n_X, n_Y, n_RadiusMax, n_RadiusMin, n_RotAngle)
distances_to_edge_radial.append(d_edge_radial)
d_edge_shortest = self.shortest_distance_to_ellipse((x, y), n_X, n_Y, n_RadiusMax, n_RadiusMin, n_RotAngle)
distances_to_edge_shortest.append(abs(d_edge_shortest))
is_inside = d_edge_shortest <= 0
inside_ellipse.append(is_inside)
if is_inside:
ratio = d_center / d_edge_radial
else:
ratio = np.nan  # Not applicable for points outside
distance_ratios.append(ratio)
self.progress['value'] = 30 + (idx + 1) / total_rows * 50
self.root.update_idletasks()
centromeres['Distance_to_Center'] = distances_to_center
centromeres['Radial_Distance_to_Edge'] = [d_edge_radial - d_center if inside else np.nan
for d_edge_radial, d_center, inside in
zip(distances_to_edge_radial, distances_to_center, inside_ellipse)]
centromeres['Shortest_Distance_to_Edge'] = distances_to_edge_shortest
centromeres['Distance_Ratio'] = distance_ratios
centromeres['Inside_Ellipse'] = inside_ellipse
self.result_df = pd.concat([centromeres, self.data.iloc[[-1]]], ignore_index=False)
self.progress['value'] = 100
self.root.update_idletasks()
self.status_var.set("Calculation complete. Ready to export.")
self.export_button.config(state=tk.NORMAL)
messagebox.showinfo("Success", "Distance calculations completed successfully!")
except Exception as e:
self.progress['value'] = 0
messagebox.showerror("Error", f"Calculation failed: {str(e)}")
def export_csv(self):
if self.result_df is None:
messagebox.showerror("Error", "Please calculate results first")
return
if self.input_file_path:
directory = os.path.dirname(self.input_file_path)
basename = os.path.splitext(os.path.basename(self.input_file_path))[0]
suggested_name = f"{basename}_improved_analysis.csv"
initial_dir = directory
else:
suggested_name = "improved_centromere_distance_analysis.csv"
initial_dir = os.getcwd()
file_path = filedialog.asksaveasfilename(
title="Save Results",
defaultextension=".csv",
initialfile=suggested_name,
initialdir=initial_dir,
filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)
if file_path:
try:
self.progress['value'] = 50
self.root.update_idletasks()
self.result_df.to_csv(file_path, index=False)
self.progress['value'] = 100
self.status_var.set(f"Results saved to: {os.path.basename(file_path)}")
messagebox.showinfo("Success", "Results saved successfully!")
except Exception as e:
self.progress['value'] = 0
messagebox.showerror("Error", f"Failed to save file: {str(e)}")
def distance_to_center(self, x, y, center_x, center_y):
return np.sqrt((x - center_x)**2 + (y - center_y)**2)
def distance_to_edge(self, x, y, center_x, center_y, a, b, angle_deg):
angle_rad = np.deg2rad(angle_deg)
x_t = x - center_x
y_t = y - center_y
x_r = x_t * np.cos(-angle_rad) - y_t * np.sin(-angle_rad)
y_r = x_t * np.sin(-angle_rad) + y_t * np.cos(-angle_rad)
theta = np.arctan2(y_r, x_r)
r = (a * b) / np.sqrt((b * np.cos(theta))**2 + (a * np.sin(theta))**2)
return r
def transform_point(self, x, y, center_x, center_y, angle_rad):
x_t = x - center_x
y_t = y - center_y
x_r = x_t * np.cos(-angle_rad) - y_t * np.sin(-angle_rad)
y_r = x_t * np.sin(-angle_rad) + y_t * np.cos(-angle_rad)
return x_r, y_r
def inverse_transform(self, x_r, y_r, center_x, center_y, angle_rad):
x_t = x_r * np.cos(angle_rad) - y_r * np.sin(angle_rad)
y_t = x_r * np.sin(angle_rad) + y_r * np.cos(angle_rad)
x = x_t + center_x
y = y_t + center_y
return x, y
def shortest_distance_to_ellipse(self, point, center_x, center_y, a, b, angle_deg):
x, y = point
angle_rad = np.deg2rad(angle_deg)
x_r, y_r = self.transform_point(x, y, center_x, center_y, angle_rad)
if np.isclose(x_r, 0) and np.isclose(y_r, 0):
return -min(a, b)
def distance_function(t):
ellipse_x = a * np.cos(t)
ellipse_y = b * np.sin(t)
return (x_r - ellipse_x)**2 + (y_r - ellipse_y)**2
initial_t = np.arctan2(y_r / b, x_r / a)
result = minimize(distance_function, initial_t, method='BFGS')
t_min = result.x[0]
closest_x = a * np.cos(t_min)
closest_y = b * np.sin(t_min)
ellipse_point_x, ellipse_point_y = self.inverse_transform(closest_x, closest_y, center_x, center_y, angle_rad)
distance = np.sqrt((x - ellipse_point_x)**2 + (y - ellipse_point_y)**2)
if (x_r/a)**2 + (y_r/b)**2 < 1:
return -distance
return distance
def main():
root = tk.Tk()
app = CentromereAnalysisApp(root)
root.mainloop()
if __name__ == "__main__":
main()