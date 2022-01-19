import praw
import requests
import os
import cv2
import pytesseract
import enchant
import math
import numpy as np
from typing import Tuple, Union

RESOURCES_FOLDER = os.path.join(os.getcwd(), "res\\pics\\")
PYTESSERACT_CONFIG = r"--oem 3 --psm 11"


def rotate(  # function from deskew github
        image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)


def write_attrs(_submission, _reference_name, save_line):
    f = open(RESOURCES_FOLDER + _reference_name + ".attrs", "w", encoding="utf-8")
    f.write("title=" + str(str(_submission.title).encode("utf-8"))+ "\n")  # some titles had emojis..
    f.write("score=" + str(_submission.score) + "\n")
    f.write("created_utc=" + str(_submission.created_utc) + "\n")
    if save_line != "":
        f.write("text=" + save_line + "\n")
    f.close()


def all_words_correct(line):
    all_blank = True
    for word in line:
        if word == "":
            continue
        if not d.check(word):
            return False
        else:
            all_blank = False
    if not all_blank:
        return True
    else:
        return False


def meets_requirements(_submission):
    if _submission.score < 1000:
        return False
    return True


if __name__ == "__main__":

    d = enchant.Dict("en_US")

    # cont = input("Folder " + RESOURCES_FOLDER + " will be emptied. Continue? y/N ")
    cont = "y"

    if cont == "y":
        print("Removing contents of " + RESOURCES_FOLDER + "..")
        files = RESOURCES_FOLDER
        for f in os.listdir(files):
            os.remove(os.path.join(files, f))

    reddit = praw.Reddit("dataset_bot", user_agent="Dataset bot")

    reddit.read_only = True

    subreddit = reddit.subreddit("memes")

    # Uses idx just for testing purposes. Should be removed later
    for idx, submission in enumerate(subreddit.hot(limit=200)):
        if submission.url[-3:] != "png" and submission.url[-3:] != "jpg" and submission.url[-3:] != "jpeg":
            continue

        reference_name = submission.url.split("/")[-1]
        reference_name_no_ext = submission.url.split("/")[-1].split(".")[0]

        print(str(idx) + " " + submission.url)

        img_data = requests.get(submission.url).content
        with open(RESOURCES_FOLDER + reference_name_no_ext + ".jpeg", 'wb') as handler:
            handler.write(img_data)

            image = cv2.imread(RESOURCES_FOLDER + reference_name_no_ext + ".jpeg")
            # grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # angle = determine_skew(grayscale)
            # rotated = rotate(image, angle, (0, 0, 0))

            img = cv2.bilateralFilter(image, 5, 55, 60)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(img, 240, 255, 1)
            # img = cv2.Canny(cv2.medianBlur(image, 5), 100, 200)

            # cv2.namedWindow('img', cv2.WINDOW_KEEPRATIO)
            # cv2.imshow("img", img)
            # cv2.resizeWindow('img', 800, 800)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            text = pytesseract.image_to_string(img, lang='eng', config=PYTESSERACT_CONFIG)

            text_lines = text.split("\n")
            final_line = ""
            for line in text_lines:
                save_line = ""
                words = line.split(" ")
                if all_words_correct(words):
                    final_line += " ".join(words) + "\n"

            final_line = final_line.replace("\n", " ")
            print(final_line)

        write_attrs(submission, reference_name_no_ext, final_line)

