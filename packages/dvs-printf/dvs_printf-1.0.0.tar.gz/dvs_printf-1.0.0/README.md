
#### simple pritning animetion styles for python Project

<br>

# Installation 
***
copy and past oneliner command on Terminal


### **Linux / macOS**
```bash
pip3 install dvs_printf 
```

```bash
python3 -m pip install dvs_printf
```

### **Windows**

```bash
pip install dvs_printf

python -m pip install dvs_printf
```
<br>

# Documentation
***

## dvs_printf 
This function makes your python project looks good,
by using printf's styl animetion function you can print you stream in uniq styles 

#### printf function keywords
``` python
from dvs_printf import printf

printf(*values, styl='typing', speed=3, intervel=2, stay=True)
```


## values
values stream can be anythin like
`(string, int, float, list, set, tuple, dict)`
and you can give multiple input as any-data-type

```  python              
printf(str, list, [tuple, set], dict, int,...) 
```     


## styl
styl is different types of print animetion
each style type works differently according to description below

``` python
 ["typing", "headline", "mid", "f2b", "b2f", "gunshort", 
  "sniper", "metrix", "metrix2", "firing", "help"]
``` 

|  option  |                 description                |
| -------- | -------------------------------------------|
| typing   | print like typing                          |
| headline | print head lines in news                   |
| mid      | print line from mid                        |
| f2b      | remove word from (back to front)           |
| b2f      | remove word from (front to back)           |
| gunshort | firing the words from short gun            |
| sniper   | sniping the words from end of the terminal |
| metrix   | print random words to real line            |
| metrix2  | print 1st word and 2nd random word         |
| firing   | just look like firing (Just For Fun)       |


## speed
Speed is printf's animetion speed, `defult speed is 3`
you can set `speed from ( 1 to 6 )`
```
1 = Very Slow
2 = Slow
3 = Mediam
4 = Mediam Fast
5 = Fast
6 = Very Fast
```

``` python
printf("hello world", speed=2)
```


## intervel
intervel is waiting time between printing 
of two lines (intervel in second)
`defult intervel is 2`, 
you can set intervel from `0 to 10 or greater` 

``` python
printf("hello world", "hii I am coder", intervel=2)

>>> hello world
(Then wating time of intervel time in second)
>>> hii I am coder
```


## stay
stay decides after styl animetion whether you want the `stream OR Not`. 
stay can be True or False, `(defult stay = False)`.
some type of styl removes printed stream after intervel 
time. so if you don't want to remove printed streame 
you can set `stay == True`, so printed line stay as it is.

but some styles `take No action on stay`,
whether it is `True OR False`.

Ex. `( typing, f2b, b2f, metrix, metrix2 )`


```python
printf("hello world", styl="headline", stay=True)
```
