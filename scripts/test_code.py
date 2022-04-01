path = '/home/makavelli/Documents/GitHub Codes/'

import coverage as cr
import pandas as pd
a = cr.coverage_area(1)
df = pd.DataFrame(a)
df.to_csv(path+'coverage_area.csv')