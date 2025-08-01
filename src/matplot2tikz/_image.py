import matplotlib.pyplot as plt
import numpy as np
import PIL
from matplotlib.image import AxesImage

from . import _files
from ._tikzdata import TikzData


def draw_image(data: TikzData, obj: AxesImage) -> list[str]:
    """Returns the PGFPlots code for an image environment."""
    content = []

    filepath, rel_filepath = _files.new_filepath(data, "img", ".png")

    # store the image as in a file
    img_array = obj.get_array()
    if img_array is None:
        msg = "No data in image?"
        raise ValueError(msg)

    dims = img_array.shape
    if len(dims) == 2:  # noqa: PLR2004
        # the values are given as one real number: look at cmap
        clims = obj.get_clim()
        plt.imsave(
            fname=filepath,
            arr=img_array,
            cmap=obj.get_cmap(),
            vmin=clims[0],
            vmax=clims[1],
            origin=obj.origin,
        )
    else:
        # RGB (+alpha) information at each point
        if not (len(dims) == 3 and dims[2] in [3, 4]):  # noqa: PLR2004
            msg = (
                "Image array should be three dimensional, with third dimension 3 (RGB) or "
                "4 (RGB+alpha) entries."
            )
            raise ValueError(msg)
        # convert to PIL image
        if obj.origin == "lower":
            img_array = np.flipud(img_array)

        # Convert mpl image to PIL
        if img_array.dtype != np.uint8:
            img_uint8 = np.uint8(img_array * 255)
        image = PIL.Image.fromarray(img_uint8)

        image.save(filepath, origin=obj.origin)

    # write the corresponding information to the TikZ file
    extent = obj.get_extent()

    # the format specification will only accept tuples
    if not isinstance(extent, tuple):
        extent = tuple(extent)

    # Explicitly use \pgfimage as includegrapics command, as the default
    # \includegraphics fails unexpectedly in some cases
    ff = data.float_format
    # Always use slash in file paths, see
    # <https://tex.stackexchange.com/a/18923/13262>
    # <https://github.com/nschloe/tikzplotlib/issues/509>
    posix_filepath = rel_filepath.as_posix()
    content.append(
        "\\addplot graphics [includegraphics cmd=\\pgfimage,"
        f"xmin={extent[0]:{ff}}, xmax={extent[1]:{ff}}, "
        f"ymin={extent[2]:{ff}}, ymax={extent[3]:{ff}}] {{{posix_filepath}}};\n"
    )
    return content
