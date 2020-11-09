from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps

ELEMENTS = ['fire', 'water', 'wood', 'light', 'dark']
INPUT_FILE_PATTERN = 'originals/{}.png'
OUTPUT_FILE_PATTERN = 'combined/{}_{}.png'

DIM = 76


def crop_image(img: Image, polygon):
    """
    Source: https://stackoverflow.com/questions/35620201/python-pil-make-pixels-outside-a-polygon-transparent
    :param img: PIL image object
    :param polygon: List of tuples
    :return:
    """
    back = Image.new('RGBA', img.size)
    back.paste(img)
    poly = Image.new('L', (512, 512))
    pdraw = ImageDraw.Draw(poly)
    pdraw.polygon(polygon, fill=255)
    inverted_poly = ImageOps.invert(poly)
    back.paste(poly, (0, 0), mask=inverted_poly)
    back.show()
    return back


def run():
    for elem in ELEMENTS:
        upper_image = Image.open(INPUT_FILE_PATTERN.format(elem)).resize((DIM, DIM))

        upper_polygon = [(0, 0), (0, DIM), (DIM, 0), (0, 0)]
        upper_triangle = crop_image(upper_image, upper_polygon)

        for elem2 in ELEMENTS:
            if elem2 == elem:
                continue
            lower_image = Image.open(INPUT_FILE_PATTERN.format(elem2)).resize((DIM, DIM))

            lower_polygon = [(DIM, DIM), (DIM, 0), (0, DIM), (DIM, DIM)]
            lower_triangle = crop_image(lower_image, lower_polygon)

            upper_triangle.paste(lower_triangle, (0, 0), lower_triangle)
            upper_triangle.save(OUTPUT_FILE_PATTERN.format(elem, elem2))


if __name__ == '__main__':
    run()
