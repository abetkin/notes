
#%%
import re
reg = r'X(-?[\d.]+) Z(-?[\d.]+)'
li = list(re.finditer(reg, 'X3 Z4'))
li[0]

#%%
type(li[0][0])
