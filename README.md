# Explaining codes:


## beam_curve_fit (Beam Profiler)
This code is can do beam curve fitting with an image of the beam. 
supported_formats = ['.tif', '.tiff', '.pgm', '.ppm']

An example:  
![curve_fit_1 copy](https://user-images.githubusercontent.com/56214423/233503579-7f7563ee-3dd4-4cbf-bbb3-d55d5f68c253.jpg)  

% python3.11 beam-profiler.py curve_fit_1.tif
![Figure_1](https://user-images.githubusercontent.com/56214423/233503605-e3978eb2-1e4e-484b-9f3e-afbe243cff04.png)  

## gaussianbeam_characterization
This code reads a folder then plots all the measurments (image data) to then characterize the beam.   
FILE NAME FORMAT:  
![Screenshot 2023-08-20 062510](https://github.com/mayradiaz5/beam_curve_fit/assets/115504456/115f966f-11e4-4de9-ab13-bb08cd20a5ca)  

Important to keep this format as it gets the distance from the name.    
Example of images:  
![Screenshot 2023-08-20 071450](https://github.com/mayradiaz5/beam_curve_fit/assets/115504456/7962fc42-af73-45b6-92e9-44563354ffa3)


Plot:  
![397_onlymeasurment](https://github.com/mayradiaz5/beam_curve_fit/assets/115504456/05d0c432-e998-4019-80d6-0776b6c60c76)


## comparing_gaussianbeam_characterization
This code reads multiple folders for each laser. (In here it is the 375, 397, and 422nm lasers)  
FILE NAME FORMAT:  
![Screenshot 2023-08-20 062510](https://github.com/mayradiaz5/beam_curve_fit/assets/115504456/115f966f-11e4-4de9-ab13-bb08cd20a5ca)  

Then, is able to get the waist of the beam at the loction that each image was taken and plot it to characterize the beams for all the folders.  
(This one being three diffrent folders for the 3 lasers)  
*Store folders in the same location as the code.  (included folders containing the images)
Can commentsection and make chamges to include data table for not.   
Data Table inluded:  
![data_table_included](https://github.com/mayradiaz5/beam_curve_fit/assets/115504456/dcccec4b-3e2b-4d92-9577-082a28a5d4ff)  

Data table not included:  
![no_datatable](https://github.com/mayradiaz5/beam_curve_fit/assets/115504456/c78a8704-f59a-4eb3-b72f-6648a095b0f7)

## centered_wasit_characterization
This code is similat to gaussianbeam_characterization just includes a plot that is centered at z=0.  

![twoplot](https://github.com/mayradiaz5/beam_curve_fit/assets/115504456/872f7f4b-647d-46fb-bcd0-2907657465aa)
