import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Huckleberry_latest.csv')

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*5, color='r', linestyle='-')
plt.show()
