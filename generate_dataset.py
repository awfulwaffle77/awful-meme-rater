import praw
import requests
import os

RESOURCES_FOLDER = os.path.join(os.getcwd(), "res\\")


def write_attrs(_submission, _reference_name):
    f = open(RESOURCES_FOLDER + _reference_name + ".attrs", "w")
    f.write("title=" + str(_submission.title) + "\n")
    f.write("score=" + str(_submission.score) + "\n")
    f.write("created_utc=" + str(_submission.created_utc) + "\n")
    f.close()


def meets_requirements(_submission):
    if _submission.score < 1000:
        return False
    return True


if __name__ == "__main__":

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

        write_attrs(submission, reference_name_no_ext)

