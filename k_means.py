from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
import os
from sklearn.cluster import KMeans
import shutil
import matplotlib.pyplot as plt

PICS_PATH = "res/pics"
POPULAR_PATH = "res/popular"
NON_POPULAR_PATH = "res/non_popular"

model = VGG16(weights='imagenet', include_top=False)

vgg16_feature_list = []

all_pics_names = os.listdir(PICS_PATH)
pics_names = []

for fname in all_pics_names:
    if fname.split(".")[-1] == "attrs":
        continue
    pics_names.append(fname)

for i, fname in enumerate(pics_names):

    img_path = os.path.join(PICS_PATH, fname)

    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)

    vgg16_feature = model.predict(img_data)
    vgg16_feature_np = np.array(vgg16_feature)
    vgg16_feature_list.append(vgg16_feature_np.flatten())

vgg16_feature_list_np = np.array(vgg16_feature_list)
kmeans = KMeans(n_clusters=2, random_state=0).fit(vgg16_feature_list_np)

for idx, label in enumerate(kmeans.labels_):
    src = os.path.join(PICS_PATH, pics_names[idx])
    if label == 0:
        dest = POPULAR_PATH
    else:
        dest = NON_POPULAR_PATH
    shutil.copy(src, dest)

#plt.scatter()