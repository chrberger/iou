import matplotlib.pyplot as plot
import numpy as np
import sys

baseline = []
with open('psnr-hevc-cq51.csv') as f:
    lines = f.readlines()
    for line in lines:
        baseline.append(float(line))

plot.boxplot(baseline)
plot.show()
