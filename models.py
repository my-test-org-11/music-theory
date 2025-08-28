from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Union, Optional
import re


class ScaleInfo(BaseModel):
    signature: List[float] = Field(..., description="Scale signature with tone/semitone ratios")
    info: str = Field(..., description="Description of the scale")
    
    @field_validator('signature')
    @classmethod
    def validate_signature(cls, v):
        if not v:
            raise ValueError("Scale signature cannot be empty")
        for interval in v:
            if not isinstance(interval, (int, float)) or interval <= 0:
                raise ValueError("All intervals must be positive numbers")
        return v


class ChordInfo(BaseModel):
    signature: List[Union[int, str]] = Field(..., description="Chord signature with intervals")
    info: str = Field(..., description="Description of the chord")
    
    @field_validator('signature')
    @classmethod
    def validate_signature(cls, v):
        if not v:
            raise ValueError("Chord signature cannot be empty")
        valid_intervals = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 
                          'm2', 'm3', 'm6', 'm7', 'b2', 'b3', 'b5', 'b6', 'b7',
                          'A4', 'A5', 'D5', 'P5', '#4', '#5']
        for interval in v:
            if isinstance(interval, str):
                if not any(valid in str(interval) for valid in valid_intervals + ['1', '2', '3', '4', '5', '6', '7', '8', '9']):
                    if not re.match(r'^[bmA#DP]?\d+$', str(interval)):
                        raise ValueError(f"Invalid interval notation: {interval}")
            elif isinstance(interval, int):
                if interval < 1 or interval > 15:
                    raise ValueError(f"Interval number must be between 1 and 15: {interval}")
        return v


class ModeInfo(BaseModel):
    modes: Dict[str, int] = Field(..., description="Mode names mapped to their starting degrees")
    
    @field_validator('modes')
    @classmethod
    def validate_modes(cls, v):
        if not v:
            raise ValueError("Modes dictionary cannot be empty")
        for mode_name, degree in v.items():
            if not isinstance(mode_name, str) or not mode_name:
                raise ValueError("Mode names must be non-empty strings")
            if not isinstance(degree, int) or degree < 1 or degree > 7:
                raise ValueError(f"Mode degree must be between 1 and 7: {degree}")
        return v


class PlaybackConfig(BaseModel):
    sample_rate: int = Field(44100, description="Audio sample rate")
    sampling: int = Field(4096, description="Sampling rate for wave generation")
    midi: bool = Field(False, description="Use MIDI playback instead of wave")
    arpeggiate: bool = Field(False, description="Arpeggiate chords")
    reverse_scale: bool = Field(False, description="Play scales in reverse as well")
    tempo: int = Field(400, description="MIDI tempo in BPM")
    volume: int = Field(100, description="MIDI volume (0-127)")
    instrument: int = Field(0, description="MIDI instrument number")
    
    @field_validator('sample_rate')
    @classmethod
    def validate_sample_rate(cls, v):
        if v <= 0:
            raise ValueError("Sample rate must be positive")
        return v
    
    @field_validator('volume')
    @classmethod
    def validate_volume(cls, v):
        if v < 0 or v > 127:
            raise ValueError("MIDI volume must be between 0 and 127")
        return v
    
    @field_validator('tempo')
    @classmethod
    def validate_tempo(cls, v):
        if v <= 0:
            raise ValueError("Tempo must be positive")
        return v


class NoteInfo(BaseModel):
    alt_name: str = Field(..., description="Alternative name for the note")
    frequency: float = Field(..., description="Frequency in Hz for octave 4")
    midi_id: int = Field(..., description="MIDI ID for octave 4")
    
    @field_validator('frequency')
    @classmethod
    def validate_frequency(cls, v):
        if v <= 0:
            raise ValueError("Frequency must be positive")
        return v
    
    @field_validator('midi_id')
    @classmethod
    def validate_midi_id(cls, v):
        if v < 0 or v > 127:
            raise ValueError("MIDI ID must be between 0 and 127")
        return v


class MusicTheoryConfig(BaseModel):
    max_octave: int = Field(8, description="Maximum octave number")
    min_octave: int = Field(0, description="Minimum octave number")
    basic_notes: Dict[str, NoteInfo] = Field(..., description="Basic note definitions")
    playback: PlaybackConfig = Field(default_factory=PlaybackConfig)
    
    @field_validator('max_octave')
    @classmethod
    def validate_max_octave(cls, v):
        if v < 0 or v > 10:
            raise ValueError("Max octave must be between 0 and 10")
        return v
    
    @field_validator('min_octave')
    @classmethod
    def validate_min_octave(cls, v):
        if v < 0:
            raise ValueError("Min octave must be non-negative")
        return v
    
    @field_validator('basic_notes')
    @classmethod
    def validate_basic_notes(cls, v):
        if not v:
            raise ValueError("Basic notes cannot be empty")
        valid_note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        for note_name in v.keys():
            if note_name not in valid_note_names:
                raise ValueError(f"Invalid note name: {note_name}")
        return v
