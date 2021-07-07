from engine.game_object import GameObject
from enum import Enum
from engine.rendering.standard_renderers import PlaneRenderer, TextRenderer
import numpy as np
import pyrr

class Camera(GameObject):
    def __init__(self):
        super().__init__()
        self.perspective = pyrr.matrix44.create_perspective_projection(
            45,
            1,
            0.5,
            500,
        )
class Plane(GameObject):
    def __init__(self, color = [1, 0, 0]):
        super().__init__()
        renderer = PlaneRenderer(color)
        self.add_renderer(renderer)

class Cube(GameObject):
    def __init__(self):
        super().__init__()
        for i in range(3):
            ui = np.zeros(3)
            ui[i] = 1
            for j in [-1, 1]:
                p = Plane(color = ui)
                p.transform.rotate(ui[0]*3.14/2, ui[1]*3.14/2, ui[2]*3.14/2)
                if i == 2:
                    p.transform.translate(j*ui[0]/2, j*ui[1]/2, j*ui[2]/2)
                else:
                    p.transform.translate(j*ui[1]/2, j*ui[0]/2, j*ui[2]/2)
                p.set_parent(self)

class TextObject(GameObject):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.add_renderer(TextRenderer(text,-0.5, -0.5, 1, 1))

    def update_text(self, text):
        self.text = text
        self.renderers[0].update_text(text)

class Button(GameObject):
    IS_CLICKED = False
    def __init__(self, callback, height, width, text = None, color = [1, 0, 0]):
        super().__init__()
        self.callback = callback
        self.height, self.width = height, width
        self.add_renderer(PlaneRenderer(color))
        self.transform.scale(width, height, 1)
        self.text = text
        if text is not None:
            t = TextObject(text)
            t.set_parent(self)
            t.transform.translate(0, 0, 0.01)
            t.transform.scale(0.75, 0.75, 1)
            self.text_obj = t

    def update(self):
        Button.IS_CLICKED = False
    
    def mouse_callback(self, button, state, x, y, camera):
        if state == 0:
            if not Button.IS_CLICKED:
                if self.renderers[0].is_clicked(x, y, camera):
                    self.callback(self)
                    Button.IS_CLICKED = True
    
    def update_text(self, text):
        self.text = text
        self.text_obj.update_text(text)

class ButtonLayout(Enum):
    HORIZONTAL=0
    VERTICAL=1


class ButtonPanel(GameObject):
    def __init__(self, height, width, callbacks=[], texts = None, colors = None, layout=ButtonLayout.HORIZONTAL):
        super().__init__()
        self.button_map = {}
        self.transform.scale(height, width, 1)
        self.width = width
        self.height = height
        self.layout = layout
        if texts is None:
            texts = [None for _ in callbacks]
        if colors is None:
            colors = [[1,0,0] for _ in callbacks]
        for i, cb in enumerate(callbacks):
            button = Button(cb, height, width, texts[i], colors[i])
            button.set_parent(self)
            self.button_map[str(button)] = button
        self.set_button_transforms()

    def set_button_transforms(self):
        if len(self.button_map) == 0:
            return
        if self.layout == ButtonLayout.HORIZONTAL:
            button_width = self.width/len(self.button_map)
            for i, (_, button) in enumerate(self.button_map.items()):
                button.transform.reset()
                button.transform.scale(button_width, 1, 1)
                button.transform.translate(((2*(i+1))-1)*(button_width/2) - 0.5, 0, 0)
        else:
            button_width = self.height/len(self.button_map)
            for i, (_, button) in enumerate(self.button_map.items()):
                button.transform.reset()
                button.transform.scale(1,button_width, 1)
                button.transform.translate(0, 0.5-((2*(i+1))-1)*(button_width/2), 0)

    def add_button(self, button):
        button.set_parent(self)
        self.button_map[str(button)] = button
        self.set_button_transforms()

    def remove_button(self, button):
        if str(button) not in self.button_map:
            return
        self.button_map[str(button)].remove_parent()
        del self.button_map[str(button)]
        self.set_button_transforms()

    @property
    def n_buttons(self):
        return len(self.button_map)

class TextInputField(GameObject):
    FOCUSED_OBJECT = None
    def __init__(self, default_text, height, width, enter_callback, color=[1,0,0]):
        super().__init__()
        self.text = default_text
        self.default_text = default_text
        self.button = Button(self.take_focus, height, width, text=default_text, color=color)
        self.button.set_parent(self)
        self.is_focused = False
        self.is_changed = False
        self.enter_callback = enter_callback

    def take_focus(self, button):
        self.is_focused = True
        TextInputField.FOCUSED_OBJECT = self

    def update(self):
        if TextInputField.FOCUSED_OBJECT != self:
            self.is_focused = False
    
    def keyboard_callback(self, key):
        if not self.is_focused:
            return
        if key == b'\x08':
            self.remove_letter()
        elif key==b'\r':
            self.enter_callback(self.text)
        else:
            key_str = key.decode()
            self.add_letter(key_str)

    def remove_letter(self):
        self.text = self.text[:-1]
        self.button.update_text(self.text)

    def add_letter(self, letter):
        if not self.is_changed:
            self.text = letter
            self.is_changed = True
        else:
            self.text += letter
        self.button.update_text(self.text)
