# Python rendering engine

This project is a lightweight python game engine built on OpenGL.
Originally a learning project, the goal is to give developers (i.e. me) the ability to quickly make visual and interactive applications purely in code


## Main features

* Dynamic generation of python classes (renderers) to control input to shader programs
* An easy-to-use interface to create multiwindowed applications
* A Unity-like approach to GameObjects and Components
* A parent-child system for GameObjects
* Standard Renderers and standard GameObjects to help you get started

## Installation

```
git clone https://github.com/walley892/engine
cd engine/
// possibly inside of a virtual environment if that's your thing
pip3 install -r requirements.txt
pip3 install .
```

## Getting started

Head over to the examples subdirectory for some sample code!

[Gameobjects] (./examples/game_object_example.py)
[Components] (examples/component_example.py)
[Point cloud rendering] (examples/point_cloud_example.py)
[Mesh rendering] (examples/mesh_example.py)
