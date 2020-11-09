import numpy
from PIL import Image
from PIL import ImageDraw

ELEMENTS = ['fire', 'water', 'wood', 'light', 'dark']
INPUT_FILE_PATTERN = 'originals/{}.png'
OUTPUT_FILE_PATTERN = 'combined/{}_{}.png'

DIM = 76


def crop_image(image: Image, polygon):
    """
    Source: https://stackoverflow.com/questions/22588074/polygon-crop-clip-using-python-pil
    :param image: PIL image object
    :param path: List of tuples
    :return:
    """

    # convert to numpy (for convenience)
    imArray = numpy.asarray(image.convert("RGBA"))

    # create mask
    maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
    mask = numpy.array(maskIm)

    # assemble new image (uint8: 0-255)
    newImArray = numpy.empty(imArray.shape, dtype='uint8')

    # colors (three first columns, RGB)
    newImArray[:, :, :3] = imArray[:, :, :3]

    # transparency (4th column)
    newImArray[:, :, 3] = mask * 255

    # back to Image from numpy
    newIm = Image.fromarray(newImArray, "RGBA")
    return newIm


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
