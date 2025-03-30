import plotly.figure_factory as ff
import numpy as np

data = np.random.randint(0, 100, (100, 100)).tolist()

fig = ff.create_table(data, colorscale='Blues')
fig.show()