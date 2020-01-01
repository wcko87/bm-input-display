import ctypes
from ctypes.wintypes import WORD, UINT, DWORD
from ctypes.wintypes import WCHAR as TCHAR

# Fetch function pointers
joyGetNumDevs = ctypes.windll.winmm.joyGetNumDevs
joyGetPos = ctypes.windll.winmm.joyGetPos
joyGetPosEx = ctypes.windll.winmm.joyGetPosEx
joyGetDevCaps = ctypes.windll.winmm.joyGetDevCapsW

# Define constants
MAXPNAMELEN = 32
MAX_JOYSTICKOEMVXDNAME = 260

JOY_RETURNX = 0x1
JOY_RETURNY = 0x2
JOY_RETURNZ = 0x4
JOY_RETURNR = 0x8
JOY_RETURNU = 0x10
JOY_RETURNV = 0x20
JOY_RETURNPOV = 0x40
JOY_RETURNBUTTONS = 0x80
JOY_RETURNRAWDATA = 0x100
JOY_RETURNPOVCTS = 0x200
JOY_RETURNCENTERED = 0x400
JOY_USEDEADZONE = 0x800
JOY_RETURNALL = JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ | JOY_RETURNR | JOY_RETURNU | JOY_RETURNV | JOY_RETURNPOV | JOY_RETURNBUTTONS

# Define some structures from WinMM that we will use in function calls.
class JOYCAPS(ctypes.Structure):
    _fields_ = [
        ('wMid', WORD),
        ('wPid', WORD),
        ('szPname', TCHAR * MAXPNAMELEN),
        ('wXmin', UINT),
        ('wXmax', UINT),
        ('wYmin', UINT),
        ('wYmax', UINT),
        ('wZmin', UINT),
        ('wZmax', UINT),
        ('wNumButtons', UINT),
        ('wPeriodMin', UINT),
        ('wPeriodMax', UINT),
        ('wRmin', UINT),
        ('wRmax', UINT),
        ('wUmin', UINT),
        ('wUmax', UINT),
        ('wVmin', UINT),
        ('wVmax', UINT),
        ('wCaps', UINT),
        ('wMaxAxes', UINT),
        ('wNumAxes', UINT),
        ('wMaxButtons', UINT),
        ('szRegKey', TCHAR * MAXPNAMELEN),
        ('szOEMVxD', TCHAR * MAX_JOYSTICKOEMVXDNAME),
    ]

class JOYINFO(ctypes.Structure):
    _fields_ = [
        ('wXpos', UINT),
        ('wYpos', UINT),
        ('wZpos', UINT),
        ('wButtons', UINT),
    ]

class JOYINFOEX(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('dwFlags', DWORD),
        ('dwXpos', DWORD),
        ('dwYpos', DWORD),
        ('dwZpos', DWORD),
        ('dwRpos', DWORD),
        ('dwUpos', DWORD),
        ('dwVpos', DWORD),
        ('dwButtons', DWORD),
        ('dwButtonNumber', DWORD),
        ('dwPOV', DWORD),
        ('dwReserved1', DWORD),
        ('dwReserved2', DWORD),
    ]

class BMStatus(object):
    def __init__(self, joystick_id):
        # Get the number of supported devices (usually 16).
        num_devs = joyGetNumDevs()
        if num_devs == 0:
            print("Joystick driver not loaded.")

        # Number of the joystick to open.
        # joystick_id = 0

        # Check if the joystick is plugged in.
        info = JOYINFO()
        p_info = ctypes.pointer(info)
        if joyGetPos(0, p_info) != 0:
            print("Joystick %d not plugged in." % (joystick_id + 1))
            
        # Get device capabilities.
        self.caps = JOYCAPS()
        if joyGetDevCaps(joystick_id, ctypes.pointer(self.caps), ctypes.sizeof(JOYCAPS)) != 0:
            print("Failed to get device capabilities.")

        # Initialise the JOYINFOEX structure.
        self.info = JOYINFOEX()
        self.info.dwSize = ctypes.sizeof(JOYINFOEX)
        self.info.dwFlags = JOY_RETURNBUTTONS | JOY_RETURNCENTERED | JOY_RETURNPOV | JOY_RETURNU | JOY_RETURNV | JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ
        self.p_info = ctypes.pointer(self.info)

    def poll(self):
        if joyGetPosEx(0, self.p_info) != 0:
            return False
        dwButtons = self.info.dwButtons
        return [(0 != (1 << b) & dwButtons) for b in range(self.caps.wNumButtons)], self.info


if __name__ == '__main__':
    controller = BMStatus(0)
    all_values = set()
    try:
        while True:
            poll_result = controller.poll()
            if poll_result == False:
                print("controller not detected.")
            button_status, info = poll_result
            angle = ((info.dwYpos)/(65536//4)*256) % 256
            value = info.dwYpos
            all_values.add(value)
            print('angle: %g | raw value: %d' % (angle, value))
    except: pass
    print(all_values)