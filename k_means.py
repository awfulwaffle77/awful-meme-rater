import tensorflow as tf
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
import os
from sklearn.cluster import KMeans
import shutil
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

PICS_PATH = "res\\pics"
POPULAR_PATH = "res\\popular"
NON_POPULAR_PATH = "res\\non_popular"
KMEAN_NULL_VALUE = 0
KMEAN_NULL_STRING_VALUE = ""
POSSIBLE_KEYS = ["title", "score", "created_utc", "text"]

tested_meme = "7lzlz0zl0jc81.jpg"
# tested_meme = KMEAN_NULL_STRING_VALUE

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


def copy_to_folders():
    for idx, label in enumerate(kmeans.labels_):
        src = os.path.join(PICS_PATH, pics_names[idx])
        if label == 0:
            dest = POPULAR_PATH
        else:
            dest = NON_POPULAR_PATH
        shutil.copy(src, dest)


def get_attr_in_dict(filename, cust_dict=None):
    if cust_dict is None:
        cust_dict = attr_dict_expl
    current_keys = [i for i in POSSIBLE_KEYS]

    filename = filename.split(".")[0]
    filename = filename + ".attrs"
    f = open(filename, "r")
    lines = f.readlines()

    for line in lines:
        key = line.split("=")[0]
        value = line.split("=")[1]
        cust_dict[key].append(value)
        current_keys.remove(key)
    if len(current_keys) != 0:
        for i in current_keys:
            cust_dict[i].append(KMEAN_NULL_STRING_VALUE)


def init_attr_dict_expl(custom_dict=None):
    if custom_dict is None:
        custom_dict = attr_dict_expl
    custom_dict["title"] = []
    custom_dict["score"] = []
    custom_dict["created_utc"] = []
    custom_dict["text"] = []


def get_tfidf_score(category, categ_array, cust_dict=None):  # get score for each category
    if cust_dict is None:
        cust_dict = attr_dict_expl
    score_array = []
    for text in cust_dict[category]:
        length = len(text)
        tfidf_sum = 0
        text = text.split(" ")
        for word in text:
            if word in categ_array:  # if in some strange case word doesn't exist, let me finish this project on time
                tfidf_sum += categ_array[word]
            else:
                length -= 1  # do not take into account if word is not in dict
        score_array.append(tfidf_sum / len(text))  # so it is not biased towards longer sentences
    return score_array


def get_tfidf_dict(category):  # get a dictionary of words in the category and their re
    _x = vectorizer.fit(attr_dict_expl[category])
    return dict(zip(_x.get_feature_names(), _x.idf_))


def get_feature_list():
    print("Getting feature list..")
    for i, fname in enumerate(pics_names):
        if fname != tested_meme:
            img_path = os.path.join(PICS_PATH, fname)
        else:
            print("Is this the last one?", str(i), " with len ", len(pics_names))
            # img_path = fname
            break

        get_attr_in_dict(img_path)  # get rid of .jpeg, ".attrs" is added in func
        # TODO: To replace with get_data_for_prediction
        img = image.load_img(img_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)

        vgg16_feature = model.predict(img_data)
        vgg16_feature_np = np.array(vgg16_feature)
        # until here
        vgg16_feature_list.append(vgg16_feature_np.flatten())


def print_best_words(tfidf):
    sorted_ = dict(sorted(tfidf.items(), key=lambda item: item[1], reverse=True))
    for idx, (key, value) in enumerate(sorted_.items()):
        if idx > 10:
            break
        print(str(idx), ". ", key)
    print(" ")


def get_data_for_prediciton(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)

    vgg16_feature = model.predict(img_data)
    vgg16_feature_np = np.array(vgg16_feature)

    get_attr_in_dict(img_path, cust_dict=our_meme_dict)
    test_feature_list.append(vgg16_feature_np.flatten())
    return vgg16_feature_np.flatten()  # no need?


def normalize(arr):
    arr_sum = sum(arr)
    if arr_sum == 0:
        arr_sum = 1
    return [float(i) / arr_sum for i in arr]

print("Setting up the model..")
model = VGG16(weights='imagenet', include_top=False)
vectorizer = TfidfVectorizer()
pics_names = []

attr_dict_expl = dict()  # explicit attributes
init_attr_dict_expl()

attr_dict = dict()
vgg16_feature_list = []
test_feature_list = []
all_pics_names = os.listdir(PICS_PATH)  # path of all files from pics, with

# Artificially apppend our data!
# all_pics_names.append("7lzlz0zl0jc81.jpg")
# all_pics_names.append("7lzlz0zl0jc81.attrs")
our_meme_dict = dict()

for fname in all_pics_names:
    if fname.split(".")[-1] == "attrs":
        continue
    pics_names.append(fname)

get_feature_list()
vgg16_feature_list_np = np.array(vgg16_feature_list)  # features of images
df = pd.DataFrame(vgg16_feature_list_np)  # you can also cluster a dataframe

text_tfidf = get_tfidf_dict("text")
title_tfidf = get_tfidf_dict("title")

#   TEST
init_attr_dict_expl(our_meme_dict)
get_data_for_prediciton(tested_meme)
test_df = pd.DataFrame(np.array(test_feature_list))
test_text_score = normalize(get_tfidf_score("text", text_tfidf, cust_dict=our_meme_dict))
test_title_score = normalize(get_tfidf_score("title", text_tfidf, cust_dict=our_meme_dict))
test_df["text"] = test_text_score
test_df["title"] = test_title_score
#   TEST

text_score = get_tfidf_score("text", text_tfidf)
title_score = get_tfidf_score("title", title_tfidf)

n_text_score = normalize(text_score)
n_title_score = normalize(title_score)

print("Text best words: ")
print_best_words(text_tfidf)

print("Title best words: ")
print_best_words(title_tfidf)

df["text"] = n_text_score
df["title"] = n_title_score

kmodel = KMeans(n_clusters=2, random_state=0)
train = kmodel.fit(df)
test = kmodel.predict(test_df)
labels = KMeans(n_clusters=2, random_state=0).fit_predict(df)


avg_score = sum(list(map(int, attr_dict_expl["score"]))) / len(attr_dict_expl["score"])
print("Average upvote score is ", str(avg_score))
matches = dict()
sc = attr_dict_expl["score"]
for idx, label in enumerate(labels):
    if idx == len(labels) - 1:  # do not take into account last picture, our meme
        break
    if int(sc[idx]) > avg_score:
        if str(label) not in matches:
            matches[str(label)] = 1
        else:
            matches[str(label)] += 1

if matches["0"] > matches["1"]:
    res = "0"
else:
    res = "1"

print("The popular label is: ", res)

if test[0] == res:
    print("Your meme is popular!")
else:
    print("Maybe try another meme..")
