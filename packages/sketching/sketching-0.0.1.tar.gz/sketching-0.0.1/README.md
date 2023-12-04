# Sketching.py
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Pypi Badge](https://img.shields.io/pypi/v/sketching)](https://pypi.org/project/sketching/) [![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

Tiny tools for creative coding in Python. Supporting portability across [desktop](https://sketchingpy.org/start.html#local), [web](https://sketchingpy.org/start.html#web), [Jupyter notebooks](https://sketchingpy.org/start.html#notebook), and [static images](https://sketchingpy.org/start.html#static). Serving makers of all kinds from experienced designers and developers to educators and students.

<br>
<br>

## Quickstart
A first sketch in 7 lines of code ([edit and run this first sketch in your browser](https://sketchingpy.org/examples/web/example.html?sketch=hello_static)):

```
import sketching

sketch = sketching.Sketch2D(500, 500)

sketch.clear('#F0F0F0')
sketch.set_fill('#C0C0C0')
sketch.set_stroke('#000000')
sketch.draw_ellipse(250, 250, 20, 20)

sketch.show()
```

A tiny bit of example interactivity in just over 10 lines ([edit and run this little drawing program in your browser](https://sketchingpy.org/examples/web/example.html?sketch=hello_interactive)):

```
import sketching

sketch = sketching.Sketch2D(500, 500)

def draw():
  mouse = sketch.get_mouse()
  
  x = mouse.get_x()
  y = mouse.get_y()
  
  sketch.set_fill('#C0C0C0')
  sketch.set_stroke('#333333')
  sketch.draw_ellipse(x, y, 20, 20)

sketch.on_step(draw)

sketch.clear('#FFFFFF')

sketch.show()

```

<br>
<br>

## Install and use
There’s multiple ways to use Sketching.py with different dependencies for different platforms.

<br>

### Online sketchbook
No installation needed! Just get your browser and start quickly using an online private sketchbook (coming soon but a slimmed down editor is available at https://sketchingpy.org/examples/web/example.html).

<br>

### Plain Python
Write Python scripts like you usually do and run them from the command line or your IDE. Just grab a few minimal dependencies:

```
$ pip install sketching pillow
```

For interactive sketches, also install pygame:

```
$ pip install pygame
```

Learn more about [using sketches inside standard Python programs](https://sketchingpy.org/start.html#local).

<br>

### Jupyter Notebook
Code creatively in Jupyter notebooks with minimal dependencies:

```
$ pip install sketching matplotlib pillow
```

Go deeper and review the [getting started instructions for Jupyter](https://sketchingpy.org/start.html#notebook).

<br>

### Custom web applications
Embed Sketching.py in your own websites. Simply add this to your [pyscript](https://pyscript.net/) `py-config`:

```
"packages": ["sketching"]
```

Review documentation about [writing sketches for the browser](https://sketchingpy.org/start.html#web).

<br>
<br>

## Learn
More educational resources coming soon. See [examples](https://sketchingpy.org/examples.html) and [reference](https://sketchingpy.org/reference.html) for now.

<br>
<br>

## Deploy
After you’ve made something you want to share, [take your creations to the web](https://sketchingpy.org/deploy.html#web) or export your work to [stand-alone executables](https://sketchingpy.org/deploy.html#desktop).

<br>
<br>

## License
Sketching.py is permissively [BSD licensed](https://gitlab.com/skteching/Sketchingpy/-/blob/main/LICENSE.md?ref_type=heads) meaning you can use it for commerical and non-commerical projects as well as for your hobbies and for your professional work.

<br>
<br>

## Purpose
This interactive coding tool enables anyone to creative code in minutes using Python across multiple platforms including desktop and web.

<br>

### Use cases
We imagine folks using Sketching.py for:

- Interactive science
- Data visualization
- Visual art
- Immersive experience
- Simulation
- Sound design
- User experience (UX) prototyping
- Game development

We would love to see what you do and invite contributions to [our showcase](https://sketchingpy.org/showcase.html).

<br>

### Goals
Specifically, this project seeks to:

- Enable creative expression in computation through Python.
- Be simple to use, friendly for everyone from beginners to experts.
- Support Mac, Windows, Linux, the browser, Jupyter, and static image generation in headless environemnts.
- Work in plain old 100% Python with sketching available as a library, supporting you anywhere in your programming journey.

We hope to reach developers of all skill levels.

<br>

### Audience
We aim to support teachers, students, artists, designers, developers, and other makers as they make creative programs including visual art, games needing a bit more flexibility, and more. Specifically, this project hopes to embrace a wide group of people:

- Serve programmers no matter where they are in their journey from beginner to expert.
- Support portabilty across desktop (Mac, Windows, Linux), web (browser), notebooks (Jupyter), and static image generation.
- Foster inclusive community across different disciplines within and outside computer science.
- Assist in both formal and informal educational contexts.

If you are interested in this mission, we invite a diverse set of collaborators to join us.

<br>

### Scope
Currently we are only focused on 2D with no explicit console support though Steam Deck should work with the Linux builds.

<br>
<br>

## Grow Sketching.py
Thank you for your interest in our humble project. Here is how to participate in our community including growing the code of Sketching.py itself.

<br>

### Get involved
Sketching hopes to foster an inclusive community of makers.

- [Let us know about a bug or other issue](https://sketchingpy.org/community.html#issue).
- [Suggest a new feature](https://sketchingpy.org/community.html#suggest).
- [Contribute to the code of Sketching.py itself](https://sketchingpy.org/community.html#develop).
- [Help with documentation](https://sketchingpy.org/community.html#document).
- [Share your work in our showcase](https://sketchingpy.org/showcase.html#submit).

Also, [join us in our Discord](https://sketchingpy.org/community.html#discord)!

<br>

### Open Source
We use and thank the following open source libraries:

 - [Ace Editor](https://ace.c9.io/) under the [BSD License](https://github.com/ajaxorg/ace/blob/master/LICENSE) for the web editor.
 - [Pillow](https://python-pillow.org/) under the [HPND License](https://github.com/python-pillow/Pillow/blob/main/LICENSE) for `Sketch2D` and `Sketch2DStatic` renderers.
 - [Pygame](https://www.pygame.org/news) under the [LGPL License](https://www.pygame.org/docs/LGPL.txt) for `Sketch2D` renderer.
 - [Pyscript](https://pyscript.net/) under the [Apache v2 License](https://pyscript.github.io/docs/2023.11.2/license/) for the `Sketch2DWeb` renderer.
 - [Pyodide](https://pyodide.org/en/stable/) under the [MPL 2.0 License](https://github.com/pyodide/pyodide/blob/main/LICENSE) for the `Sketch2DWeb` renderer.

Other code and contributors listed in the code itself or within [the people section of the website](https://sketchingpy.org/community.html#people).
