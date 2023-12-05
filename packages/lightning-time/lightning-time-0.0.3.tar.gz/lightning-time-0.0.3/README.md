# Lightning Time

TODO: add description here

Learn more about how Lightning Time works & play with it hands-on: [here](https://blog.purduehackers.com/posts/lightning-time)

## Installation

```sh
pip3 install lightning-time
```

```python
from LightningTime.Lightning import Lightning, Timestring
```

# Usage

## Colors
```python
from LightningTime.Lightning import Lightning, Timestring

# Create a Lightning object
lt = Lightning(Timestring("a~b~c|d"))
```

**By default**, the `Lightning` colors are set to the following:

```
bolt: (dynamic value), 161, 0
zap: 50, (dynamic value), 214
spark: 246, 133, (dynamic value)
```

You can **change** these colors by passing in color arguments to the `Lightning` object:

```python
lt = Lightning(Timestring("a~b~c|d"), bolt_color=(g, b), zap_color=(r, b), spark_color=(r, g))
```
> r, g and b are integers between 0 and 255, inclusive.

For example, to change the color of a `bolt`, use the following:

```python
lt = Lightning(Timestring("a~b~c|d"), bolt_color=(155, 35))
```

You can set the static colors of a `Lightning` object with the `set_static_colors` method:

```python
lt.set_static_colors((g, b), (r, b), (r, g))
```

## Conversions

```python
from datetime import datetime

#convert from datetime to Lightning time

Lightning.to_lightning(datetime.now()) #e~3~3|8

#convert from Lightning time to a time st

Lightning.from_lightning(Lightning.to_lightning(datetime.now()), withseconds=True) # 21:18:06
```

## Color String

```python
from datetime import datetime
Lightning.to_lightning(datetime.now()).color_strings() # ('#e3a100', '#3238d6', '#f68582')
```

## Print without charges

```python
from datetime import datetime
Lightning.to_lightning(datetime.now()).strip_charges() 
# e~3~a
```

## Accessing values

```python
lt = Lightning(Timestring("a~b~c|d"))
lt.timestring.bolts # a
lt.timestring.zaps # b
lt.timestring.sparks # c
lt.timestring.charges # d
```
---

## Contributing

This project is still under development, feel free to contribute by opening a pull request.

