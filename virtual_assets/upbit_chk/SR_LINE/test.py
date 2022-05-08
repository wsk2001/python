import numpy as np
import pandas as pd
from support_resistance_line import SupportResistanceLine


# Generate a random series
sr = pd.Series(np.random.random(size=250))
# ... moving avg to make it more trending
sr = sr.rolling(50).mean().dropna()

# Init. Index will be ignored
srl = SupportResistanceLine(sr, kind='support')

# Plot the best 3 support lines
srl.plot_top_lines()

# Plot the best 3 resistance lines
srl.twin.plot_top_lines()

# Plot the best support & resistance lines
srl.plot_both()

# View the logic steps if you want
srl.plot_steps()
