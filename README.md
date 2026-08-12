# Python for CQSFA

- Plotting algorithms
- ML learning tools
- Unit tests for modules

## Setup

```
pip install -r requirements.txt
```

## Tests

Run the full test suite with pytest from the repository root:

```
pytest
```

## Examples

`notebooks/examples.ipynb` consolidates the example scripts (clustering, trajectory
plotting, regression, IRIS, MNIST, ARC asymmetry, contour plotting) and calls the
underlying helper classes in `Source/` and `MLexamples/`. Some examples require
data files that aren't included in this repository — see the notes in each section.
