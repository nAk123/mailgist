'''
This is a modification of Andy's Worcloud generator
(Somehow he always ends up helping me :P)
Stumbled upon it while reading his blog
http://peekaboo-vision.blogspot.in/
'''

import random
import numpy as np

#from __future__ import division
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from query_integral_image import query_integral_image

FONT_PATH = "/usr/share/fonts/truetype/ttf-japanese-gothic.ttf"

def make_wordcloud(words, counts, fname, width=400, height=200,
                           margin=5, ranks_only=False):

    if len(counts) <= 0:
        print("We need at least 1 word to plot a word cloud, got %d."
                % len(counts))

    font_path = FONT_PATH
    max_count = float(max(counts))
    #normalize counts
    counts = counts/max_count
    #sort words by count
    inds = np.argsort(counts)[::-1]
    counts = counts[inds]
    words = words[inds]
    #create image
    img_grey = Image.new("L", (width, height))
    draw = ImageDraw.Draw(img_grey)
    integral = np.zeros((height, width), dtype=np.uint32)
    img_array = np.asarray(img_grey)
    font_sizes, positions, orientations = [], [], []
    # intitiallize font size "large enough"
    font_size = 1000
    # start drawing grey image
    for word, count in zip(words, counts):
        # alternative way to set the font size
        if not ranks_only:
            font_size = min(font_size, int(100 * np.log(count + 100)))
        while True:
            #try to find position
            font = ImageFont.truetype(font_path, font_size)
            #transpose font optionally
            orientation = random.choice([None, Image.ROTATE_90])
            transposed_font = ImageFont.TransposedFont(font,
                                                       orientation=orientation)
            draw.setfont(transposed_font)
            #get size of resulting text
            box_size = draw.textsize(word)
            #finding possible places using integral images
            result = query_integral_image(integral, box_size[1] + margin,
                                            box_size[0] + margin)
            if (result is not None or font_size == 0) :
                break
            #if we didn't find space make the font smaller
            font_size -= 1

        if font_size == 0:
            break

        x, y = np.array(result) + margin // 2
        # actually draw the text
        draw.text((y, x), word, fill="white")
        positions.append((x, y))
        orientations.append(orientation)
        font_sizes.append(font_size)
        # recompute integral image
        img_array = np.asarray(img_grey)
        # recompute bottom right
        # the order of the cumsum's is important for speed ?!
        partial_integral = np.cumsum(np.cumsum(img_array[x:, y:], axis=1),
                                     axis=0)
        if x > 0:
            if y > 0:
                partial_integral += (integral[x - 1, y:]
                                     - integral[x - 1, y - 1])
            else:
                partial_integral += integral[x - 1, y:]
        if y > 0:
            partial_integral += integral[x:, y - 1][:, np.newaxis]

        integral[x:, y:] = partial_integral

    # redraw in color
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    everything = zip(words, font_sizes, positions, orientations)
    for word, font_size, position, orientation in everything:
        font = ImageFont.truetype(font_path, font_size)
        #transpose font optionally
        transposed_font = ImageFont.TransposedFont(font,
                                                   orientation=orientation)
        draw.setfont(transposed_font)
        draw.text((position[1], position[0]), word,
                   fill="hsl(%d" % random.randint(0, 255) + ", 80%, 50%)")
    #img.show()
    img.save(fname)

def init_cloud(keywords):

    #from sklearn.feature_extraction.text import CountVectorizer

    #cv = CountVectorizer(min_df=1, charset_error="ignore"
    #                     stop_words="english", max_features=200)
    #counts = cv.fit_transform([text]).toarray().ravel()
    words = np.array([keyword[0] for keyword in keywords])
    # throw away some words, normalize
    #counts = counts[counts > 1]
    counts = np.array([(k[1] + k[2]) for k in keywords])
    counts = make_wordcloud(words, counts, "wordcloud.png")
