import js
import pyodide

script = '''
(size, frame) => {
    const canvas = document.createElement('canvas');
    canvas.id = 'canvas';
    canvas.tabindex = 1;
    canvas.width = size[0];
    canvas.height = size[1];
    document.body.appendChild(canvas);

    const gl = canvas.getContext('webgl2', {
        powerPreference: 'high-performance',
        premultipliedAlpha: false,
        antialias: false,
        alpha: false,
        depth: false,
        stencil: false,
    });

    const state = {
        canvas,
        gl,
        frame_time: 0.0,
        prev_mouse: [0, 0],
        mouse: [0, 0],
        prev_keys: new Set(),
        keys: new Set(),
    };

    const mouseKeys = ['mouse1', 'mouse3', 'mouse2', 'mouse4', 'mouse5'];

    window.addEventListener('keydown', (evt) => {
        state.keys.add(evt.key);
    });

    window.addEventListener('keyup', (evt) => {
        state.keys.delete(evt.key);
    });

    window.addEventListener('mousedown', (evt) => {
        state.keys.add(mouseKeys[evt.button]);
    });

    window.addEventListener('mouseup', (evt) => {
        state.keys.delete(mouseKeys[evt.button]);
    });

    window.addEventListener('mousemove', (evt) => {
        const rect = canvas.getBoundingClientRect();
        state.mouse[0] = evt.clientX - rect.left;
        state.mouse[1] = evt.clientY - rect.top;
    });

    let last_timestamp = null;
    const animate = (timestamp) => {
        if (last_timestamp === null) {
            last_timestamp = timestamp;
        }
        state.frame_time = (timestamp - last_timestamp) / 1000.0;
        frame();
        state.prev_mouse[0] = state.mouse[0];
        state.prev_mouse[1] = state.mouse[1];
        state.prev_keys = new Set(state.keys);
        requestAnimationFrame(animate);
    };

    requestAnimationFrame(animate);
    return state;
}
'''


class WebWindow:
    def __init__(self, size):
        self.size = size
        callback = js.window.eval(script)

        def frame():
            if self.render:
                self.render()

        self.state = callback(size, pyodide.ffi.create_proxy(frame))
        self.canvas = self.state.canvas
        self.gl = self.state.gl

    @property
    def frame_time(self):
        return tuple(self.state.frame_time)

    @property
    def mouse(self):
        return tuple(self.state.mouse)

    @property
    def mouse_delta(self):
        return (self.state.mouse[0] - self.state.prev_mouse[0], self.state.mouse[1] - self.state.prev_mouse[1])

    def key_down(self, key):
        return self.state.keys.has(key)

    def key_pressed(self, key):
        return self.state.keys.has(key) and not self.state.prev_keys.has(key)

    def key_released(self, key):
        return not self.state.keys.has(key) and self.state.prev_keys.has(key)

    def on_render(self, render):
        self.render = render
