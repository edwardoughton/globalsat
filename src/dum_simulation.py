import numpy as np



MC =100
Interval = 20 # years
# baseline, h0(t)
# h(t:x)
# Noteu+19 dN/dE

for i in range(MC):
    pr100Hist = np.zeros((Interval))
    pr60_100Hist = np.zeros((Interval))


# output
