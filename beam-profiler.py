# coding: utf-8
# In[ ]:
# Reference: https://gist.github.com/carmelom/4dd407d307b2fb1dc99b017835ce8432

import numpy as np
from PIL import Image

from scipy.optimize import curve_fit

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, help="image name")
parser.add_argument("-l", "--pix-len", type=float, help="camera pixel size [m]", default="4.84e-6") #1800U 500m pixel size is 2.2 * 2.2
parser.add_argument("-p", "--pow", type=float, help="Total beam power [W]",)

parser.add_argument("--no-plot", action="store_true",
                    help="suppress plotting the output")
                    
args = parser.parse_args()


# supported_formats = ['.tif', '.tiff', '.pgm', '.ppm']


name = args.name

im = Image.open(name)
im = np.asarray(im).astype(float)
if len(im.shape) > 2:
    im = im.mean(axis=-1)
    
def gaussianbeam(x, a, m, w, offs):
    return a*np.exp(-2*(x-m)**2/w**2) + offs



pix_len = args.pix_len
Pow = args.pow if args.pow is not None else np.nan

Isat = 6.26 # mW/cm^2, Na D2 transition

h, w = im.shape
x = np.arange(w)
y = np.arange(h)


# fit x
xdata = x
ydata = im.sum(0)
# a, m, w, offs
p0 = (ydata.max(), xdata.max()/2, xdata.max()/4, im[0,0])
px, cov = curve_fit(gaussianbeam, xdata, ydata, p0)
mx, wx = px[1], abs(px[2])

# fit y
xdata = y
ydata = im.sum(1)
# a, m, w, offs
p0 = (ydata.max(), xdata.max()/2, xdata.max()/4, im[0,0])
py, cov = curve_fit(gaussianbeam, xdata, ydata, p0)
my, wy = py[1], abs(py[2])

# calculate other quantities
if args.pow is None:
    print("No input power specified")
    
I0 = 0.2*Pow/(np.pi*wx*wy*pix_len**2)
isat = I0/Isat
omega = 0.5 * np.sqrt(isat)

text = """
Gaussian beam intensity fit

pixel size: {px:g} um

waist x: {wx:g} um
waist y: {wy:g} um

I0: {i0:.2f} mW/cm^2
+ I/I_sat: {isat:.2f} 
+ Rabi fr: {omega:.2f} Gamma
""".format(px=pix_len*1e6, wx=wx*pix_len*1e6, wy=wy*pix_len*1e6, i0=I0, isat=isat, omega=omega)
print(text)

# plot
print("Plotting: ", not args.no_plot)
if not args.no_plot:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
    fig, [[ax_y, ax_im], [ax_text, ax_x]] = plt.subplots(2,2,  figsize=(12,12),
                                             gridspec_kw={'height_ratios':[2,1], 'width_ratios':[1,2]},)
    
    ax_im.imshow(im, origin='lower')
    ax_im.axis('off')

    ax_im.get_shared_x_axes().join(ax_im, ax_x)
    ax_im.get_shared_y_axes().join(ax_im, ax_y)



    ax_x.plot(x, im.sum(0))
    ax_x.plot(x, gaussianbeam(x, *px), 'r')
    ax_x.grid()


    ax_y.plot(im.sum(1), y)
    ax_y.plot(gaussianbeam(y, *py), y, 'r')
    ax_y.grid()

    e = Ellipse((mx, my), 2*wx, 2*wy, color='none', ec='w', linestyle='--')
    ax_im.add_patch(e)

    ax_text.text(-0.05, 0.6, text, ha='left', va='center', fontdict={'family': 'monospace', 'size': 14})
    ax_text.axis('off')
    plt.show()


