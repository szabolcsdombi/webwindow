import js
import pyodide

__version__ = '1.2.1'

script = '''
(width, height, frame) => {
    const backdrop = document.createElement('div');
    backdrop.style.position = 'fixed';
    backdrop.style.top = '0';
    backdrop.style.left = '0';
    backdrop.style.width = '100vw';
    backdrop.style.height = '100vh';
    backdrop.style.backgroundColor = 'black';
    backdrop.style.display = 'flex';
    backdrop.style.justifyContent = 'center';
    backdrop.style.alignItems = 'center';
    backdrop.style.overflow = 'hidden';
    document.body.appendChild(backdrop);

    const canvas = document.createElement('canvas');
    canvas.id = 'canvas';
    canvas.tabindex = 1;
    canvas.width = width;
    canvas.height = height;
    canvas.style.maxWidth = `${100 * window.devicePixelRatio}vw`;
    canvas.style.maxHeight = `${100 * window.devicePixelRatio}vh`;
    canvas.style.transform = `scale(calc(1 / ${window.devicePixelRatio}))`;
    canvas.style.aspectRatio = `${canvas.width} / ${canvas.height}`;
    backdrop.appendChild(canvas);

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
        frame_time: 0,
        time: 0,
        prev_mouse: [0, 0],
        mouse: [0, 0],
        prev_keys: new Set(),
        keys: new Set(),
    };

    const mouseKeys = ['mouse1', 'mouse3', 'mouse2', 'mouse4', 'mouse5'];
    const keys = {
        Tab: 'tab',
        ArrowLeft: 'left_arrow',
        ArrowRight: 'right_arrow',
        ArrowUp: 'up_arrow',
        ArrowDown: 'down_arrow',
        PageUp: 'page_up',
        PageDown: 'page_down',
        Home: 'home',
        End: 'end',
        Insert: 'insert',
        Delete: 'delete',
        Backspace: 'backspace',
        Space: 'space',
        Enter: 'enter',
        Escape: 'escape',
        Quote: 'apostrophe',
        Comma: 'comma',
        Minus: 'minus',
        Period: 'period',
        Slash: 'slash',
        Semicolon: 'semicolon',
        Equal: 'equal',
        BracketLeft: 'left_bracket',
        Backslash: 'backslash',
        BracketRight: 'right_bracket',
        Backquote: 'grave_accent',
        CapsLock: 'caps_lock',
        ScrollLock: 'scroll_lock',
        NumLock: 'num_lock',
        PrintScreen: 'print_screen',
        Pause: 'pause',
        Numpad0: 'keypad_0',
        Numpad1: 'keypad_1',
        Numpad2: 'keypad_2',
        Numpad3: 'keypad_3',
        Numpad4: 'keypad_4',
        Numpad5: 'keypad_5',
        Numpad6: 'keypad_6',
        Numpad7: 'keypad_7',
        Numpad8: 'keypad_8',
        Numpad9: 'keypad_9',
        NumpadDecimal: 'keypad_decimal',
        NumpadDivide: 'keypad_divide',
        NumpadMultiply: 'keypad_multiply',
        NumpadSubtract: 'keypad_subtract',
        NumpadAdd: 'keypad_add',
        ShiftLeft: 'left_shift',
        ControlLeft: 'left_ctrl',
        AltLeft: 'left_alt',
        MetaLeft: 'left_super',
        ShiftRight: 'right_shift',
        ControlRight: 'right_ctrl',
        AltRight: 'right_alt',
        MetaRight: 'right_super',
        Menu: 'menu',
        Digit0: '0',
        Digit1: '1',
        Digit2: '2',
        Digit3: '3',
        Digit4: '4',
        Digit5: '5',
        Digit6: '6',
        Digit7: '7',
        Digit8: '8',
        Digit9: '9',
        KeyA: 'a',
        KeyB: 'b',
        KeyC: 'c',
        KeyD: 'd',
        KeyE: 'e',
        KeyF: 'f',
        KeyG: 'g',
        KeyH: 'h',
        KeyI: 'i',
        KeyJ: 'j',
        KeyK: 'k',
        KeyL: 'l',
        KeyM: 'm',
        KeyN: 'n',
        KeyO: 'o',
        KeyP: 'p',
        KeyQ: 'q',
        KeyR: 'r',
        KeyS: 's',
        KeyT: 't',
        KeyU: 'u',
        KeyV: 'v',
        KeyW: 'w',
        KeyX: 'x',
        KeyY: 'y',
        KeyZ: 'z',
        F1: 'f1',
        F2: 'f2',
        F3: 'f3',
        F4: 'f4',
        F5: 'f5',
        F6: 'f6',
        F7: 'f7',
        F8: 'f8',
        F9: 'f9',
        F10: 'f10',
        F11: 'f11',
        F12: 'f12',
        F13: 'f13',
        F14: 'f14',
        F15: 'f15',
        F16: 'f16',
        F17: 'f17',
        F18: 'f18',
        F19: 'f19',
        F20: 'f20',
        F21: 'f21',
        F22: 'f22',
        F23: 'f23',
        F24: 'f24',
    };

    window.addEventListener('keydown', (evt) => {
        state.keys.add(keys[evt.code]);
    });

    window.addEventListener('keyup', (evt) => {
        state.keys.delete(keys[evt.code]);
    });

    window.addEventListener('mousedown', (evt) => {
        state.keys.add(mouseKeys[evt.button]);
    });

    window.addEventListener('mouseup', (evt) => {
        state.keys.delete(mouseKeys[evt.button]);
    });

    window.addEventListener('mousemove', (evt) => {
        const rect = canvas.getBoundingClientRect();
        state.mouse[0] = Math.floor((evt.clientX - rect.left) * canvas.width / rect.width);
        state.mouse[1] = Math.floor((evt.clientY - rect.top) * canvas.height / rect.height);
    });

    let last_timestamp = null;
    const animate = (timestamp) => {
        if (last_timestamp === null) {
            last_timestamp = timestamp;
        }
        state.frame_time = (timestamp - last_timestamp) / 1000.0;
        state.time += state.frame_time;
        frame();
        state.prev_mouse[0] = state.mouse[0];
        state.prev_mouse[1] = state.mouse[1];
        state.prev_keys = new Set(state.keys);
        last_timestamp = timestamp;
        requestAnimationFrame(animate);
    };

    requestAnimationFrame(animate);
    return state;
}
'''


class WebWindow:
    def __init__(self, width, height):
        self.size = (width, height)
        self.render = None

        def frame():
            if self.render:
                self.render()

        callback = js.window.eval(script)
        self.state = callback(width, height, pyodide.ffi.create_proxy(frame))
        self.canvas = self.state.canvas
        self.gl = self.state.gl

    @property
    def frame_time(self):
        return self.state.frame_time

    @property
    def time(self):
        return self.state.time

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
