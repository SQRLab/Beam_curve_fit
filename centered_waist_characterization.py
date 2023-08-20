'''
Format Idea (to make a diameter vs distance plot)
Refrence: https://github.com/SQRLab/beam_curve_fit/blob/master/beam-profiler.py 
This code characterizes a laser beam as well as centering it at 0.
'''
import os
from PIL import Image
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#Gaussian functions 
def gaussianbeam(x,a, m, w, offs):
    return a*np.exp(-2*(x-m)**2/w**2)+ offs

def waist_function(z, w0, z0, off):
     #Gaussian funciton waist
    return w0*np.sqrt(1+((z-off)/z0)**2)

# Reading from the folder 397 ,includes all the 
# images at diffrent distances (mm)
root = '397_25' #can modify this for diffrent folder names
fnames = os.listdir(root)
length = len(fnames)
wavelength = fnames[0][7:10]

# Saving the names, x and y diameter measured by the camera
# and the pixels into arrays for further calculations
filenames = [] 
xDiameter = []
w_stddevs = []

#getting the images and reading them to then determine the beam diameter
for i in range(length):
    filepaths = os.path.join(root, fnames[i])
    names = fnames[i] ## to get the distance that is in the name
    filenames.append(names)

    #getting the images
    img = Image.open(filepaths)
    im = np.asarray(img).astype(float)
    if len(im.shape) > 2:
        im = im.mean(axis = -1)
    pix_len = 4.84e-6 ##defult pixel length of the camera 

    # shape of the beam 
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
    #coveriance for w
    perr = np.sqrt(np.diag(cov)) ##the error needed in the plot
    w_stddevs.append(perr[2])

    px1=pix_len*1e6
    wx1=wx*pix_len*1e6
    xDiameter.append(wx1)   

### distances away from the lens 
distance = []
for k in range(len(filenames)):
    cameradistance = 17 # mm
    d = int(filenames[k][0:3]) + cameradistance
    distance.append(d)  

###ploting the data in a diameter vs distance plot
## curve fit of the data
w0_guess = min(xDiameter)
offset_guess = distance[np.argmin(xDiameter)]
popt, _ =  curve_fit(waist_function, distance,xDiameter, sigma = w_stddevs, p0=(w0_guess,50,offset_guess))
smoothvals = np.linspace(min(distance), max(distance), 1000)
#z, w0, z0, off
print('w_0 {}'.format(popt[0]))
yfit = waist_function(smoothvals, *popt)
print('z_0 {}'. format(popt[2]))

#diameter vs distance
plt.subplots(2,1, figsize=(8,9))
plt.scatter(distance,xDiameter, color = 'b', label = 'Expirimental')
plt.errorbar(distance, xDiameter, yerr =np.array(w_stddevs), ls = 'none', ecolor = 'b')
plt.title("Diameter of the beam vs Distance (for {} nm)".format(wavelength))
plt.xlabel('Distance in (mm)')
plt.ylabel('Diameter of the beam ($\mu$m)')
plt.plot(smoothvals, yfit, color = 'orange', label = 'gaussian beam waist ')
plt.tight_layout(pad = 1)
plt.legend()

#Plot where w_0 is at 0 
plt.subplot(2,1,1)
x = [d - popt[2] for d in distance]
curvefitting = np.linspace(min(x), max(x), 1000)
plt.plot(curvefitting, yfit, color = 'm', label = 'gaussian beam \n w\u2080 {:.3f} \n z\u2080 {:.3f}  '.format(popt[0], popt[2]))
plt.title('Gaussian Beam waist')
plt.xlabel('z position (mm)')
plt.ylabel('beam waist ($\mu$m)')
plt.tight_layout(pad = 1)
plt.legend()
plt.show()






