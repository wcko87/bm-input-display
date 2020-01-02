# BM Input Display
Input display for rhythm game controllers

[Download Here](https://ci.appveyor.com/project/wcko87/bm-input-display/build/artifacts)

### Video Example: (the input display is in the bottom right corner)

[![input_display_sample](https://user-images.githubusercontent.com/27341392/71674633-b9208480-2d49-11ea-8fa8-194ee5bbfe06.png)](https://thumbs.gfycat.com/PositivePoorAsiaticmouflon-mobile.mp4)


# How to Use

Double click on the bat file corresponding to a profile to run the input display using that profile.

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
