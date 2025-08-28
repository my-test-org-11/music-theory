from typing import List, Optional
from pydantic import BaseModel
from note import Note
from models import PlaybackConfig
import pygame
import pygame.sndarray
import numpy
import scipy.signal
from midiutil import MIDIFile
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class AudioPlayer(BaseModel):
    config: PlaybackConfig = PlaybackConfig()
    
    model_config = {"arbitrary_types_allowed": True, "extra": "allow"}
    
    def __init__(self, **data):
        super().__init__(**data)
        self._initialize_pygame()
    
    def _initialize_pygame(self):
        pygame.mixer.init(self.config.sample_rate, -16, 1)
    
    def sine_wave(self, hz: float, peak: int, n_samples: Optional[int] = None) -> numpy.ndarray:
        n_samples = n_samples or self.config.sample_rate
        length = self.config.sample_rate / float(hz)
        omega = numpy.pi * 2 / length
        xvalues = numpy.arange(int(length)) * omega
        onecycle = peak * numpy.sin(xvalues)
        return numpy.resize(onecycle, (n_samples,)).astype(numpy.int16)
    
    def play_wave(self, wave: numpy.ndarray, ms: int):
        sound = pygame.sndarray.make_sound(wave.astype(numpy.int16))
        sound.play(-1)
        pygame.time.delay(ms)
        sound.stop()
    
    def play_note(self, note: Note, ms: int):
        if self.config.midi:
            self.create_midi([note], 'note')
            self.play_midi_file('out.mid')
        else:
            self.play_wave(self.sine_wave(note.frequency, self.config.sampling), ms)
    
    def play_chord(self, chord_notes: List[Note]):
        chord_wave = numpy.zeros(self.config.sample_rate, dtype=numpy.int16)
        for note in chord_notes:
            note_wave = self.sine_wave(note.frequency, self.config.sampling)
            chord_wave = chord_wave + note_wave
        
        print('Chord is now being played..')
        if self.config.midi:
            self.create_midi(chord_notes, 'chord')
            self.play_midi_file('out.mid')
        else:
            self.play_wave(chord_wave, 700)
        pygame.time.delay(100)
        
        if self.config.arpeggiate:
            print('Single notes of the chord are now being played separately..')
            if self.config.midi:
                self.create_midi(chord_notes, 'scale', t=0.3)
                self.play_midi_file('out.mid')
            else:
                for note in chord_notes:
                    self.play_wave(self.sine_wave(note.frequency, self.config.sampling), 500)
            pygame.time.delay(100)
            print('Chord is now being played again..')
            if self.config.midi:
                self.create_midi(chord_notes, 'chord')
                self.play_midi_file('out.mid')
            else:
                self.play_wave(chord_wave, 700)
    
    def play_scale(self, scale_notes: List[Note], ms: int):
        print('Scale is now being played forward..')
        if self.config.midi:
            self.create_midi(scale_notes, 'scale')
            self.play_midi_file('out.mid')
        else:
            self.play_piece(scale_notes, ms)
        
        if self.config.reverse_scale:
            reverse_scale = scale_notes[::-1]
            scale_notes.extend(reverse_scale[1:])
            pygame.time.delay(200)
            print('Scale is now being played forward and then backwards..')
            if self.config.midi:
                self.create_midi(scale_notes, 'scale')
                self.play_midi_file('out.mid')
            else:
                self.play_piece(scale_notes, ms)
    
    def play_piece(self, notes: List[Note], ms: int):
        for note in notes:
            self.play_note(note, ms)
    
    def create_midi(self, note_list: List[Note], type_: str, t: float = 0.3):
        time = 0
        MyMIDI = MIDIFile(1)
        MyMIDI.addProgramChange(0, 0, time, self.config.instrument)
        MyMIDI.addTempo(0, time, self.config.tempo)
        
        for note in note_list:
            MyMIDI.addNote(0, 0, note.midi_id, time, 8, self.config.volume)
            if type_ == 'scale':
                padding_in_beats = ((t * self.config.tempo) / 60) + 0.1
                time += padding_in_beats
        
        with open('out.mid', "wb") as output_file:
            MyMIDI.writeFile(output_file)
    
    def create_arp_chord_midi(self, note_list: List[Note], t: float = 1.5):
        time = 0
        MyMIDI = MIDIFile(1)
        MyMIDI.addProgramChange(0, 0, time, self.config.instrument)
        MyMIDI.addTempo(0, time, self.config.tempo)
        
        for note in note_list:
            MyMIDI.addNote(0, 0, note.midi_id, time, 8, self.config.volume)
            padding_in_beats = ((t * self.config.tempo) / 60) + 0.1
            time += padding_in_beats
        
        time += 2.5 * padding_in_beats
        
        for note in note_list:
            MyMIDI.addNote(0, 0, note.midi_id, time, 8, self.config.volume)
        
        with open('out.mid', "wb") as output_file:
            MyMIDI.writeFile(output_file)
    
    def play_midi_file(self, midi_filename: str):
        try:
            clock = pygame.time.Clock()
            pygame.mixer.music.load(midi_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                clock.tick(30)
        except KeyboardInterrupt:
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()
            raise SystemExit
