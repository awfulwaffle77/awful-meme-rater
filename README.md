# awful meme rater

## Documentation links

[praw.ini documentation](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#praw-ini)

[submission attributes](https://praw.readthedocs.io/en/latest/code_overview/models/submission.html#submission)

[install tesseract](https://nanonets.com/blog/ocr-with-tesseract/#preprocessingfortesseract)

[meme ocr](https://towardsdatascience.com/extract-text-from-memes-with-python-opencv-tesseract-ocr-63c2ccd72b69)
## Image pre-processing

### First try with skew, canny and median blur
```
# grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# angle = determine_skew(grayscale)
# rotated = rotate(image, angle, (0, 0, 0))

# img = cv2.Canny(cv2.medianBlur(image, 5), 100, 200)
```

### Second try with way more clearer text
```
img = cv2.bilateralFilter(image, 5, 55, 60)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, img = cv2.threshold(img, 240, 255, 1)
```

## Files
`generate_dataset.py`: generates the dataset while applying filters on the
image and performing OCR.

## K-Means
Managed to split images in 2 categories based on the *blackbox*(VGG16). 
Have to see based on further decisions which one is popular and which
one is not and if these are correct.

## *To do*
- interpret score and date as factors deciding if meme is popular or not
- train with the given data and crafted labels
- explain what the dataset consists of