# BM Input Display
Input display for rhythm game controllers

[Download Here](https://ci.appveyor.com/project/wcko87/bm-input-display/build/artifacts)

### Video Example: (the input display is in the bottom right corner)

[![input_display_sample](https://user-images.githubusercontent.com/27341392/71674633-b9208480-2d49-11ea-8fa8-194ee5bbfe06.png)](https://thumbs.gfycat.com/PositivePoorAsiaticmouflon-mobile.mp4)


# How to Use

Double click on the bat file corresponding to a profile to run the input display using that profile.
- [Example Profile (BM P1)](https://raw.githubusercontent.com/wcko87/bm-input-display/master/profiles/profile_bm_p1.txt)

Check the profiles folder if you want to customize the input display.
- There are a lot of things that can be configured. (layout, colors, keybinds, etc.)
- This input display can also be used to bind the turntable/buttons to keyboard inputs. (so you can play other games using your controller too)

If you make additional profiles, you might have to make separate .bat files for the new profiles. Open the .bat file in a text editor to check the format of the .bat file. It shouldn't be too hard to figure out from there.


# Running from the Command Line
If you'd rather not download an executable file, or you'd like to modify the code directly, you can run the script directly using python. (it should work on any recent version of python)

Download the source code from this repository, and install `pywin32` via:
```
pip install pywin32
```

Then to run the script (using the `profile_bm_p1.txt` profile for example), run:
```
python inputdisplay.py profiles/profile_bm_p1.txt
```


# Using Keybinds with IIDX INFINITAS
- This input display can be used to keybind the analog turntable to Infinitas.
- The profiles `profile_infinitas_p1.txt` and `profile_infinitas_p2.txt` will keybind your controller keys and turntable to the default keyboard keybinds (LCTRL LSHIFT ZSXDCFV for P1 and BHNJMK, RSHIFT RCTRL for P2) used by Infinitas.
- However, the four option keys (E1, E2, E3, E4) don't have equivalent keys on the keyboard, and so can't be keybinded this way. You will need to configure keys E1-E4 in the Infinitas key config menu separately.

### Q: How do I unbind the other keys in Infinitas?
**Context:** You might observe that as this input display keybinds the controller inputs to keyboard keys, you should be unbinding the actual controller keys and turntable in the Infinitas config so that they do not interfere with extra inputs.

The Infinitas setting UI does not offer an option to unbind controller keys. However, you can still unbind keys this way:
1. Configure the keys you care about (e.g. E1-E4) in the Infinitas launcher, and click SAVE(保存). Note that the UI does not allow you to click save if not all keys have been configured.
2. Go to your Infinitas installation folder and look for `.\Resource\config\1001_cf.xml`, which is a config file that contains all your keybinds. Open it in a text editor like Notepad.
3. You should see a list of keybinds. To unbind a key, change the value to 0.
    Example:
    ```xml
    <KeyValuePair>
      <Key>
        <string>KeyConfig1P_1</string>
      </Key>
      <Value>
        <string>0</string>
      </Value>
    </KeyValuePair>
    ```

### Q: How do I make keybinds work in Infinitas?
(This is only relevant when making your own profiles)

By default, the input display's keybinds do not work in Infinitas. However, you can switch the keybind method to DirectInput by setting `use_directinput_keybinds=true` in the config. DirectInput works with Infinitas, but uses a completely different set of input keycodes from the default (Win32API). The two given Infinitas profiles use this.


