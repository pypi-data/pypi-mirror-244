from PIL import Image, ImageDraw
from typing import Dict

from packg.maths import clip_rectangle_coords


def create_bbox_images(
    bx:int,
    by:int,
    bw:int,
    bh:int,
    w:int,
    h:int,
    box_color=(0, 0, 255, 255),
    bbox_width: int = 5,
    mask_opacity: int = 64,
) -> Dict[str, Image.Image]:
    """
    Create box overlay images, originally used in the OVAD visualizer e.g.:
    https://lmb.informatik.uni-freiburg.de/resources/datasets/ovad/?imgnum=14#top

    This function creates transparent PNGs that can be overlayed on top of an image to show or
    highlight a bounding box.
    """
    # create one image with transparent background and one with half transparent
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    img2 = Image.new("RGBA", (w, h), (0, 0, 0, mask_opacity))
    draw2 = ImageDraw.Draw(img2)

    # boxes should be approximately the same width after scaling the image
    # so we have to scale the box thickness now
    target_w = 800
    rel_w = w / target_w  # if small image, create smaller boxes
    rel_bbox_width = round(bbox_width * rel_w)

    # the inside of the thick drawn box will be the true bbox
    # this means that the box can clip outside the image and become almost invisible
    # to avoid that, we move the edges of the box outwards and then clip them
    x1 = bx - rel_bbox_width
    y1 = by - rel_bbox_width
    x2 = bx + bw + rel_bbox_width
    y2 = by + bh + rel_bbox_width
    (x1, y1, x2, y2) = clip_rectangle_coords((x1, y1, x2, y2), w, h)

    for bbox_step in range(rel_bbox_width):
        rectangle_coords = (
            x1 + bbox_step,
            y1 + bbox_step,
            x2 - bbox_step,
            y2 - bbox_step,
        )
        # a 2nd clip should now not be necessary anymore and we assert instead
        assert (
            rectangle_coords[0] >= 0
            and rectangle_coords[1] >= 0
            and rectangle_coords[2] <= w
            and rectangle_coords[3] <= h
        ), f"{rectangle_coords} outside {w}x{h}"

        draw.rectangle(rectangle_coords, fill=(0, 0, 0, 0), outline=box_color)
        draw2.rectangle(rectangle_coords, fill=(0, 0, 0, 0), outline=box_color)

    return {"box": img, "box-mask": img2}
