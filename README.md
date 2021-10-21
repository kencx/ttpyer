# ttpyer
A terminal based typing test written in Python.

Built with [urwid](http://urwid.org/) and inspired from [monkeytype](https://monkeytype.com/) and [tt](https://github.com/lemnos/tt).

ttpyer aims to have a minimalist and customizable interface.

No Windows support at the moment.

> ttpyer is a work in progress and my first project

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

### Todo
- Support for paragraphs (>70 characters)
- On screen timer
- Word accuracy
- Show wrong characters instead of hiding them.
- Accept input words from files/stdin
- Gradient colors, theming
- Config file
