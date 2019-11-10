# texted

> Convert raw text to beautiful pixel data.

This script uses PIL to translate text into images.



## Usage


* See ``texted --help`` for default values


* Text can be read from a pipe

```sh
    printf "some text" | texted - image.png
```


* Image data can be written into a pipe

  * When using a pipe, the output format is `PNG`

```sh
    texted text.txt - > image.png
```


* Fonts can be specified by name or by full path

```sh
    texted text.txt image.png --font 'Helvetica'

    texted text.txt image.png --font  /System/Library/Fonts/Helvetica.ttc
```


* Colors (``-bg``, ``-fg``) may be passed in various forms
  (all lines define a white background, some with alpha)

```sh
    texted text.txt image.png -bg '#ff0'
    texted text.txt image.png -bg '#ff0f'
    texted text.txt image.png -bg '#ffff00'
    texted text.txt image.png -bg '#ffff00ff'
    texted text.txt image.png -bg 'rgb(255,255,0)'
    texted text.txt image.png -bg 'rgb(100%,100%,0%)'
    texted text.txt image.png -bg 'rgba(255,255,0,255)'
    texted text.txt image.png -bg 'hsl(60,100%,50%)'
    texted text.txt image.png -bg 'hsv(60,100%,100%)'
    texted text.txt image.png -bg 'yellow'
```
