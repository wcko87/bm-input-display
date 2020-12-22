import tkinter as tk
import math
from math import sin, cos
import time
import bmcon
import sys
from win32api import keybd_event
from directinput import PressKey, ReleaseKey

sign = lambda a: (a>0) - (a<0)
TWO_PI = math.pi*2

class KeyBindWin32API(object):
    def __init__(self, key_code):
        self.key_code = key_code
        self.pressed = False
        
    def press(self):
        if self.key_code == None: return
        if self.pressed: return
        keybd_event(self.key_code, 0, 1, 0)
        self.pressed = True
    
    def release(self):
        if self.key_code == None: return
        if not self.pressed: return
        keybd_event(self.key_code, 0, 2, 0)
        self.pressed = False
        

class KeyBindDirectInput(object):
    def __init__(self, key_code):
        self.key_code = key_code
        self.pressed = False
        
    def press(self):
        if self.key_code == None: return
        if self.pressed: return
        PressKey(self.key_code)
        self.pressed = True
    
    def release(self):
        if self.key_code == None: return
        if not self.pressed: return
        ReleaseKey(self.key_code)
        self.pressed = False
        
class KeyRepeater(object):
    def __init__(self, keybind, interval_ticks, firstinput_ticks):
        self.keybind = keybind
        self.interval = interval_ticks
        self.firstinput = firstinput_ticks
        self.remaining_ticks = -1
        
    def tick(self):
        if self.remaining_ticks == -1:
            self.remaining_ticks = self.firstinput
        if self.remaining_ticks == 0:
            self.keybind.press()
            self.keybind.release()
            self.remaining_ticks = self.interval
        self.remaining_ticks -= 1
    
    def stop(self):
        self.remaining_ticks = -1
        
        
def get_keybind_class(get_data):
    if parse_bool(get_data('use_directinput_keybinds', default='false')):
        return KeyBindDirectInput
    else:
        return KeyBindWin32API

def int_or_hex(v):
    return int(v, 0)

def hex_to_rgb(s):
    if len(s) != 7 or not s.startswith('#'):
        raise Exception('%s is not a valid color.' % s)
    return tuple(int(s[i:i+2],16) for i in (1,3,5))

def center_to_bounds(cx,cy,width,height):
    cx, cy, width, height = map(float, (cx, cy, width, height))
    return cx-width/2, cy-height/2, cx+width/2, cy+height/2
    
def parse_bool(s):
    if s.lower() in ['true', 'yes', '1', 'y', 't']: return True
    elif s.lower() in ['false', 'no', '0', 'n', 'f']: return False
    else: raise Exception('Invalid true/false value: %s' % s)

def parse_config(file_name):
    with open(file_name) as f:
        lines = f.read().split('\n')
    
    settings = {}
    buttons = []
    turntables = []
    
    def action_setting(key, value):
        settings[key] = value
    
    def create_button():
        button = {}
        buttons.append(button)
        def action_button(key, value):
            button[key] = value
        return action_button
    
    def create_turntable():
        turntable = {}
        turntables.append(turntable)
        def action_turntable(key, value):
            turntable[key] = value
        return action_turntable
    
    current_action = None
    
    for l in lines:
        line = l
        if '//' in line: line = line[:line.index('//')]
        line = line.strip()
        if len(line) == 0: continue
        
        if line.startswith('++++') and line.endswith('++++'):
            label = line[4:-4]
            if label == 'BUTTON':
                current_action = create_button()
            elif label == 'TURNTABLE':
                current_action = create_turntable()
            elif label in ['SETTINGS', 'DEFAULTCOLORS', 'DEFAULTSIZES', 'DEFAULTPARAMETERS']:
                current_action = action_setting
            else:
                raise Exception('Unknown label: %s' % label)
        elif '=' in line:
            if current_action == None: continue
            key, value = line.split('=', 1)
            current_action(key, value)
        else:
            raise Exception('Unable to parse line: %s' % line)
        
    return settings, buttons, turntables
    
class KeyButton(object):
    def __init__(self, get_data, rect):
        self.rect = rect
        self.button_index = int(get_data('button_input_index'))
        self.color_lit = get_data('button_color_lit')
        self.color_dark = get_data('button_color_dark')
        self.rgb_flash = hex_to_rgb(get_data('button_color_flash'))
        self.rgb_flash_diff = tuple(b-a for a,b in zip(self.rgb_flash, hex_to_rgb(self.color_lit)))
        KeyBind = get_keybind_class(get_data)    
        self.key_bind = KeyBind(get_data('button_key_bind', transform=int_or_hex, default=None))
        
        self.flash_duration = int(get_data('button_flash_fade_time_ms'))/1000
        self.hold_start_time = None
        
    def get_color(self, pressed, curr_time):
        if pressed:
            if self.hold_start_time == None: self.hold_start_time = curr_time
            dt = curr_time - self.hold_start_time
            if dt < self.flash_duration:
                dt /= self.flash_duration
                return '#{:02x}{:02x}{:02x}'.format(*(int(v+dt*diff) for v,diff in zip(self.rgb_flash, self.rgb_flash_diff)))
            return self.color_lit
        else:
            self.hold_start_time = None
            return self.color_dark
            
    
    
class Turntable(object):
    def __init__(self, get_data, inner_circle, outline_circle):
        self.orbit_r = float(get_data('turntable_diameter_circle_orbit'))/2
        self.circle_r = float(get_data('turntable_diameter_circle'))/2
        self.center_x = float(get_data('turntable_center_x'))
        self.center_y = float(get_data('turntable_center_y'))
        self.index = int(get_data('turntable_axis_index'))
        self.color_positive = hex_to_rgb(get_data('turntable_color_clockwise'))
        self.color_negative = hex_to_rgb(get_data('turntable_color_counterclockwise'))
        KeyBind = get_keybind_class(get_data)
        self.scratch_up_hold = KeyBind(get_data('scratch_up_hold', transform=int_or_hex, default=None))
        self.scratch_down_hold = KeyBind(get_data('scratch_down_hold', transform=int_or_hex, default=None))
        self.scratch_up = KeyBind(get_data('scratch_up', transform=int_or_hex, default=None))
        self.scratch_down = KeyBind(get_data('scratch_down', transform=int_or_hex, default=None))
        self.scratch_up_repeating = KeyRepeater(
            KeyBind(get_data('scratch_up_repeating', transform=int_or_hex, default=None)),
            get_data('keyrepeat_firstinput_ticks', transform=int_or_hex, default=2),
            get_data('keyrepeat_interval_ticks', transform=int_or_hex, default=2),
        )
        self.scratch_down_repeating = KeyRepeater(
            KeyBind(get_data('scratch_down_repeating', transform=int_or_hex, default=None)),
            get_data('keyrepeat_firstinput_ticks', transform=int_or_hex, default=2),
            get_data('keyrepeat_interval_ticks', transform=int_or_hex, default=2),
        )
        
        
        self.inner_circle = inner_circle
        self.outline_circle = outline_circle
        self.last_value = None
        self.velocity = 0
        
        self.integer_angle = 0
        self.single_revolution_distance = round(65536 / float(get_data('turntable_num_revolutions_per_cycle')))
        self.reverse_turntable = parse_bool(get_data('turntable_reverse_direction'))
        
        self.last_positive_time = 0
        self.last_negative_time = 0
        self.detection_timeout = int(get_data('turntable_detection_timeout_ms'))/1000
    
class InputDisplay(object):

    def __init__(self, controller, settings, buttons, turntables):
        self.controller = controller
        self.settings = settings
        self.buttons = buttons
        self.turntables = turntables
        
    def loop(self):
        poll_result = self.controller.poll()
        if poll_result == False:
            print("controller not detected.")
            self.canvas.after(1000, self.loop)
            return
        button_status, info = poll_result
        tt_axes = [info.dwXpos,info.dwYpos,info.dwZpos,info.dwRpos,info.dwUpos,info.dwVpos]
        
        canvas = self.canvas
        curr_time = time.time()
        
        for bt in self.ui_buttons:
            button_pressed = button_status[bt.button_index] if bt.button_index < len(button_status) else False
            canvas.itemconfig(bt.rect, fill=bt.get_color(button_pressed, curr_time))
            bt.key_bind.press() if button_pressed else bt.key_bind.release()
            
        for tt in self.ui_turntables:
            value = tt_axes[tt.index]
        
            if tt.last_value == None: tt.last_value = value
            diff_y = value - tt.last_value
            if diff_y > 32768: diff_y -= 65536 + 255
            elif diff_y < -32768: diff_y += 65536 + 255
            if tt.reverse_turntable: diff_y = -diff_y
            
            # Turntable angle
            tt.integer_angle = (tt.integer_angle + diff_y) % tt.single_revolution_distance
            #angle = -(value)/(65536//4)*TWO_PI
            angle = -(tt.integer_angle/tt.single_revolution_distance)*TWO_PI
            cx = tt.center_x + tt.orbit_r*sin(angle)
            cy = tt.center_y + tt.orbit_r*cos(angle)
            canvas.coords(tt.inner_circle, cx-tt.circle_r, cy-tt.circle_r, cx+tt.circle_r, cy+tt.circle_r)

            sign_diff_y = sign(diff_y)

            # Turntable highlight
            tt.velocity = tt.velocity*0.7 + sign_diff_y*0.3
            colorvec = tt.color_positive if tt.velocity>=0 else tt.color_negative
            color = '#{:02x}{:02x}{:02x}'.format(*(int(min(abs(tt.velocity)*10,0.99)*v) for v in colorvec))
            canvas.itemconfig(tt.outline_circle, outline=color)
            
            if tt.velocity > 0.2:
                tt.scratch_up_hold.press()
                tt.scratch_down_hold.release()
            elif tt.velocity < -0.2:
                tt.scratch_down_hold.press()
                tt.scratch_up_hold.release()
            else:
                tt.scratch_up_hold.release()
                tt.scratch_down_hold.release()
                
            if sign_diff_y > 0:
                if curr_time - tt.last_positive_time <= tt.detection_timeout:
                    tt.scratch_up.press()
                tt.scratch_up_repeating.tick()
                tt.scratch_down.release()
                tt.scratch_down_repeating.stop()
                tt.last_positive_time = curr_time
            elif sign_diff_y < 0:
                if curr_time - tt.last_negative_time <= tt.detection_timeout:
                    tt.scratch_down.press()
                tt.scratch_down_repeating.tick()
                tt.scratch_up.release()
                tt.scratch_up_repeating.stop()
                tt.last_negative_time = curr_time
            else: # sign_diff_y == 0
                if curr_time - tt.last_positive_time > tt.detection_timeout:
                    tt.scratch_up.release()
                    tt.scratch_up_repeating.stop()
                if curr_time - tt.last_negative_time > tt.detection_timeout:
                    tt.scratch_down.release()
                    tt.scratch_down_repeating.stop()

            tt.last_value = value
        
        
        canvas.after(15, self.loop)
        
        
    def initialize(self):
        settings = self.settings
        
        root = tk.Tk()
        root.title('controller input display')
        self.canvas = tk.Canvas(root, width=settings['width'], height=settings['height'], bg=settings['background_color'])
        canvas = self.canvas
        canvas.grid()
        
        def get_data_from(data):
            def get_data(key, transform=lambda x:x, default=Exception):
                if key in data:
                    return transform(data[key])
                elif key in settings:
                    return transform(settings[key])
                elif default == Exception:
                    raise Exception('setting not found: %s' % key)
                else:
                    return default
            return get_data

        self.ui_buttons = []
        self.ui_turntables = []
            
        for button_data in self.buttons:
            gd = get_data_from(button_data)
        
            x1,y1,x2,y2 = center_to_bounds(gd('button_center_x'), gd('button_center_y'), gd('button_width'), gd('button_height'))
            rect = canvas.create_rectangle(x1,y1,x2,y2,fill=settings['button_color_dark'])
            self.ui_buttons.append(KeyButton(gd, rect))
    
        
        for tt_data in self.turntables:
            gd = get_data_from(tt_data)
            def create_circle(diameter, outline, width):
                x1,y1,x2,y2 = center_to_bounds(gd('turntable_center_x'), gd('turntable_center_y'), diameter, diameter)
                return canvas.create_oval(x1,y1,x2,y2,outline=outline,width=width)
            
            outline_circle = create_circle(gd('turntable_diameter_outline'), settings['background_color'], gd('turntable_thickness_outline'))
            create_circle(gd('turntable_diameter_outer_ring'), gd('turntable_color_outer_ring'), gd('turntable_thickness_outer_ring'))
            create_circle(gd('turntable_diameter_inner_ring'), gd('turntable_color_inner_ring'), gd('turntable_thickness_inner_ring'))
            create_circle(gd('turntable_diameter_axle'), gd('turntable_color_axle'), gd('turntable_thickness_axle'))
            inner_circle = create_circle(gd('turntable_diameter_circle'), gd('turntable_color_circle'), gd('turntable_thickness_circle'))
            
            self.ui_turntables.append(Turntable(gd, inner_circle, outline_circle))
        
        
        self.loop()
        root.mainloop()

def main():
    config_file = 'profiles/profile_custom.txt'
    if len(sys.argv) > 1: config_file = sys.argv[1]
    settings, buttons, turntables = parse_config(config_file)
    controller = bmcon.BMStatus(int(settings['joystick_id']))
    input_display = InputDisplay(controller, settings, buttons, turntables)
    input_display.initialize()

if __name__ == '__main__':
    main()