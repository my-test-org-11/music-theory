import pytest
from models import ScaleInfo, ChordInfo, ModeInfo, PlaybackConfig, NoteInfo, MusicTheoryConfig


class TestScaleInfo:
    def test_valid_scale_info(self):
        scale = ScaleInfo(
            signature=[2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.0],
            info="Major scale"
        )
        assert len(scale.signature) == 7
        assert scale.info == "Major scale"
    
    def test_empty_signature(self):
        with pytest.raises(ValueError, match="Scale signature cannot be empty"):
            ScaleInfo(signature=[], info="Empty scale")
    
    def test_invalid_signature_values(self):
        with pytest.raises(ValueError, match="All intervals must be positive numbers"):
            ScaleInfo(signature=[2.0, -1.0, 1.0], info="Invalid scale")


class TestChordInfo:
    def test_valid_chord_info(self):
        chord = ChordInfo(
            signature=[1, 3, 5],
            info="Major triad"
        )
        assert chord.signature == [1, 3, 5]
        assert chord.info == "Major triad"
    
    def test_chord_with_string_intervals(self):
        chord = ChordInfo(
            signature=[1, 'm3', 'P5'],
            info="Minor triad"
        )
        assert chord.signature == [1, 'm3', 'P5']
    
    def test_empty_signature(self):
        with pytest.raises(ValueError, match="Chord signature cannot be empty"):
            ChordInfo(signature=[], info="Empty chord")
    
    def test_invalid_interval_number(self):
        with pytest.raises(ValueError, match="Interval number must be between 1 and 15"):
            ChordInfo(signature=[1, 16, 5], info="Invalid chord")


class TestModeInfo:
    def test_valid_mode_info(self):
        modes = ModeInfo(modes={
            "Ionian": 1,
            "Dorian": 2,
            "Phrygian": 3
        })
        assert modes.modes["Ionian"] == 1
        assert modes.modes["Dorian"] == 2
    
    def test_empty_modes(self):
        with pytest.raises(ValueError, match="Modes dictionary cannot be empty"):
            ModeInfo(modes={})
    
    def test_invalid_degree(self):
        with pytest.raises(ValueError, match="Mode degree must be between 1 and 7"):
            ModeInfo(modes={"Invalid": 8})


class TestPlaybackConfig:
    def test_default_config(self):
        config = PlaybackConfig()
        assert config.sample_rate == 44100
        assert config.midi == False
        assert config.volume == 100
    
    def test_custom_config(self):
        config = PlaybackConfig(
            sample_rate=48000,
            midi=True,
            volume=80
        )
        assert config.sample_rate == 48000
        assert config.midi == True
        assert config.volume == 80
    
    def test_invalid_volume(self):
        with pytest.raises(ValueError, match="MIDI volume must be between 0 and 127"):
            PlaybackConfig(volume=128)
    
    def test_invalid_sample_rate(self):
        with pytest.raises(ValueError, match="Sample rate must be positive"):
            PlaybackConfig(sample_rate=-1)


class TestNoteInfo:
    def test_valid_note_info(self):
        note = NoteInfo(
            alt_name="Db",
            frequency=277.18,
            midi_id=61
        )
        assert note.alt_name == "Db"
        assert note.frequency == 277.18
        assert note.midi_id == 61
    
    def test_invalid_frequency(self):
        with pytest.raises(ValueError, match="Frequency must be positive"):
            NoteInfo(alt_name="", frequency=-1.0, midi_id=60)
    
    def test_invalid_midi_id(self):
        with pytest.raises(ValueError, match="MIDI ID must be between 0 and 127"):
            NoteInfo(alt_name="", frequency=440.0, midi_id=128)


class TestMusicTheoryConfig:
    def test_valid_config(self):
        basic_notes = {
            "C": NoteInfo(alt_name="", frequency=261.63, midi_id=60),
            "D": NoteInfo(alt_name="", frequency=293.66, midi_id=62)
        }
        config = MusicTheoryConfig(basic_notes=basic_notes)
        assert len(config.basic_notes) == 2
        assert config.max_octave == 8
        assert config.min_octave == 0
    
    def test_invalid_octave_range(self):
        basic_notes = {"C": NoteInfo(alt_name="", frequency=261.63, midi_id=60)}
        
        with pytest.raises(ValueError, match="Max octave must be between 0 and 10"):
            MusicTheoryConfig(basic_notes=basic_notes, max_octave=11)
    
    def test_empty_basic_notes(self):
        with pytest.raises(ValueError, match="Basic notes cannot be empty"):
            MusicTheoryConfig(basic_notes={})
    
    def test_invalid_note_name(self):
        basic_notes = {
            "H": NoteInfo(alt_name="", frequency=261.63, midi_id=60)
        }
        with pytest.raises(ValueError, match="Invalid note name: H"):
            MusicTheoryConfig(basic_notes=basic_notes)
