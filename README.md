# awful meme rater
 and the fellowship of 🍜(ramen) code
## Documentation links

[praw.ini documentation](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#praw-ini)

[submission attributes](https://praw.readthedocs.io/en/latest/code_overview/models/submission.html#submission)

[install tesseract](https://nanonets.com/blog/ocr-with-tesseract/#preprocessingfortesseract)

[feature extraction](https://keras.io/api/applications/#usage-examples-for-image-classification-models)

[tf-idf](https://www.geeksforgeeks.org/understanding-tf-idf-term-frequency-inverse-document-frequency/)

[meme ocr](https://towardsdatascience.com/extract-text-from-memes-with-python-opencv-tesseract-ocr-63c2ccd72b69)
## Image pre-processing

*complete here with the filter balancing stuff from meme ocr*

## Plotting?

VGG116 outputs a *ton* of features. Too many dimensions to plot, sorry.

## How the prediction is done in kmeans

Stick a new picture that is reduced to features into the dataframe and 
then use kmeans on all of the dataframe. As kmeans uses the centroids to
determine the label, we get to see how close the new image's features
are to the centroids.

## What is popular and what is not?

The method is the simplest possible. We take the scores of the training
images, compute a score(as in upvotes) average and what is over it means
popular; what is below means unpopular.

## Creating clusters with more features
vgg16_feature_list_np has 25088 features. Let's see how to add more.

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

## Before normalization
Only 2 labels are 1 for some reason. I suspect the last two columns to
have a very big impact. First normalize them and then try to remove
them.

## After normalization
`norm = [float(i)/sum(raw) for i in raw]`

to normalize against the sum to ensure that the sum is 
always 1.0 (or as close to as possible).

## Issues
Apparently if I add the same image 2 times, kmeans goes crazy and becomes
**super** biased towards that image, rejecting all other points. Probably
depends on image features a lot too.

## *To do*
- interpret score and date as factors deciding if meme is popular or not
- train with the given data and crafted labels
- explain what the dataset consists of

*NEW*

- ~~vectorize words into numbers(?) and stick them in the dataframe, then
apply kmeans~~

- plot some scores bro, or sth relevant