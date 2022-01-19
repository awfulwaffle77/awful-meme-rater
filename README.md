# awful meme rater
![Pepe](https://emoji.gg/assets/emoji/9658-pepe-20.png) **<(How *awful* can this get?)**
## What the *heck* is a awful meme rater?

As the name says, it rates memes and it does an awful job while at it.
Please check the `Awful meme rater.pdf` document to get more in-depth
details than you would get here.

## Requirements

Creating the dataset requires [Tesseract](https://github.com/tesseract-ocr/) 
to use the python library.

## How does it work?

It has two files and each one does their thing. Remember, KISS (keep it 
simple, stupid)

`generate_dataset.py`:
- Gets memes from reddit.com/r/memes
- Stores the images and a `.attrs` file (detailed in the `.pdf`)

`kmeans.py`:
- Applies k-means to fit memes to `popular` and `unpopular` clusters
- You can add your own meme with your own .attrs file and see if you're
gonna reach hot

## Documentation links ![Pepe](https://emoji.gg/assets/emoji/1428-pepe-23.png)

[praw.ini documentation](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#praw-ini)

[submission attributes](https://praw.readthedocs.io/en/latest/code_overview/models/submission.html#submission)

[install tesseract](https://nanonets.com/blog/ocr-with-tesseract/#preprocessingfortesseract)

[feature extraction](https://keras.io/api/applications/#usage-examples-for-image-classification-models)

[tf-idf](https://www.geeksforgeeks.org/understanding-tf-idf-term-frequency-inverse-document-frequency/)

[meme ocr](https://towardsdatascience.com/extract-text-from-memes-with-python-opencv-tesseract-ocr-63c2ccd72b69)