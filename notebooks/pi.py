import marimo

__generated_with = "0.19.9"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Marimo showcase: computing $\pi$

    This notebook is for showcasing Marimo notebooks. The requirements for this notebook are: marimo, matplotlib and numpy.
    """)
    return


@app.cell(hide_code=True)
def _():
    # import required packages
    import marimo as mo
    import numpy as np
    from matplotlib import pyplot as plt

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Computing $\pi$ using Monte Carlo

    Monte Carlo methods are a general type of statistical method that uses random numbers to sample from the true distribution. In this case, we will compute $\pi$ by sampling random numbers between 0 and 1 using numpy.

    To compute $\pi$ we can recognize that a circle of radius $r$ has a surface of $\pi r^2$. So that if we can estimate the surface area of a circle, then we can estimate $\pi$. Let us take a unitary circle, which is a circle of radius $r = 1$, and the smallest square that encloses the circle. We can draw this out and find out that the square has sides of $2 \times 2$, with a surface area of 4. Then if we sample from this square, the chance for this sample to be inside the circle (${\rm P}_{\rm circle}$) is the surface of the circle divided by the surface of the square: ${\rm P}_{\rm circle} = \frac{S_{\rm circle}}{S_{\rm square}} = \frac{\pi}{4} \rightarrow \pi = 4 \cdot {\rm P}_{\rm circle}$.

    Thus, we only need to sample from the square, find the fraction inside the circle and multiply by 4!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Below we define some sliders and number boxes so we can define how precisely we want to compute $\pi$. Take care that you don't put the number of samples of number of samples to plot too high, or the calculation might take a long time!

    Every time you adjust the number of samples, $\pi$ will be recalculated.
    """)
    return


@app.cell
def _(mo):
    n_sample = mo.ui.number(1, label="Number of samples")
    show_samples = mo.ui.slider(10, 1000, step=100, label="Maximum number of samples to plot", show_value=True, debounce=True)
    n_sample, show_samples
    return n_sample, show_samples


@app.cell
def _(mo, n_sample, np):
    # The actual sampling of the surface of the square and circle.

    x, y = 2*np.random.rand(n_sample.value)-1, 2*np.random.rand(n_sample.value)-1
    hit_ratio = x**2+y**2 <= 1  # Estimate of P_circle
    pi_measured = hit_ratio.mean()*4  # Estimate of pi
    mo.md(rf"$\pi \approx {pi_measured}$ after {n_sample.value} samples")
    return hit_ratio, x, y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plotting the MC sampling, which will automatically update when we change the number of samples or the number of samples to plot.
    """)
    return


@app.cell
def _(hit_ratio, plot_pi_mc, show_samples, x, y):
    plot_pi_mc(x, y, hit_ratio, show_samples=show_samples)
    return


@app.cell
def _(plt):
    def plot_pi_mc(x, y, hit_ratio, show_samples):
        pi_measured = hit_ratio.mean()*4
        _hit_ratio_plot = hit_ratio[:show_samples.value]
        _x_plot, _y_plot = x[:show_samples.value], y[:show_samples.value]
    
        plt.title(f"$\pi$ = {pi_measured}")
        plt.scatter(_x_plot[_hit_ratio_plot], _y_plot[_hit_ratio_plot], color="green", alpha=0.5)
        plt.scatter(_x_plot[~_hit_ratio_plot], _y_plot[~_hit_ratio_plot], color="red", alpha=0.5)
        _circ = plt.Circle((0,0), 1, color="green", alpha=0.1)
        plt.gca().add_patch(_circ)
        plt.gca().set_aspect(1)
        plt.xlim((-1, 1))
        plt.ylim((-1, 1))
        plt.show()

    return (plot_pi_mc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Computing $\pi$ with smaller squares

    We can also compute the surface of a circle by dividing the square around it into squares. For each of these smaller squares we can then see if the middle of this square lies inside or outside the circle.

    For this method we will only calculate the ratio of surface of the square and circle for the upper right quadrant. Symmetry dictates that we should get the same result.
    """)
    return


@app.cell
def _(mo):
    n_ticks = mo.ui.slider(2, 100, show_value=True)
    mo.md(f"Number of squares in one direction: {n_ticks}")
    return (n_ticks,)


@app.cell
def _(mo, n_ticks, np, plt):
    delta = 1/n_ticks.value  # Size of the side of a smaller square

    # Use numpy to create all middle points of the squares
    x_lin = np.linspace(delta/2, 1-delta/2, n_ticks.value)
    y_lin = np.linspace(delta/2, 1-delta/2, n_ticks.value)
    xx, yy = np.meshgrid(x_lin, y_lin)

    # Find the ones inside the circle and compute the P_circle estimate
    mask_inside = xx*xx+yy*yy <= 1.0
    xx[mask_inside], yy[mask_inside]
    pi_lin_est = np.mean(mask_inside)*4

    # Make the plot
    plt.gca().set_aspect(1)
    plt.title(rf"$\pi \approx {pi_lin_est}$ with {n_ticks.value} ticks")
    plt.scatter(xx[mask_inside], yy[mask_inside], color="green", alpha=0.5, s=1000*delta)
    plt.scatter(xx[~mask_inside], yy[~mask_inside], color="red", alpha=0.5, s=1000*delta)
    plt.show()
    mo.md(f"Number of squares in one direction: {n_ticks}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compute pi with dynamically sided squares

    Some of you may have noticed a glaring inefficiency with the above approach: we are creating smaller and smaller squares in areas that are completely uninteresting. Squares that are close to (0, 0) are always going to be inside the circle while squares close to (1, 1) are going to be outside the circle.

    In the method below we divide the squares into smaller and smaller squares by separating them into three categories: inside, edge and outside. The category "edge" contains squares that have the edge of the circle go through the square.

    Every step we subdivide squares into 4 smaller squares. We only do this for squares that are in the "edge" category, which saves a lot of squares and thus time.

    A nice side effect of computing it this way is that we also get bounds of pi: the surface of the circle is between the surface of the squares inside and the surface of the squares inside + the surface of the squares on the edge.
    """)
    return


@app.cell
def _(np):
    # Functions to compute pi
    def compute_surf(squares):
        "Compute the surface area of all squares in the array."
        return np.sum((squares[3]-squares[1])*(squares[2]-squares[0]))

    def divide_square(square):
        "Divide a square into 4 smaller squares."
        middle_x = (square[2]-square[0])/2 + square[0]
        middle_y = (square[3]-square[1])/2 + square[1]
        lower_left = np.vstack((square[0], square[1], middle_x, middle_y))
        upper_left = np.vstack((square[0], middle_y, middle_x, square[3]))
        lower_right = np.vstack((middle_x, square[1], square[2], middle_y))
        upper_right = np.vstack((middle_x, middle_y, square[2], square[3]))

        return np.hstack((lower_left, upper_left, lower_right, upper_right))

    def generate_pi(cur_level, inside, edge, outside, max_level=5):
        "Compute pi with the multi-level algorithm."
        if cur_level == max_level:
            return (inside, edge, outside)
        new_squares = divide_square(edge)
        cond_inside = new_squares[2]**2 + new_squares[3]**2 <= 1
        cond_outside = new_squares[0]**2 + new_squares[1]**2 >= 1
        cond_edge = ~(cond_inside|cond_outside)
        if inside is None:
            new_inside = new_squares[:, cond_inside]
        else:
            new_inside = np.hstack((inside, new_squares[:, cond_inside]))
        if outside is None:
            new_outside = new_squares[:, cond_outside]
        else:
            new_outside = np.hstack((outside, new_squares[:, cond_outside]))
        new_edge = new_squares[:, cond_edge]

        return generate_pi(cur_level+1, new_inside, new_edge, new_outside, max_level=max_level) 

    return compute_surf, generate_pi


@app.cell
def _(mo):
    max_level=mo.ui.slider(2, 20, label="Maximum detail for the computation", show_value=True)
    return (max_level,)


@app.cell
def _(generate_pi, max_level, np):
    start_square = np.array([[0, 0, 1, 1]]).T
    inside, edge, outside = generate_pi(1, None, start_square, None, max_level=max_level.value)

    return edge, inside, outside


@app.cell
def _(compute_surf, edge, inside, max_level, mo, outside, plt):
    _inside_surf = compute_surf(inside)
    plt.title(f"${_inside_surf*4} \leq \pi \leq {(_inside_surf+compute_surf(edge))*4}$")
    plt.scatter((inside[0]+inside[2])/2, (inside[1]+inside[3])/2, color="green")
    plt.scatter((outside[0]+outside[2])/2, (outside[1]+outside[3])/2, color="red")
    plt.scatter((edge[0]+edge[2])/2, (edge[1]+edge[3])/2, color="orange")
    plt.gca().set_aspect(1)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()
    mo.md(f"{max_level}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise: refine the above algorithm

    You might notice that the bounds are not converging particularly fast. It turns out that squares are not particularly good estimators for circles. One way to improve the convergence might be to subdivide the squares with line. For the lower bound, this can be done relatively easy, since we know that a circle is convex. The upper bound could perhaps be done using a tangential line.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
