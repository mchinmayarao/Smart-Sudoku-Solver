print('\nSetting UP\n')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from utlis import *
import sudukoSolver
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

# Open directory dialog to choose a directory path
pathImage = filedialog.askopenfilename(title="Select File")

#pathImage = "Resources/6.jpg"

heightImg = 450
widthImg = 450

model = load_model("model.h5")

# 1. PREPARE THE IMAGE
img = cv2.imread(pathImage)

img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED

imgThreshold = preProcess(img)


# 2. FIND ALL COUNTOURS
imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS

# 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
biggest, maxArea = biggestContour(contours) # FIND THE BIGGEST CONTOUR

if biggest.size != 0:
    biggest = reorder(biggest)
    
    cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
    pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    imgDetectedDigits = imgBlank.copy()
    imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

    # 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
    imgSolvedDigits = imgBlank.copy()
    boxes = splitBoxes(imgWarpColored)
   
    # cv2.imshow("Sample",boxes[65])
    numbers = getPredection(boxes, model)
    print("\nDetected numbers:\n",numbers)
    imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
    numbers = np.asarray(numbers)
    posArray = np.where(numbers > 0, 0, 1)
    #print(posArray)


    #### 5. FIND SOLUTION OF THE BOARD
    board = np.array_split(numbers,9)
    #print(board)
    try:
        sudukoSolver.solve(board)
    except:
        pass
    print("\nFinal solution board:\n",board)
    flatList = []
    for sublist in board:
        for item in sublist:
            flatList.append(item)
    solvedNumbers =flatList*posArray
    imgSolvedDigits= displayNumbers(imgSolvedDigits,solvedNumbers)

    # 6. OVERLAY SOLUTION
    
    matrix = cv2.getPerspectiveTransform(pts2, pts1)  
    imgInvWarpColored = img.copy()
    imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
    inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)

    cv2.imshow('Input Image',img)
    cv2.imshow('Output Image',inv_perspective)
    

else:
    print("No Sudoku Found")

cv2.waitKey(0)