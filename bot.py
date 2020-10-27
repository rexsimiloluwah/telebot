import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--name", required = True, help = "Please enter name")

args = vars(ap.parse_args())

print(args["name"])