'''
Refrence: https://github.com/SQRLab/beam_curve_fit/blob/master/beam-profiler.py 
This code is able to read various folders containing images (.tif) 
of the diffrent wavelength lasers. 
It takes the individul folder reads the image and then fits it to the 
gaussian beam. 
This is done for every folder read of the various lasers and then all
plotted against eachother dependent on the first folder to dertimine 
where their beam waist are located relative to each other 

'''

import os
from PIL import Image
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#Gaussian functions 
def gaussianbeam(x, a, m, w, offs):
    return a*np.exp(-2*(x-m)**2/w**2)+ offs

def waist_function(z, w0, z0, off):
     #Gaussian funciton waist
    return w0*np.sqrt(1+((z-off)/z0)**2)

#Another definition for comapring multiple folders
def waist(root):
    #can modify this for diffrent folder names
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
    #Plot where w_0 is at 0 
    return wavelength, distance,xDiameter, yfit, popt

#getting the imformation and plotting on a plot
#**Change the name of the folder to the name that your images are stored in
name1, d1,diameter_1, y_1,popt1 = waist('397_25') 
name2,d2,diameter_2, y_2, popt2 =  waist('422_25')
name3,d3,diameter_3, y_3, popt3 = waist('375_25') 

fig,(ax1,ax2)= plt.subplots(1,2, gridspec_kw={'width_ratios':[3,1]})
fig.tight_layout()
fig.set_figwidth(8)
fig.set_figheight(6)

#plotting imfo of the folders being called
#*If don't need to compare three beams can comment out sections

#first folder 
x = [d - popt1[2] for d in d1]
curvefitting = np.linspace(min(x), max(x), 1000)
ax1.scatter(np.array(x),diameter_1, color = 'm', label = '{}'.format(name1))

#second
x2 = [d- popt1[2]  for d in d2] # graphed on the scale of the first plot do subtracting popt1[2]
curve_fit1 =np.linspace(min(x2),max(x2), 1000)
ax1.scatter(np.array(x2),diameter_2, color = 'b', label = '{}'.format(name2))

#third
x3 = [d- popt1[2] for d in d3] #graphed on the scale of the first plot do subtracting popt1[2]
curve_fit2 =np.linspace(min(x3),max(x3), 1000)
ax1.scatter(x3,diameter_3, color = 'c', label = '{}'.format(name3) )

#curve fitting plot and labels
ax1.plot(curvefitting, y_1, color = 'm', label = '{}'.format(name1), linewidth = 2) #,popt1[0], popt1[2]))
ax1.plot(curve_fit1,y_2, color = 'b', label = '{}'.format(name2), linewidth = 2) # \n w\u2080 {:.3f} \n z\u2080 {:.3f}  '.format(name2,popt2[0], popt2[2]))
ax1.plot(curve_fit2, y_3, color = 'c', label = '{}'.format(name3), linewidth = 2)
ax1.set_title('Gaussian Beam Waist Comparison', fontsize = 18)
ax1.set_xlabel('z position (mm)',fontsize= 14)
ax1.set_ylabel('beam waist ($\mu$m)', fontsize = 14)
ax1.legend()


"""#table
# can comment this section out to not have the 
# table displayed
table_data = [
    [popt1[0], popt2[0], popt3[0]], #W_0
    [popt1[2], popt2[2], popt3[2]],  #Z_0
    [popt1[2]-popt1[2], popt2[2]-popt1[2], popt3[2]-popt1[2]] #z_0 (adjusted to the new axis)
]
print(popt2,popt1)
dec = np.around(table_data,3)
print(dec)
table = plt.table(cellText = dec,colLabels=[name1,name2, name3], rowLabels= ['w\u2080', 'z\u2080', 'diffrence z\u2080'],
                  loc= 'center') #, fontsize = 60)
#table = plt.table(cellText = dec,colLabels=[name1,name2, name3], rowLabels= ['w\u2080', 'z\u2080', 'diffrence z\u2080'],
#                  loc= 'center' , fontsize = 25)
table.set_fontsize(25)

table.scale(.8,6)"""
plt.axis('off')
plt.show()


