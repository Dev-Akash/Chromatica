import numpy as np  # for processing tensors
import cv2          # for processing image
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog


# Initiallizing the Camera to start Video Capturing
cap = cv2.VideoCapture(-1)
# Placing the upper bound and lower bound of chroma in hsv
lb=np.array([0,0,0])        # lb=np.array([190,190,190])
ub=np.array([100,100,100])  # ub=np.array([255,255,255])
#count=0
#list_of_img = ['img.jpg','img1.jpg','img2.png','img3.jpg','img4.jpg','img5.jpg','space.jpg']
# kernel for performing the mrophological operation on the frames

kernel = np.ones((2,2),np.uint8)

flag = 0
filename = " "

root = Tk()
root.title("Chromatica")

# On exit release camera and destroy window.
def exit_():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", exit_)
lmain = Label(root)
lmain.pack(side= "left")
sidebar = PanedWindow(root)

chroma_header = LabelFrame(sidebar,text = "Chroma Settings")

var_red = IntVar()
red_scale = Scale(chroma_header, variable = var_red, to=255, orient = HORIZONTAL, label = "Red")
red_scale.pack(fill = "x", expand=1)

var_green = IntVar()
green_scale = Scale(chroma_header, variable = var_green, to=255, orient = HORIZONTAL, label = "Green")
green_scale.pack(fill = "x", expand=1)

var_blue = IntVar()

blue_scale = Scale(chroma_header, variable = var_blue, to= 255, orient = HORIZONTAL, label = "Blue")
blue_scale.pack(fill = "x", expand = 1)

chroma_header.pack(side = "top",fill= "x", expand= 1)

Input_image = LabelFrame(sidebar,text = "Backgound Image Setting")

path_labe = Label(Input_image, text = "Path")
path_labe.pack(fill="x", expand = 1)

path = Entry(Input_image)
path.pack(fill= "x", expand = 1, side = "left")

def browsefunc():
    filename = filedialog.askopenfilenames(filetypes=[("Pictures", "*.png |*.PNG | *.jpg |*.JPG")])
    path.insert(0,filename)

browsebutton = Button(Input_image, text="Browse", command=browsefunc)
browsebutton.pack(side= "right")

Input_image.pack(side = "top", fill = "x", expand= 1)

sidebar.pack(side= "top",fill = "both", expand=1)

def show_frame():
    # reading the image from the camera instance
    ret, frame = cap.read()
    # Reducing the noise, doing meadian bluring
    frame = cv2.medianBlur(frame,3)
    # Converting bgr color fromat to HSV format
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Masking image between upper bounds and lower bounds
    closing = cv2.inRange(rgb,lb,ub)
    # Appling Morphological operation to reduce noise
    closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel,iterations=1)
    
    # providing final input in canvas by combining frame and image
    canvas = frame.copy()
    canvas[closing != 0] =[0,0,0]
    print(flag)
    if(flag == 1):
        img = cv2.imread("{}".format(string_p))
        img = cv2.resize(img, (640,480))
        img[closing == 0]= [0,0,0]
        final = canvas + img
    # showing the final frame after combining both frame
    else:
        final = canvas#+img
    img = Image.fromarray(final)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    # inturrupt in while loop.
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
    #elif cv2.waitKey(1) & 0xFF == ord('f'):
    #    if count<len(list_of_img)-1:
    #        count=count+1
    #        img = list_of_img[count]
    #    else:
    #        count=0
    #elif cv2.waitKey(1) & 0xFF == ord('b'):
    #    if count>1:
    #        count=count-1
    #        img = list_of_img[count]
    #    else:
    #        count = len(list_of_img)-1
show_frame()
root.mainloop()
