"""Hatch demo code from https://matplotlib.org/3.1.1/gallery/shapes_and_collections/hatch_demo.html.

Slightly modified to test more aspects of the hatch implementation.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse, Polygon

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig, (ax1, ax2, ax3) = plt.subplots(3)

    ax1.bar(range(1, 5), range(1, 5), color="red", edgecolor="black", hatch="/")
    ax1.bar(
        range(1, 5),
        [6] * 4,
        bottom=range(1, 5),
        color="blue",
        edgecolor="black",
        hatch="/",
    )
    ax1.set_xticks([1.5, 2.5, 3.5, 4.5])

    bars = ax2.bar(range(1, 5), range(1, 5), color="yellow", edgecolor="black") + ax2.bar(
        range(1, 5), [6] * 4, bottom=range(1, 5), color="green"
    )
    ax2.set_xticks([1.5, 2.5, 3.5, 4.5])

    patterns = ("-", "+", "x", "\\", "*", "o", "O", ".")
    for bar, pattern in zip(bars, patterns):
        bar.set_hatch(pattern)

    ax3.fill([1, 3, 3, 1], [1, 1, 2, 2], fill=False, hatch="\\", zorder=1, label="Square")
    ax3.add_patch(Ellipse((4, 1.5), 4, 0.5, fill="green", hatch="*", zorder=3, label="Ellipse"))
    p = Polygon(
        np.array([[0, 0], [4, 1.1], [6, 2.5], [2, 1.4]]),
        closed=True,
        fill=False,
        hatch="/",
        zorder=2,
        label="Polygon",
    )
    p._hatch_color = (0.5, 0.3, 0.8, 0.7)  # type: ignore[attr-defined]  # noqa: SLF001
    ax3.add_patch(p)
    ax3.set_xlim((0, 6))
    ax3.set_ylim((0, 2.5))
    ax3.legend(loc="upper right")

    return fig


def test() -> None:
    with pytest.warns(
        UserWarning,
        match=r"matplot2tikz: The hatches \['o', 'O'\] do not have good PGF counterparts.",
    ):
        assert_equality(plot, "test_hatch_reference.tex")
