# Smart-Sudoku-Solver


This project is a Sudoku solver application that uses image processing techniques and machine learning to solve Sudoku puzzles from input images. It provides a user-friendly interface to select an image file containing a Sudoku puzzle and generates the solved puzzle as an output.

## Features

- Preprocesses the input image by converting it to grayscale, applying a Gaussian blur, and adaptive thresholding.
- Identifies the Sudoku puzzle in the image by finding the biggest contour.
- Warps the image to get a top-down view of the puzzle.
- Splits the puzzle into individual cells and uses a trained machine learning model to predict the numbers in each cell.
- Solves the Sudoku puzzle using a backtracking algorithm.
- Displays the detected numbers and the solved puzzle on the original image.
- Provides an interactive Jupyter Notebook (`test.ipynb`) for step-by-step code execution and debugging.

## Prerequisites

- Python 3.x
- OpenCV
- NumPy
- TensorFlow

## Usage

1. Clone the repository: `git clone https://github.com/mchinmayarao/Smart-Sudoku-Solver.git`
2. Run the application: `python app.py`
3. Select an image file containing a Sudoku puzzle using the file dialog.
4. View the original image, detected numbers, and the solved puzzle.

## Notebooks

The `test.ipynb` notebook provides a step-by-step breakdown of the code used in the application. It allows you to run and debug code cells individually, making it easier to understand and modify the code.


Feel free to use and modify the code according to your needs.


