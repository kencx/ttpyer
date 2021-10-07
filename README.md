# ttpyer
A terminal based typing test written in Python. ttpyer is built with [urwid](http://urwid.org/) and argparse.

ttpyer aims to be minimalist and customizable. It draws inspiration from [monkeytype](https://monkeytype.com/) and [tt](https://github.com/lemnos/tt).

The basic test uses the 1000 most common English words.

> ttpyer is a word in progress and my first project

## Usage
Random word mode with 10 words
```
$ ttpyer
```
Random word mode with 50 words
```
$ ttpyer -n 50
```
Timed mode at 30 seconds
```
$ ttpyer -t 30
```
Quote mode
```
$ ttpyer -q
```

## Todo
- Support for paragraphs (>70 characters)
- Timer, Word accuracy, speed
- Accept input words from files/stdin
- Show wrong characters instead of hiding them.
- Gradient colors, theming
