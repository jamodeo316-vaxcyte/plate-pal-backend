import matplotlib.pyplot as plt
import numpy as np


def plot_standard_curve(data):
    curve_fit = data['curve_fit']

    x_values = curve_fit['x_values']
    y_values = curve_fit['y_values']
    slope = curve_fit['slope']
    intercept = curve_fit['intercept']
    r_squared = curve_fit['r_squared']

    curve_plot, ax = plt.subplots()
    ax.scatter(x_values, y_values, color='blue', s=50, alpha=0.7, label='Standards')
    ax.set_xlabel('Concentration (ug/mL)')
    ax.set_ylabel('Absorbance (AU)')
    ax.grid(True, alpha=0.3)

    x_line = np.array([min(x_values), max(x_values)])
    y_line = slope * x_line + intercept
    
    legend_text = 'Regression:\n'
    legend_text += f'y = {slope:.3f}x + {intercept:.3f}\n'
    legend_text += f'r² = {r_squared:.3f}'
    
    ax.plot(x_line, y_line, 'r--', linewidth=2, alpha=0.8, label=legend_text)
    ax.legend(fontsize=9)

    data['curve_plot'] = curve_plot
    
    return data
