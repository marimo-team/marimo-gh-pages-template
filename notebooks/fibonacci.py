# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
# ]
# ///
import marimo

__generated_with = "0.10.6"
app = marimo.App()

with app.setup:
    import marimo as mo
    
@app.cell
def _():
    mo.md(
        r"""
        # Fibonacci Calculator

        Use the slider above to calculate the first {n.value} numbers in the Fibonacci sequence.
        """
    )
    return


@app.cell
def _():
    # Create an interactive slider
    n = mo.ui.slider(1, 100, value=50, label="Number of Fibonacci numbers")
    n
    return n


@app.cell
def _(n):
    fib = fibonacci(n.value)
    mo.md(", ".join([str(f) for f in fib]))
    
@app.function
def fibonacci(n):
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence
    

if __name__ == "__main__":
    app.run()
