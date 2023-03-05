#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import PySimpleGUI as sg
import numpy as np
import pandas as pd
from pickle import load
from PIL import Image
from PIL import ImageOps

#import the dataset
dd1 = pd.read_excel('data.xlsx', sheet_name = 'data')
df=dd1.copy(deep=True)

t=32
td=35
td2=8

# define the range of values for each parameter
fc_range = [25, 62.62]
b_range = [80, 250]
d_range = [96, 359]
roh_range = [0.00452, 1.84]
fy_range = [334, 593]
massloss_range = [0, 34.8]


sg.theme('DefaultNoMoreNagging')

layout = [
    [sg.Text('Developed by Abushanab A., Wakjira T., Alnahhal W.')],
            [sg.Text('University of British Columbia Okanagan, Qatar University')],
            [sg.Text('Contact: tgwakjira@gmail.com, www.tadessewakjira.com/Contact')],
            #[sg.Text('Input parameters')],
    [
      sg.Column(layout=[
            [sg.Frame(layout=[
            [sg.Text('Beam width',size=(t, 1)),sg.InputText(key='-f1-', size=(td2,1)),sg.Text('mm')],
            [sg.Text('Beam effective depth',size=(t, 1)),sg.InputText(key='-f2-', size=(td2,1)),sg.Text('mm')],            
            [sg.Text('Concrete compressive strength',size=(t, 1)),sg.InputText(key='-f3-', size=(td2,1)),sg.Text('MPa')],
            [sg.Text('Longitudinal reinforcement ratio',size=(t, 1)),sg.InputText(key='-f4-', size=(td2,1)),sg.Text('--')],        
            [sg.Text('Steel yield strength',size=(t, 1)), sg.InputText(key='-f5-', size=(td2,1)),sg.Text('MPa')],
            [sg.Text('Mass loss or corrosion level',size=(t, 1)), sg.InputText(key='-f6-', size=(td2,1)),sg.Text('%')]],

            title='Input parameters')],
        ], justification='left'),
        
            
            
            sg.Column(layout=[
            [sg.Frame(layout=[
             
            [sg.Text('80 mm ≤ b ≤ 250 mm')],
            [sg.Text('96 mm ≤ d ≤ 359 mm')],
            [sg.Text('25 MPa ≤ fc ≤ 62.62 MPa')], 
            [sg.Text('0.00452 ≤ roh ≤ 1.84')],
            [sg.Text('334 MPa ≤ fy ≤ 593 MPa')],
            [sg.Text('0.0 ≤ mass loss ≤ 34.8%')]],
            title='Range of applications of the model')],            
            
        ], justification='center') 
  ],
[sg.Frame(layout=[   
            [sg.Text('Flexural capacity (M)',size=(32, 1)), sg.InputText(key='-OP-', size=(td2,1)),sg.Text('kN.m')]],
                      title='Output')],
            [sg.Button('Predict'),sg.Button('Cancel')]
]


# Open the images
img1 = Image.open('image1.png')
img2 = Image.open('image2.png')
img3 = Image.open('image3.png')

# Get the minimum width and height among the images
widths = [img1.width, img2.width, img3.width]
heights = [img1.height, img2.height, img3.height]
min_width = min(widths)
min_height = min(heights)

# Resize the images to the minimum size
img1 = ImageOps.fit(img1, (min_width, min_height))
img2 = ImageOps.fit(img2, (min_width, min_height))
img3 = ImageOps.fit(img3, (min_width, min_height))

# Define the scale factor
scale_factor = 0.8

# Resize the images
img1 = img1.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img2 = img2.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img3 = img3.resize((int(min_width * scale_factor), int(min_height * scale_factor)))

# Save the resized images
img1.save('image11.png')
img2.save('image22.png')
img3.save('image33.png')

# To add figures in two columns
fig1 = sg.Image(filename='image11.png', key='-fig1-', size=(min_width * scale_factor, min_height * scale_factor))
fig2 = sg.Image(filename='image22.png', key='-fig2-', size=(min_width * scale_factor, min_height * scale_factor))
fig3 = sg.Image(filename='image33.png', key='-fig3-', size=(min_width * scale_factor, min_height * scale_factor))


# # To add description of the image
# fig1_desc = sg.Text('Image 1')
# fig2_desc = sg.Text('Image 2')
layout += [[sg.Column([[sg.Text('Authors: Abushanab A., Wakjira T., Alnahhal W.')],
                [sg.Text('Contact: tgwakjira@gmail.com,'+ '\n'
                         '             www.tadessewakjira.com/Contact')],
            ],
            element_justification='left'
        ),
        sg.Column(
            [   [fig1,
                fig2,
                fig3,],
            ],
            element_justification='center'
        ),
    ]
]


# Create the Window
window = sg.Window('ML-based flexural capacity prediction of corroded RC beams', layout)

filename = 'main1_model.pkl'
model = load(open(filename, 'rb'))


while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'Predict':
        try:
            # get the input values
            b = float(values['-f1-'])
            d = float(values['-f2-'])
            fc = float(values['-f3-'])
            roh = float(values['-f4-'])
            fy = float(values['-f5-'])
            massloss = float(values['-f6-'])
            
            # check if the input values are within the defined range
            if fc < fc_range[0] or fc > fc_range[1]:
                sg.popup("Concrete compressive strength (fc) must be between 25 MPa and 62.62 MPa.")
                continue   
            if b < b_range[0] or b > b_range[1]:
                sg.popup("Beam width (b) must be between 80 mm and 250 mm.")
                continue                
            if d < d_range[0] or d > d_range[1]:
                sg.popup("Beam effective depth (d) must be between 96 mm and 359 mm.")
                continue                
            if roh < roh_range[0] or roh > roh_range[1]:
                sg.popup("Reinforcement ratio must be between 0.00452 and 1.84.")
                continue                
            if fy < fy_range[0] or fy > fy_range[1]:
                sg.popup("Yield strength (fy) must be between 334 MPa and 593 MPa.")
                continue                
            if massloss < massloss_range[0] or massloss > massloss_range[1]:
                sg.popup("Mass loss must be between 0% and 34.8%.")
                continue  
            
            df11=np.array([[fc, b, d, roh, fy, massloss]])
            df1=pd.DataFrame(df11)
#           # normalize the user defined variables
            dfn=[]
            for i in range(0,df1.shape[1]):
#                 a = (df1.iloc[:,i]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
                a = (df1.iloc[:,i][0]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
                dfn.append(a)

            dfn = pd.DataFrame(np.array(dfn)).T.values           
            
            # make the prediction
            prediction = model.predict(dfn)[0]
            y_pred = prediction
            
            # Inverse normalization
            # observed responses
            yy1 = df['Flexure'].values

            # predicted responses
            y1=round(yy1.min()+(yy1.max()-yy1.min()) * y_pred, 2)
            
            window['-OP-'].update(np.round(y1,2))
  
        except:
            sg.popup("Invalid input. Please make sure to enter numeric values and make sure the input values are within the defined range.")
            continue         
                    
            
window.close()

