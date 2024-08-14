# WebWindow

WebWindow is a lightweight window implementation for Python,
developed primarily to support the [ZenGL](https://zengl.readthedocs.io/) documentation,
and it can be easily deployed with [Pyodide](https://pyodide.org/) or [PyScript](https://pyscript.com/).

## Examples

See WebWindow in action: [Live Examples](https://pyscript.com/@szabolcsdombi?q=webwindow)

## Usage

Add this line to the **pyscript.toml**

```toml
packages = ["zengl", "webwindow"]
```

```py
from webwindow import WebWindow
import zengl

window = WebWindow(600, 400)
ctx = zengl.context()

@window.on_render
def render():
    ctx.new_frame()
    ctx.end_frame()
```

## License

Licensed under the [MIT License](LICENSE).
