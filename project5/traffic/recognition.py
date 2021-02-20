import sys
from tensorflow import keras
from traffic import convertImg
import numpy as np
import cv2

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 recognition.py model.h5 img.ppm")
        sys.exit()

    # Load model
    model = keras.models.load_model(sys.argv[1])

    # Open and convert image
    imgPath = sys.argv[2]
    img = np.array(convertImg(imgPath)).reshape(1, 30, 30, 3)

    # Use model on image
    result = model.predict([img])
    category = result.argmax()
    probability = "{:.5%}".format(max(result[0]))

    # Show image with category and probability
    img = cv2.imread(imgPath)
    windowName = f'{category} {probability}'
    cv2.namedWindow(windowName, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(windowName, img)

    print()
    print(f'Category {category} with {probability} probability.')
    print("Press any key while window is active to exit.")

    # Wait for key press to exit
    cv2.waitKey()

if __name__ == "__main__":
    main()
