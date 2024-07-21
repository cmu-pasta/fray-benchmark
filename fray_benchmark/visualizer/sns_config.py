import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid", {'axes.grid' : True})
# sns.set_context("paper", font_scale=2)
sns.set_theme(rc={'figure.figsize':(8, 3), "text.usetex": True})

plt.rcParams.update({'axes.edgecolor': 'black', 'axes.linewidth': 2,
   'axes.spines.top': False, 'axes.spines.right': False,
   'axes.spines.left': False,
   'axes.grid.axis': 'y', 'grid.linestyle': '--'})

colors = ['#F0A856', '#76A12B', '#284C67', '#E72388', '#EC321D', "#44AA99", "#C0C0C0"]
d_colors = [sns.desaturate(c, 0.65) for c in colors]
sns.palplot(colors)
sns.set_palette(sns.color_palette(colors), 8, .75)
line_style = dict(linewidth = 2, markersize = 8)