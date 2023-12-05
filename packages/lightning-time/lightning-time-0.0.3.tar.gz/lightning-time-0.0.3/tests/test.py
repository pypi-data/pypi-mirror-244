import datetime
from LightningTime.Lightning import Lightning, Timestring

print(Lightning.from_lightning(Lightning()))
lt = Lightning(Timestring("a~b~c|d"))
print(lt.timestring.bolts)
print(lt.timestring.zaps) # b
print(lt.timestring.sparks) # c
print(lt.timestring.charges) # d