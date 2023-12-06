<h1 align="center">strcolred</h1>


## Install

```sh
pip install strcolred
```


# FEATURES IN THE DOC

  - Colorate text ✔️
  - Colorate text with fade effect ✔️
  - Writing effects ✔️
  - Centered Text ✔️
  - Adding banners ✔️
  - Make boxes ✔️
 

<br>

## Colorate text
```python
from strcolred import Colors, Colorate
text = "Hello world!"
print(Colors.blue + text)
# or
print(Colorate.Color(Colors.blue, text, True))
```

<br>

`Colors.blue` = color<br>
`text` = text to be colored<br>
`True` = end the coloring after (otherwise it will continue printing characters in the specified color)

<br>

Available functions are:
  - Color (simply colorate a text)
  - Error (make an error effect easily)


<br>



```python
from strcolred import Colors, Colorate
print(Colorate.Horizontal(Colors.yellow_to_red, "Hello World.", 1))
```

<br>

`Colors.yellow_to_red` = color<br>
`Colorate.Vertical` = mode<br>
`1` = intensity (default=1)

<br>

Available effects are:
  - Vertical
  - Horizontal
  - Diagonal
  - DiagonalBackwards

<br>

## Writing text with fade effect

<br>

To print a text with a writing and fade effect you can use the `strcolred.Write` function.

```python
from strcolred import Write, Colors

name = Write.Input("Enter your name -> ", Colors.red_to_purple, interval=0.0025)
Write.Print(f"Nice to meet you, {name}!", Colors.blue_to_green, interval=0.05)
```
<br>


There are 2 functions:<br>


`Write.Print`: prints the text to the terminal with chosen effects<br>
`Write.Input`: same than `Write.Print` but adds an input at the end<br>


<br>


There are 6 arguments:<br>


`text`: the text to be written to the terminal<br>
`color`: the color you want for the text<br>
`interval`: the interval of the writing effect<br>
`hide_cursor`: whether you want the cursor to be hidden or not<br>
`end`: the end color, the default is white<br>
`input_color` (only for `Write.Input`): the color of the input<br>


<br>
<br>
```python
from strcolred import Center
print(Center.XCenter("Hello, Welcome to strcolred."))
```
<br>
<p>Output:</p>
<br>

```
                                            Hello, Welcome to strcolred.                                
```


<br>

Available modes are:
  - Center (Center the banner/text on both axis)
  - XCenter (Center the banner/text on X axis)
  - YCenter (Center the banner/text on Y axis)

<br><br>

```python
from strcolred import Box
print(Box.Lines("Hello, Welcome to strcolred."))
print(Box.DoubleCube("Hello, Welcome to strcolred."))
```

Output:

```
─══════════════════════════☆☆══════════════════════════─
               Hello, Welcome to strcolred.
─══════════════════════════☆☆══════════════════════════─
╔════════════════════════════╗
║ Hello, Welcome to strcolred. ║
╚════════════════════════════╝
```

Available modes are:
  - Lines
  - SimpleCube
  - DoubleCube

<br>
<br>

## 👤 Author

👤 GitHub: [@**johnlesure**](https://github.com/johnlesure)<br>
***
