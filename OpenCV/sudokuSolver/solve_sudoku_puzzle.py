import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# import the necessary packages
import cv2
import imutils
import numpy as np
from sudoku import Sudoku
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from .pyimagesearch.sudoku import find_puzzle
from .pyimagesearch.sudoku import extract_digit



# Manupulate image to the better form and get ROI
def get_roi(digit , erode = False):

    # Get contours
    cnts = cv2.findContours(digit.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    cnt = cv2.boundingRect(max(cnts, key=lambda x: cv2.contourArea(x)))

    # Extract digit from image
    num = digit[cnt[1]:cnt[1] + cnt[3], cnt[0]:cnt[0] + cnt[2]]

    # resize and put it into Mask
    r = 90
    num = cv2.resize(num, (round((num.shape[1] * r / num.shape[0]) - 0.5), r))

    mask = np.ones((128, 128), np.uint8)

    side_shape = round((((128 - num.shape[1]) / 2) - 0.5))
    mask[19:109, side_shape:side_shape + num.shape[1]] = num


    roi_im = mask
    if erode:
        th = cv2.threshold(roi_im, 0, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((3, 3), np.uint8)
        roi_im = cv2.erode(th, kernel, iterations=1)

    # Prepare for prediction
    roi = roi_im.astype("float") / 255.0
    roi = img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)

    return roi


def solve(image, model, debug_is=False):

    # load the input image from disk and resize it
    image = imutils.resize(image, width=600)

    # find the puzzle in the image and then
    (puzzleImage, warped) = find_puzzle(image, debug=debug_is)

    # initialize our 9x9 sudoku board
    board = np.zeros((9, 9), dtype="int")

    # a sudoku puzzle is a 9x9 grid (81 individual cells), so we can
    # infer the location of each cell by dividing the warped image
    # into a 9x9 grid
    stepX = warped.shape[1] // 9
    stepY = warped.shape[0] // 9

    # loop over the grid locations
    for y in range(0, 9):

        for x in range(0, 9):
            # compute the starting and ending (x, y)-coordinates of the
            # current cell
            startX = x * stepX
            startY = y * stepY
            endX = (x + 1) * stepX
            endY = (y + 1) * stepY

            # crop the cell from the warped transform image and then
            # extract the digit from the cell
            cell = warped[startY:endY, startX:endX]
            digit = extract_digit(cell, debug=debug_is)

            # verify that the digit is not empty
            if digit is not None:

                # resize the cell to 128x128 pixels and then prepare the
                # cell for classification
                roi = get_roi(digit)

                # classify the digit and update the sudoku board with the
                # prediction
                pred = model.predict(roi).argmax(axis=1)[0]
                board[y, x] = pred


    # construct a sudoku puzzle from the board
    puzzle = Sudoku(3, 3, board=board.tolist())
    # puzzle.show()

    # solve the sudoku puzzle
    solution = puzzle.solve()
    # solution.show_full()


    return solution.board, board.tolist()


def main(dj_im):  # dj_im should be (request.FILES['file'].read())

    model = load_model('sudokuSolver\\output\\trained_model.h5')
    image = cv2.imdecode(np.fromstring(dj_im, np.uint8), cv2.IMREAD_COLOR)

    output, initial = solve(image, model)
    return output, initial
