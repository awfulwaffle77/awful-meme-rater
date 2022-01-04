import praw
import requests
import os
import cv2
import pytesseract
import enchant
import re

RESOURCES_FOLDER = os.path.join(os.getcwd(), "res\\")


def write_attrs(_submission, _reference_name, save_line):
    f = open(RESOURCES_FOLDER + _reference_name + ".attrs", "w", encoding="utf-8")
    f.write("title=" + str(_submission.title) + "\n")
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
        if submission.url[-3:] != "png" and submission.url[-3:] != "jpg":
            continue

        reference_name = submission.url.split("/")[-1]
        reference_name_no_ext = submission.url.split("/")[-1].split(".")[0]

        print(str(idx) + " " + submission.url)

        img_data = requests.get(submission.url).content
        with open(RESOURCES_FOLDER + reference_name, 'wb') as handler:
            handler.write(img_data)

            img = cv2.Canny(cv2.medianBlur(cv2.imread(RESOURCES_FOLDER + reference_name, cv2.IMREAD_GRAYSCALE), 5), 100, 200)
            cv2.imshow("img", img)
            cv2.waitKey(0)
            text = pytesseract.image_to_string(img)

            text_lines = text.split("\n")
            final_line = ""
            for line in text_lines:
                save_line = ""
                words = line.split(" ")
                if all_words_correct(words):
                    final_line += " ".join(words) + "\n"

            print(final_line)

        write_attrs(submission, reference_name_no_ext, final_line)

