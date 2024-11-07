# Chip-8 Emulator

Is an implementation of the classical 8-bit microcomputer.

The documentation that I follow to do this project is the following:
http://devernay.free.fr/hacks/chip8/C8TECH10.HTM

## Project Structure and File 

- main.py: Is the entry point, all the pygame engine imports, game loop, and the clock normalization are defined here.

Inside the src folder are the modules that make the emulator works:
- src/cpu.py: CPU Definition, all the implementation of the cpu instruction lives in this module
- src/keyboard.py: Keyboard input definition, key definition and keybinding are defined here
- src/ram.py: A data structure representing the RAM memory. 
- src/screen.py: The representation of the screen of the emulator, all the functions that controls the screen are defined here.
- src/singleton.py: A helper class to share the state between the components independently of where are defined.

## Executing the program

```
git clone git@github.com:harpiechoise/Chip-8-Emulator.git
cd Chip-8-Emulator
pip install -r requirements.txt
python main.py <rom_path>
```

## Example
```
python main.py Pong.ch8
```

Feel free to modify this project.