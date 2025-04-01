import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.optimize import minimize
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

class CentromereAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Centromere Distance Analysis")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Variables to store data
        self.data = None
        self.result_df = None
        self.input_file_path = None
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title_label = ttk.Label(main_frame, text="Centromere to Nuclear Periphery Distance Analysis", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Please upload a CSV file to begin analysis")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="gray")
        status_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Upload button
        upload_button = ttk.Button(button_frame, text="Upload CSV", command=self.upload_csv, width=20)
        upload_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Calculate button
        self.calculate_button = ttk.Button(button_frame, text="Calculate", command=self.calculate_distances, 
                                         width=20, state=tk.DISABLED)
        self.calculate_button.grid(row=1, column=0, padx=10, pady=10)
        
        # Export button
        self.export_button = ttk.Button(button_frame, text="Export CSV", command=self.export_csv, 
                                       width=20, state=tk.DISABLED)
        self.export_button.grid(row=2, column=0, padx=10, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=(20, 0), fill=tk.X)
    
    def upload_csv(self):
        """Open file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Reset progress
                self.progress['value'] = 10
                self.root.update_idletasks()
                
                # Read CSV file
                self.data = pd.read_csv(file_path)
                self.input_file_path = file_path
                
                # Update progress
                self.progress['value'] = 100
                
                # Update status
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
                self.calculate_button.config(state=tk.NORMAL)
                
                messagebox.showinfo("Success", "CSV file loaded successfully!")
                
            except Exception as e:
                self.progress['value'] = 0
                messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")
    
    def calculate_distances(self):
        """Calculate distances between centromeres and nucleus periphery"""
        if self.data is None:
            messagebox.showerror("Error", "Please upload a CSV file first")
            return
        
        try:
            # Reset progress
            self.progress['value'] = 10
            self.root.update_idletasks()
            
            # Invert Y coordinates
            self.data['Y'] = -self.data['Y']
            
            # Last row contains the nucleus ellipse parameters
            nucleus = self.data.iloc[-1]
            n_X = nucleus['X']
            n_Y = nucleus['Y']
            n_DiameterMax = nucleus['Feret']  # Major axis
            n_DiameterMin = nucleus['MinFeret']  # Minor axis
            n_RotAngle = nucleus['FeretAngle']  # Rotation angle in degrees
            
            # Calculate radii
            n_RadiusMax = n_DiameterMax / 2
            n_RadiusMin = n_DiameterMin / 2
            
            # Extract centromere coordinates (all rows except the last one)
            centromeres = self.data.iloc[:-1].copy()
            
            # Update progress
            self.progress['value'] = 30
            self.root.update_idletasks()
            
            # Calculate distances for each centromere
            distances_to_center = []
            distances_to_edge_radial = []
            distances_to_edge_shortest = []
            distance_ratios = []
            inside_ellipse = []
            
            total_rows = len(centromeres)
            
            for idx, centromere in centromeres.iterrows():
                x = centromere['X']
                y = centromere['Y']
                
                # Calculate distance from centromere to nucleus center
                d_center = self.distance_to_center(x, y, n_X, n_Y)
                distances_to_center.append(d_center)
                
                # Calculate distance from nucleus center to periphery through centromere (original method)
                d_edge_radial = self.distance_to_edge(x, y, n_X, n_Y, n_RadiusMax, n_RadiusMin, n_RotAngle)
                distances_to_edge_radial.append(d_edge_radial)
                
                # Calculate shortest distance to periphery (new method)
                d_edge_shortest = self.shortest_distance_to_ellipse((x, y), n_X, n_Y, n_RadiusMax, n_RadiusMin, n_RotAngle)
                distances_to_edge_shortest.append(abs(d_edge_shortest))
                
                # Check if point is inside ellipse
                is_inside = d_edge_shortest <= 0
                inside_ellipse.append(is_inside)
                
                # Calculate ratio (percentage of distance from center to periphery)
                # Only calculate for points inside the ellipse
                if is_inside:
                    ratio = d_center / d_edge_radial
                else:
                    ratio = np.nan  # Not applicable for points outside
                
                distance_ratios.append(ratio)
                
                # Update progress bar
                self.progress['value'] = 30 + (idx + 1) / total_rows * 50
                self.root.update_idletasks()
            
            # Add results to the dataframe
            centromeres['Distance_to_Center'] = distances_to_center
            centromeres['Radial_Distance_to_Edge'] = [d_edge_radial - d_center if inside else np.nan 
                                                     for d_edge_radial, d_center, inside in 
                                                     zip(distances_to_edge_radial, distances_to_center, inside_ellipse)]
            centromeres['Shortest_Distance_to_Edge'] = distances_to_edge_shortest
            centromeres['Distance_Ratio'] = distance_ratios
            centromeres['Inside_Ellipse'] = inside_ellipse
            
            # Combine centromere data with nucleus data
            self.result_df = pd.concat([centromeres, self.data.iloc[[-1]]], ignore_index=False)
            
            # Update progress
            self.progress['value'] = 100
            self.root.update_idletasks()
            
            # Update status
            self.status_var.set("Calculation complete. Ready to export.")
            self.export_button.config(state=tk.NORMAL)
            
            messagebox.showinfo("Success", "Distance calculations completed successfully!")
            
        except Exception as e:
            self.progress['value'] = 0
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")
    
    def export_csv(self):
        """Export results to a CSV file"""
        if self.result_df is None:
            messagebox.showerror("Error", "Please calculate results first")
            return
        
        # Get suggested filename from input file
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
                # Reset progress
                self.progress['value'] = 50
                self.root.update_idletasks()
                
                # Save to CSV
                self.result_df.to_csv(file_path, index=False)
                
                # Update progress
                self.progress['value'] = 100
                
                # Update status
                self.status_var.set(f"Results saved to: {os.path.basename(file_path)}")
                
                messagebox.showinfo("Success", "Results saved successfully!")
                
            except Exception as e:
                self.progress['value'] = 0
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    # Helper functions copied from original script
    def distance_to_center(self, x, y, center_x, center_y):
        """Calculate distance from a point to the center of the ellipse"""
        return np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    def distance_to_edge(self, x, y, center_x, center_y, a, b, angle_deg):
        """Calculate distance from center to ellipse edge through a point"""
        # Convert angle to radians
        angle_rad = np.deg2rad(angle_deg)
        
        # Translate point to origin
        x_t = x - center_x
        y_t = y - center_y
        
        # Rotate point to align ellipse with axes
        x_r = x_t * np.cos(-angle_rad) - y_t * np.sin(-angle_rad)
        y_r = x_t * np.sin(-angle_rad) + y_t * np.cos(-angle_rad)
        
        # Calculate angle to the point in the unrotated system
        theta = np.arctan2(y_r, x_r)
        
        # Calculate distance to ellipse edge along the line from center to point
        r = (a * b) / np.sqrt((b * np.cos(theta))**2 + (a * np.sin(theta))**2)
        
        return r
    
    def transform_point(self, x, y, center_x, center_y, angle_rad):
        """Transform a point from the original coordinate system to the ellipse's coordinate system"""
        # Translate
        x_t = x - center_x
        y_t = y - center_y
        
        # Rotate
        x_r = x_t * np.cos(-angle_rad) - y_t * np.sin(-angle_rad)
        y_r = x_t * np.sin(-angle_rad) + y_t * np.cos(-angle_rad)
        
        return x_r, y_r
    
    def inverse_transform(self, x_r, y_r, center_x, center_y, angle_rad):
        """Transform a point from the ellipse's coordinate system back to the original"""
        # Rotate back
        x_t = x_r * np.cos(angle_rad) - y_r * np.sin(angle_rad)
        y_t = x_r * np.sin(angle_rad) + y_r * np.cos(angle_rad)
        
        # Translate back
        x = x_t + center_x
        y = y_t + center_y
        
        return x, y
    
    def shortest_distance_to_ellipse(self, point, center_x, center_y, a, b, angle_deg):
        """Calculate the shortest distance from a point to an ellipse"""
        x, y = point
        angle_rad = np.deg2rad(angle_deg)
        
        # Transform point to ellipse coordinate system
        x_r, y_r = self.transform_point(x, y, center_x, center_y, angle_rad)
        
        # If point is at origin (center of ellipse), return -min(a, b)
        if np.isclose(x_r, 0) and np.isclose(y_r, 0):
            return -min(a, b)
        
        # Function to minimize: squared distance from point to a point on the ellipse
        def distance_function(t):
            # Parametric equation of ellipse
            ellipse_x = a * np.cos(t)
            ellipse_y = b * np.sin(t)
            
            # Calculate squared distance
            return (x_r - ellipse_x)**2 + (y_r - ellipse_y)**2
        
        # Initial guess: angle from center to point
        initial_t = np.arctan2(y_r / b, x_r / a)
        
        # Find t that minimizes the distance
        result = minimize(distance_function, initial_t, method='BFGS')
        t_min = result.x[0]
        
        # Calculate the closest point on the ellipse
        closest_x = a * np.cos(t_min)
        closest_y = b * np.sin(t_min)
        
        # Transform back to original coordinate system
        ellipse_point_x, ellipse_point_y = self.inverse_transform(closest_x, closest_y, center_x, center_y, angle_rad)
        
        # Calculate the distance
        distance = np.sqrt((x - ellipse_point_x)**2 + (y - ellipse_point_y)**2)
        
        # If point is inside ellipse, return negative distance
        if (x_r/a)**2 + (y_r/b)**2 < 1:
            return -distance
        
        return distance

def main():
    root = tk.Tk()
    app = CentromereAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()