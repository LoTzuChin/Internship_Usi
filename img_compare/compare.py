# coding = utf-8
from skimage.metrics import structural_similarity
import matplotlib.pyplot as plt
import numpy as np
import cv2

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB. astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err

def compare_images(imageA, imageB, title):

    m = mse(imageA, imageB)
    s = structural_similarity(imageA, imageB)

    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap='gray')
    plt.axis("off")
    plt.tight_layout()
    plt.show()


original1 = cv2.imread("high/r0a3c52a0t.png")
contrast1 = cv2.imread("high/r0a3c52a0t.png")
shopped1 = cv2.imread("low/r0a3c52a0t.png")

original1 = cv2.cvtColor(original1, cv2.COLOR_BGR2GRAY)
contrast1 = cv2.cvtColor(contrast1, cv2.COLOR_BGR2GRAY)
shopped1 = cv2.cvtColor(shopped1, cv2.COLOR_BGR2GRAY)

fig = plt.figure("Images")
images = ("Original", original1), ("Enhance", contrast1), ("Others", shopped1)

for (i, (name, image)) in enumerate(images):
    ax = fig.add_subplot(1, 3, i+1)
    ax.set_title(name)
    plt.imshow(image, cmap='gray')
    plt.axis("off")
plt.tight_layout()
plt.show()

compare_images(original1, original1, "original vs original")
compare_images(original1, contrast1, "original vs enhance")
compare_images(original1, shopped1, "original vs others")