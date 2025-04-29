#!/usr/bin/env python3
"""
notefreq.py  —  Convert between pitch names and frequencies.

Usage examples
--------------
$ ./notefreq.py A4          # → 440.00 Hz
$ ./notefreq.py 329.63      # → E4  (+0.00 cents)
$ ./notefreq.py 445         # → A4  (+19.56 cents)
"""

import argparse, math, re, sys

A4_FREQ = 440.0
A4_MIDI = 69                    # MIDI number for A4
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']
ENHARMONICS = {'DB': 'C#', 'EB': 'D#', 'GB': 'F#', 'AB': 'G#', 'BB': 'A#'}

note_re = re.compile(r'^([A-Ga-g])([bB#♭♯]?)(-?\d+)$')

def note_to_midi(name: str) -> int:
    m = note_re.match(name.replace('♯', '#').replace('♭', 'b'))
    if not m:
        raise ValueError(f"Bad note: {name}")
    letter, accidental, octave = m.groups()
    letter = letter.upper()

    # Normalize flats, e.g. Db → C#
    accidental = accidental.replace('b', 'B').replace('#', '#').upper()
    if accidental == 'B':
        letter = ENHARMONICS.get(letter + 'B', letter + '#')[:-1]
        accidental = '#'

    index = NOTE_NAMES.index(letter + accidental)
    return 12 * (int(octave) + 1) + index

def midi_to_note(midi: int) -> str:
    name = NOTE_NAMES[midi % 12]
    octave = midi // 12 - 1
    return f"{name}{octave}"

def midi_to_freq(midi: int) -> float:
    return A4_FREQ * 2 ** ((midi - A4_MIDI) / 12)

def freq_to_midi(freq: float):
    midi = 12 * math.log2(freq / A4_FREQ) + A4_MIDI
    nearest = round(midi)
    cents = (midi - nearest) * 100
    return int(nearest), float(cents)

def main():
    ap = argparse.ArgumentParser(description="Convert between note names and frequencies.")
    ap.add_argument("value", help="Pitch (e.g. C#4) or frequency in hertz")
    args = ap.parse_args()

    val = args.value.strip()
    try:
        # Try numeric first
        freq = float(val)
        if freq <= 0:
            raise ValueError
        midi, cents = freq_to_midi(freq)
        note = midi_to_note(midi)
        print(f"{note} ({cents:+.2f} cents)")

    except ValueError:
        # Treat as note name
        try:
            midi = note_to_midi(val)
        except ValueError as e:
            sys.exit(e)
        freq = midi_to_freq(midi)
        print(f"{freq:.2f} Hz")

if __name__ == "__main__":
    main()
