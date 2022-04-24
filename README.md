# Doppler Effect Simulator

The program simulates how a sound coming from a moving source is heard form a receptor (Doppler effect). The source moves on a circular track with a speed that can be set; the position of the receptor is also set-able.

### Installation

On the project's directory, create a virtual environment for the program and install the needed packages

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Depending on your system you might have to install additional graphic backend for `matplotlib`.

### Usage

```
usage: main.py [-h] [-a FIN] [-R R] [-v V] [-c C] [--x0 X0] [--y0 Y0] [-o FOUT] [-i] [-V]

Simulates the sound from a source moving in a circle taking Doppler effect into account.

options:
  -h, --help            show this help message and exit
  -a FIN, --input FIN   Input audio file in WAV format
  -R R, --radius R      Radius of source's trajectory in meters (default = 100)
  -v V, --velocity V    Speed of the source in meters per second (default = 30)
  -c C, --sound-speed C
                        Speed of the sound in meters per second (default = 300)
  --x0 X0               Initial x position of receptor in meters (default = 0)
  --y0 Y0               Initial y position of receptor in meters (default = 0)
  -o FOUT, --output FOUT
                        Output file
  -i, --interactive     Interactive mode
  -V, --version         show program's version number and exit
```

In order to get an audio with the result of applying Doppler effect to a sound run the program giving the `-o` (or `--output`) argument and specifying a path to save the file. Example:

```bash
python main.py -a test/data_train-whistle.wav -o test.wav
```

#### Interactive mode

Give the flag `-i`(or `--interactive`) in order to run in interactive mode; here you can see an animation of the movement an interact with the receptor. The bindings are this:

- Left click: changes receptor position,
- Right click (or `spacebar`): toggles play/pause the animation
- Middle click (or `Enter`): starts the animation as if the sound was emitted in the current position
- Scroll wheel: changes the position of the source
