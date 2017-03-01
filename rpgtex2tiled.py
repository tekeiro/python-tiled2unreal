#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
from PIL import Image


#  *****************  Constants  ***********************
FINAL_IMG_ROWS = 4
FINAL_IMG_COLS = 4
TILE_WIDTH = 32
TILE_HEIGHT = 32
MINI_TILE_WIDTH = 16
MINI_TILE_HEIGHT = 16
TERRAIN_WIDTH = 64
TERRAIN_HEIGHT = 96
REGIONS = (
    (16, 48),   # 0 - No walls
    (0, 32),    # 1 - Free Corner top-left
    (32, 32),   # 2 - Free Corner top-right
    (0, 64),    # 3 - Free Corner bottom-left
    (32, 64),   # 4 - Free Corner bottom-right
    (0, 48),    # 5 - Left wall
    (32, 48),   # 6 - Right wall
    (16, 32),   # 7 - Top wall
    (16, 64),   # 8 - Bottom wall
    (32, 0),    # 9 - Corner top-left
    (48, 0),    # 10 - Corner top-right
    (32, 16),   # 11 - Corner bottom-left
    (48, 16),   # 12 - Corner bottom-right
)
CORNERS_CROP = {
    9:  (0, 0),
    10: (16, 0),
    11: (0, 16),
    12: (16, 16),
}
#  ******************************************************


def origin2box(x, y, width=TILE_WIDTH, height=TILE_HEIGHT):
    return (x, y, x+width, y+height)


def part_image(img):
    """
    Part an RPG Maker texture into subimages for each
    tile
    :param img: {PIL.Image}  Image that its a RPG Maker terrain texture 
    :return: Array of Images for each tile
    """
    imgs = []
    blank_img = None
    for i,region in enumerate(REGIONS):
        if i < 9:
            new_img = img.crop(origin2box(
                region[0], region[1],
                TILE_WIDTH, TILE_HEIGHT
            )).copy()
            if i == 0:
                blank_img = new_img
            imgs.append(new_img)
        else:
            new_img = Image.new("RGBA", (TILE_WIDTH, TILE_HEIGHT))
            new_img.paste(blank_img.copy())
            tmp_img = img.crop(origin2box(
                region[0], region[1],
                MINI_TILE_WIDTH, MINI_TILE_HEIGHT
            )).copy()
            new_img.paste(tmp_img, box=CORNERS_CROP[i])
            imgs.append(new_img)
    return imgs


def spritesheet(rows, columns, imgs):
    if len(imgs) > 0:
        first_img = imgs[0]
        width, height = first_img.size
        result_img = Image.new("RGBA", (width*columns, height*rows))
        r, c = 0, 0

        for i, img in enumerate(imgs):
            r, c = int(i / columns), int(i % columns)
            result_img.paste(img, box=(int(c*width), int(r*height)))
        return result_img
    else:
        return None


def calculate_rows_cols(imgs):
    cols = int(math.sqrt(len(imgs)))
    rows = int(len(imgs) / cols)+1
    return rows, cols


if __name__ == '__main__':
    img_path = sys.argv[1]
    out_img_path = 'new_' + img_path

    image = Image.open(img_path)
    img_width, img_height = image.size
    print("Image size: ({0}, {1})".format(
        img_width, img_height
    ))
    all_imgs = []
    r, c, keep_w, keep_h = 0, 0, True, True

    while keep_h:
        r1 = int((r + 1) * TERRAIN_HEIGHT)
        c = 0

        if r1 > img_height:
            keep_h = False
            continue

        keep_w = True
        while keep_w:
            c1 = int((c + 1) * TERRAIN_WIDTH)

            if c1 <= img_width:
                imgs = part_image(image.crop(origin2box(
                    c*TERRAIN_WIDTH, r*TERRAIN_HEIGHT,
                    TERRAIN_WIDTH, TERRAIN_HEIGHT
                )))
                all_imgs.extend(imgs)
                print("Terrain: ({0}, {1}, {2}, {3})".format(
                    c * TERRAIN_WIDTH, r*TERRAIN_HEIGHT,
                    TERRAIN_WIDTH, TERRAIN_HEIGHT
                ))
                print("Limit: ({0}, {1})".format(
                    c1, r1
                ))
                c += 1
            else:
                keep_w = False

        r += 1

    rows, cols = calculate_rows_cols(all_imgs)
    result_img = spritesheet(rows, cols, all_imgs)
    if result_img is not None:
        result_img.save(out_img_path)
    print("Done!")



    

