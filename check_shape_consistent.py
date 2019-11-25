import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import operator
import argparse
import os


def check_shape(masks_path, depth_path):

    imgs = []
    deps = []

    for idx, filename in enumerate(sorted(os.listdir(masks_path))):
        if idx > 1 and idx < 98:
            pass
        im = Image.open(masks_path+filename)
        imgs.append(np.array(im.getdata()).reshape(288, 288))

    for idx, filename in enumerate(sorted(os.listdir(depth_path))):
        if idx > 1 and idx < 98:
            pass
        dm = Image.open(depth_path+filename)
        deps.append(np.array(dm.getdata()).reshape(288, 288))

    imgs = np.array(imgs).reshape(-1, 288, 288)
    deps = np.array(deps).reshape(-1, 288, 288)

    new_imgs = imgs.copy()
    depth_mask = np.multiply((deps[0] == deps[1]), (deps[-1] == deps[-2]))
    # use depth mask to disregard small area of folded panel as a potential mask
    for i in range(imgs.shape[0]):
        unique, counts = np.unique(imgs[i][depth_mask], return_counts=True)
        unique = dict(zip(unique, counts))
        sorted_uniq = sorted(unique, key=unique.get)
        for j, k in enumerate(sorted_uniq):
            new_imgs[i][imgs[i]==k] = j * 20

    consistent_count = 0
    # abnormal = []
    # for i in range(1, new_imgs.shape[0]):
    #     if np.all(new_imgs[i] == new_imgs[i-1]):
    #         consistent_count += 1
    #     else:
    #         abnormal.append(i)

    # depth may be consistent across neiboring frames but different between
    # the inital frame and last frame due to different panel configuration
    # so expand mask horizontally to disregard that row entirely
    for i in range(len(depth_mask)):
        if not np.all(depth_mask[i]):
            depth_mask[i, :] = False

    if np.all(new_imgs[0][depth_mask] == new_imgs[-1][depth_mask]):
        consistent_count += 1

    return consistent_count
    # print(masks_path)
    # print("consistent_count: ", consistent_count)
    # print("abnormal transitions: ", abnormal)





parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store', dest='filename', help='file of directory addresses')
args = parser.parse_args()

f = open(args.filename, 'r')
dirs = f.readlines()

for dirname in dirs:
    masks_path = dirname[:-1] + '/masks/'
    depth_path = dirname[:-1] + '/depth/'
    score = check_shape(masks_path, depth_path)
    print(dirname, score)
    with open('answer.txt', 'a') as ans:
        ans.write('%s %d\n' % (dirname[:-1], score))


# for dirname in sorted(os.listdir(args.path)):
#     masks_path = args.path + dirname + '/masks/'
#     depth_path = args.path + dirname + '/depth/'
#     check_shape(masks_path, depth_path)
