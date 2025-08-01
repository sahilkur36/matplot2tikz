"""Multiple tests for testing _cleanfigure's functionality."""

import matplotlib as mpl
import numpy as np
import pytest
from matplotlib import colors as mcolors
from matplotlib import pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.ticker import FormatStrFormatter, LinearLocator
from mpl_toolkits.mplot3d import axes3d

from matplot2tikz import clean_figure, get_tikz_code

mpl.use("Agg")

RC_PARAMS = {"figure.figsize": [5, 5], "figure.dpi": 220, "pgf.rcfonts": False}


class TestPlottypes:
    """Testing plot types found at matplotlib's manual.

    Link: https://matplotlib.org/3.1.1/tutorials/introductory/sample_plots.html
    """

    def test_plot(self) -> None:
        """Tets cleanfigure with a plot."""
        line_difference = 18
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y)
            ax.set_ylim(20, 80)
            ax.set_xlim(20, 80)
            raw = get_tikz_code()

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_step(self) -> None:
        """Test if clean_figure runs (with warning)."""
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.step(x, y)
            ax.set_ylim(20, 80)
            ax.set_xlim(20, 80)
            with pytest.warns(Warning, match="step plot simplification not yet implemented."):
                clean_figure(fig)
        plt.close("all")

    def test_scatter(self) -> None:
        """Test cleanfigure with a simple scatter plot."""
        line_difference = 6
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)
        with plt.rc_context(rc=RC_PARAMS):
            _, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.scatter(x, y)
            ax.set_ylim(20, 80)
            ax.set_xlim(20, 80)
            raw = get_tikz_code()

            clean_figure()
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_bar(self) -> None:
        """Test if clean_figure runs (with warning)."""
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)
        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.bar(x, y)
            ax.set_ylim(20, 80)
            ax.set_xlim(20, 80)
            with pytest.warns(
                Warning, match=r"Cleaning Bar Container \(bar plot\) is not supported yet."
            ):
                clean_figure(fig)
        plt.close("all")

    def test_hist(self) -> None:
        """Test if clean_figure runs (with warning)."""
        x = np.linspace(1, 100, 20)
        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.hist(x)
            ax.set_ylim(20, 80)
            ax.set_xlim(20, 80)
            with pytest.warns(
                Warning, match=r"Cleaning Bar Container \(bar plot\) is not supported yet."
            ):
                clean_figure(fig)
        plt.close("all")

    def test_plot3d(self) -> None:
        """Test cleanfigure with a 3d plot."""
        line_difference = 13
        theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
        z = np.linspace(-2, 2, 100)
        r = z**2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax: axes3d.Axes3D = fig.add_subplot(111, projection="3d")
            ax.plot(x, y, z)
            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            ax.set_zlim(-2, 2)
            ax.view_init(30, 30)
            raw = get_tikz_code(fig)

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_scatter3d(self) -> None:
        """Test cleanfigure with scatter plot."""
        line_difference = 14
        theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
        z = np.linspace(-2, 2, 100)
        r = z**2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax: axes3d.Axes3D = fig.add_subplot(111, projection="3d")
            ax.scatter(x, y, z)
            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            ax.set_zlim(-2, 2)
            ax.view_init(30, 30)
            raw = get_tikz_code(fig)

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")

            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_wireframe3d(self) -> None:
        """Test if clean_figure runs (with warning)."""
        # Grab some test data.
        x, y, z = axes3d.get_test_data(0.05)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax: axes3d.Axes3D = fig.add_subplot(111, projection="3d")

            # Plot a basic wireframe.
            ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
            with pytest.warns(
                Warning, match=r"Cleaning Line Collections \(scatter plot\) is not supported yet."
            ):
                clean_figure(fig)
        plt.close("all")

    def test_surface3d(self) -> None:
        """Test if clean_figure runs (with warning)."""
        # Make data.
        x = np.arange(-5, 5, 0.25)
        y = np.arange(-5, 5, 0.25)
        xx, yy = np.meshgrid(x, y)
        r = np.sqrt(xx**2 + yy**2)
        z = np.sin(r)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax: axes3d.Axes3D = plt.axes(projection="3d")

            # Plot the surface.
            surf = ax.plot_surface(
                xx, yy, z, cmap=plt.get_cmap("coolwarm"), linewidth=0, antialiased=False
            )

            # Customize the z axis.
            ax.set_zlim(-1.01, 1.01)
            ax.zaxis.set_major_locator(LinearLocator(10))
            ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))

            # Add a color bar which maps values to colors.
            fig.colorbar(surf, shrink=0.5, aspect=5)

            with pytest.warns(UserWarning) as record:  # noqa: PT030  (we check later for specific warnings)
                clean_figure(fig)

            warnings = (
                "Cleaning Poly3DCollections is not supported yet.",
                "Cleaning Line Collections (scatter plot) is not supported yet.",
            )
            assert len(record) == len(warnings)
            for record_warning, warning in zip(record, warnings):
                assert str(record_warning.message) == warning

        plt.close("all")

    def test_trisurface3d(self) -> None:
        """Test if clean_figure runs (with warning)."""
        n_radii = 8
        n_angles = 36
        # Make radii and angles spaces (radius r=0 omitted to eliminate duplication).
        radii = np.linspace(0.125, 1.0, n_radii)
        angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)

        # Repeat all angles for each radius.
        angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)

        # Convert polar (radii, angles) coords to cartesian (x, y) coords.
        # (0, 0) is manually added at this stage,  so there will be no duplicate
        # points in the (x, y) plane.
        x = np.append(0, (radii * np.cos(angles)).flatten())
        y = np.append(0, (radii * np.sin(angles)).flatten())

        # Compute z to make the pringle surface.
        z = np.sin(-x * y)

        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax: axes3d.Axes3D = plt.axes(projection="3d")

            ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)
            with pytest.warns(Warning, match="Cleaning Poly3DCollections is not supported yet."):
                clean_figure(fig)
        plt.close("all")

    def test_contour3d(self) -> None:
        """Test if clean_figure runs (with warning)."""
        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            x, y, z = axes3d.get_test_data(0.05)
            cset = ax.contour(x, y, z, cmap=plt.get_cmap("coolwarm"))
            ax.clabel(cset, fontsize=9, inline=1)
            with pytest.warns(Warning, match=r"Cleaning QuadContourSet is not supported yet."):
                clean_figure(fig)
        plt.close("all")

    def test_polygon3d(self) -> None:
        """Test if clean_figure runs (with warning)."""
        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax: axes3d.Axes3D = plt.axes(projection="3d")
            rng = np.random.default_rng(42)

            def cc(arg: str) -> tuple[float, float, float, float]:
                return mcolors.to_rgba(arg, alpha=0.6)

            xs = np.arange(0, 10, 0.4)
            verts = []
            zs = [0.0, 1.0, 2.0, 3.0]
            for _ in zs:
                ys = rng.random(size=len(xs))
                ys[0], ys[-1] = 0, 0
                verts.append(list(zip(xs, ys)))

            poly = PolyCollection(verts, facecolors=[cc("r"), cc("g"), cc("b"), cc("y")])
            poly.set_alpha(0.7)
            ax.add_collection3d(poly, zs=zs, zdir="y")

            ax.set_xlabel("X")
            ax.set_xlim3d(0, 10)
            ax.set_ylabel("Y")
            ax.set_ylim3d(-1, 4)
            ax.set_zlabel("Z")
            ax.set_zlim3d(0, 1)
            with pytest.warns(Warning, match="Cleaning Poly3DCollections is not supported yet."):
                clean_figure(fig)
        plt.close("all")

    def test_bar3d(self) -> None:
        """Test if clean_figure runs (with warning)."""
        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax: axes3d.Axes3D = fig.add_subplot(111, projection="3d")

            rng = np.random.default_rng(42)
            for c, z in zip(["r", "g", "b", "y"], [30, 20, 10, 0]):
                xs = np.arange(20)
                ys = rng.random(size=20)

                # You can provide either a single color or an array. To demonstrate this,
                # the first bar of each set will be colored cyan.
                cs = [c] * len(xs)
                cs[0] = "c"
                ax.bar(xs, ys, zs=z, zdir="y", color=cs, alpha=0.8)

            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            with pytest.warns(
                Warning, match=r"Cleaning Bar Container \(bar plot\) is not supported yet."
            ):
                clean_figure(fig)
        plt.close("all")

    def test_quiver3d(self) -> None:
        """Test if clean_figure runs (with warning)."""
        with plt.rc_context(rc=RC_PARAMS):
            fig = plt.figure()
            ax = plt.axes(projection="3d")

            # Make the grid
            x, y, z = np.meshgrid(
                np.arange(-0.8, 1, 0.2),
                np.arange(-0.8, 1, 0.2),
                np.arange(-0.8, 1, 0.8),
            )

            # Make the direction data for the arrows
            u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
            v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
            w = np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z)

            ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)
            with pytest.warns(
                Warning, match=r"Cleaning Line Collections \(scatter plot\) is not supported yet."
            ):
                clean_figure(fig)
        plt.close("all")


class TestLineplotMarkers:
    """Test plots with/without lines/markers."""

    def test_line_no_markers(self) -> None:
        """Test with plot with line but no markers."""
        line_difference = 18
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y, linestyle="-", marker="None")
            ax.set_ylim(20, 80)
            ax.set_xlim(20, 80)
            raw = get_tikz_code()

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_no_line_markers(self) -> None:
        """Test with plot with markers but without line."""
        line_difference = 6
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y, linestyle="None", marker="*")
            ax.set_ylim(20, 80)
            ax.set_xlim(20, 80)
            raw = get_tikz_code()

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_line_markers(self) -> None:
        """Test with plot with line and markers."""
        line_difference = 6
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y, linestyle="-", marker="*")
            ax.set_ylim(20, 80)
            ax.set_xlim(20, 80)
            raw = get_tikz_code()

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_sine(self) -> None:
        """Test plot with sinus function."""
        line_difference = 39
        x = np.linspace(1, 2 * np.pi, 100)
        y = np.sin(8 * x)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y, linestyle="-", marker="*")
            ax.set_xlim(0.5 * np.pi, 1.5 * np.pi)
            ax.set_ylim(-1, 1)
            raw = get_tikz_code()

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")


class TestSubplots:
    """Test with subplot."""

    def test_subplot(self) -> None:
        """Test cleanfigure with a subplot.

        Octave code
        ```octave
            addpath ("../matlab2tikz/src")

            x = linspace(1, 100, 20);
            y1 = linspace(1, 100, 20);

            figure
            subplot(2, 2, 1)
            plot(x, y1, "-")
            subplot(2, 2, 2)
            plot(x, y1, "-")
            subplot(2, 2, 3)
            plot(x, y1, "-")
            subplot(2, 2, 4)
            plot(x, y1, "-")
            xlim([20, 80])
            ylim([20, 80])
            set(gcf,'Units','Inches');
            set(gcf,'Position',[2.5 2.5 5 5])
            cleanfigure;
        ```
        """
        line_difference = 36
        x = np.linspace(1, 100, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, axes = plt.subplots(2, 2, figsize=(5, 5))
            plotstyles = [("-", "o"), ("-", "None"), ("None", "o"), ("--", "x")]
            for ax, style in zip(axes.ravel(), plotstyles):
                ax.plot(x, y, linestyle=style[0], marker=style[1])
                ax.set_ylim([20, 80])
                ax.set_xlim([20, 80])
            raw = get_tikz_code()

            clean_figure(fig)
            clean = get_tikz_code()

            # Use number of lines to test if it worked.
            # the baseline (raw) should have 20 points
            # the clean version (clean) should have 2 points
            # the difference in line numbers should therefore be 2
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")


class TestLogscale:
    """Different tests with at least one axis on log scale."""

    def test_ylog(self) -> None:
        """Test first semilogy plot."""
        line_difference = 98
        x = np.linspace(0, 3, 100)
        y = np.exp(x)

        with plt.rc_context(rc=RC_PARAMS):
            _, ax = plt.subplots(1)
            ax.plot(x, y)
            ax.set_yscale("log")
            raw = get_tikz_code()
            clean_figure()

            clean = get_tikz_code()
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_xlog(self) -> None:
        """Test first semilogx plot."""
        line_difference = 98
        y = np.linspace(0, 3, 100)
        x = np.exp(y)

        with plt.rc_context(rc=RC_PARAMS):
            _, ax = plt.subplots(1)
            ax.plot(x, y)
            ax.set_xscale("log")
            raw = get_tikz_code()
            clean_figure()

            clean = get_tikz_code()
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_loglog(self) -> None:
        """Test first loglog plot."""
        line_difference = 98
        x = np.exp(np.logspace(0.0, 1.5, 100))
        y = np.exp(np.logspace(0.0, 1.5, 100))

        with plt.rc_context(rc=RC_PARAMS):
            _, ax = plt.subplots(1)
            ax.plot(x, y)
            ax.set_xscale("log")
            ax.set_yscale("log")
            raw = get_tikz_code()
            clean_figure()

            clean = get_tikz_code()
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_ylog_2(self) -> None:
        """Test second semilogy plot."""
        line_difference = 51
        x = np.arange(1, 100)
        y = np.arange(1, 100)
        with plt.rc_context(rc=RC_PARAMS):
            _, ax = plt.subplots(1)
            ax.plot(x, y)
            ax.set_yscale("log")
            raw = get_tikz_code()
            clean_figure()

            clean = get_tikz_code()
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_xlog_2(self) -> None:
        """Test second semilogx plot."""
        line_difference = 51
        x = np.arange(1, 100)
        y = np.arange(1, 100)
        with plt.rc_context(rc=RC_PARAMS):
            _, ax = plt.subplots(1)
            ax.plot(x, y)
            ax.set_xscale("log")
            raw = get_tikz_code()
            clean_figure()

            clean = get_tikz_code()
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_loglog_2(self) -> None:
        """Test second loglog plot."""
        line_difference = 97
        x = np.arange(1, 100)
        y = np.arange(1, 100)
        with plt.rc_context(rc=RC_PARAMS):
            _, ax = plt.subplots(1)
            ax.plot(x, y)
            ax.set_xscale("log")
            ax.set_yscale("log")
            raw = get_tikz_code()
            clean_figure()

            clean = get_tikz_code()
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_loglog_3(self) -> None:
        """Test third loglog plot."""
        line_difference = 18
        x = np.logspace(-3, 3, 20)
        y = np.logspace(-3, 3, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y)
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_ylim(10**-2, 10**2)
            ax.set_xlim(10**-2, 10**2)
            raw = get_tikz_code()

            clean_figure(fig)
            clean = get_tikz_code()
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")

    def test_xlog_3(self) -> None:
        """Test third semilogx plot."""
        line_difference = 18
        x = np.logspace(-3, 3, 20)
        y = np.linspace(1, 100, 20)

        with plt.rc_context(rc=RC_PARAMS):
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.plot(x, y)
            ax.set_xscale("log")
            ax.set_xlim(10**-2, 10**2)
            ax.set_ylim(20, 80)
            raw = get_tikz_code()

            clean_figure(fig)
            clean = get_tikz_code()
            num_lines_raw = raw.count("\n")
            num_lines_clean = clean.count("\n")
            assert num_lines_raw - num_lines_clean == line_difference
        plt.close("all")


def test_memory() -> None:
    plt.plot(np.arange(100000))
    clean_figure()
    plt.close("all")
