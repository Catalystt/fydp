from os import path
from fastai.imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *


# https://colab.research.google.com/drive/1E2ghzfV9GjRYcxlxwrxi7FzacARtBbQG#scrollTo=WPjt9Otkt4Pq

def most_by_mask(mask, mult):
    idxs = np.where(mask)[0]
    return idxs[np.argsort(mult * probs[idxs])[:4]]


def most_by_correct(y, is_correct):
    mult = -1 if (y == 1) == is_correct else 1
    return most_by_mask((preds == data.val_y) == is_correct & (data.val_y == y), mult)


PATH = path.abspath("../document-generator/output/")
sz = 224

arch = resnet34
data = ImageClassifierData.from_paths(PATH, tfms=tfms_from_model(arch, sz), bs=32)
learn = ConvLearner.pretrained(arch, data, precompute=True)
learn.fit(0.01, 3)

log_preds = learn.predict()
# log_preds.shape

preds = np.argmax(log_preds, axis=1)  # Take max value in each row
probs = np.exp(log_preds[:, 1])  # pr(dog)


def rand_by_mask(mask): return np.random.choice(np.where(mask)[0], 4, replace=False)


def rand_by_correct(is_correct): return rand_by_mask((preds == data.val_y) == is_correct)


def plots(ims, figsize=(12, 6), rows=1, titles=None):
    f = plt.figure(figsize=figsize)
    for i in range(len(ims)):
        sp = f.add_subplot(rows, len(ims) // rows, i + 1)
        sp.axis('Off')
        if titles is not None: sp.set_title(titles[i], fontsize=16)
        plt.imshow(ims[i])
        plt.show()


def load_img_id(ds, idx):
    img_path = path.join(PATH, ds.fnames[idx])
    img = PIL.Image.open(img_path)

    return np.array(img)


def plot_val_with_title(idxs, title):
    imgs = [load_img_id(data.val_ds, x) for x in idxs]
    title_probs = [probs[x] for x in idxs]
    print(title)
    return plots(imgs, rows=1, titles=title_probs, figsize=(16, 8))


# imgs = [load_img_id(data.val_ds, x) for x in idxs]

# print(log_preds)
# print(log_preds[:, 1])
# print(preds)
# print(probs)

for i in range(len(preds)):
    print(data.val_ds.fnames[i], preds[i], log_preds[i])

# plot_val_with_title(most_by_correct(0, True), "Most correct cats")
# plot_val_with_title(most_by_correct(1, True), "Most correct dogs")
# plot_val_with_title(most_by_correct(0, False), "Most incorrect cats")
# plot_val_with_title(most_by_correct(1, False), "Most incorrect dogs")

# most_uncertain = np.argsort(np.abs(probs -0.5))[:4]
# plot_val_with_title(most_uncertain, "Most uncertain predictions")
