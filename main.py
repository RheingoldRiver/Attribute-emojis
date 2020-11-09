from PIL import Image
from PIL import ImageDraw

ELEMENTS = ['fire', 'water', 'wood', 'light', 'dark', 'nil']
INPUT_FILE_PATTERN = 'originals/{}.png'
OUTPUT_FILE_PATTERN = 'combined/{}_{}.png'

DIM = 76


def make_polygon(path):
    """
    :param path:
    :return: a mask to use to make the thing transparent
    """
    poly = Image.new('RGBA', (DIM, DIM))
    pdraw = ImageDraw.Draw(poly)
    pdraw.polygon(path, fill=(255, 255, 255, 255), outline=(255, 255, 255, 255))
    return poly


def run():
    for elem in ELEMENTS:
        upper_image = Image.open(INPUT_FILE_PATTERN.format(elem)).resize((DIM, DIM))

        upper_path = [(0, 0), (0, DIM), (DIM, 0), (0, 0)]
        upper_triangle = make_polygon(upper_path)

        for elem2 in ELEMENTS:
            if elem2 == elem:
                continue
            lower_image = Image.open(INPUT_FILE_PATTERN.format(elem2)).resize((DIM, DIM))

            lower_path = [(DIM, DIM), (DIM, 0), (0, DIM), (DIM, DIM)]
            lower_triangle = make_polygon(lower_path)

            new = Image.new('RGBA', (DIM, DIM))
            new.paste(upper_image, (0, 0), mask=upper_triangle)
            new.paste(lower_image, (0, 0), mask=lower_triangle)
            new.save(OUTPUT_FILE_PATTERN.format(elem, elem2))


if __name__ == '__main__':
    run()
