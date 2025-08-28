import pytest
from chord import Chord, create_chord
from note import Note
from models import ChordInfo


class TestChord:
    def test_create_major_chord(self):
        chord = create_chord("C", "Major_triad", 4)
        notes = chord.construct_notes()
        
        assert len(notes) == 3
        assert notes[0].name == "C"
        assert notes[1].name == "E"
        assert notes[2].name == "G"
    
    def test_create_minor_chord(self):
        chord = create_chord("C", "Minor_triad", 4)
        notes = chord.construct_notes()
        
        assert len(notes) == 3
        assert notes[0].name == "C"
        assert notes[1].name == "D#"
        assert notes[2].name == "G"
    
    def test_create_seventh_chord(self):
        chord = create_chord("C", "Major_7th", 4)
        notes = chord.construct_notes()
        
        assert len(notes) == 4
        assert notes[0].name == "C"
        assert notes[1].name == "E"
        assert notes[2].name == "G"
        assert notes[3].name == "B"
    
    def test_create_power_chord(self):
        chord = create_chord("C", "Power", 4)
        notes = chord.construct_notes()
        
        assert len(notes) == 3
        assert notes[0].name == "C"
        assert notes[1].name == "G"
        assert notes[2].name == "C"
        assert notes[2].octave == 5
    
    def test_different_octaves(self):
        chord3 = create_chord("C", "Major_triad", 3)
        chord5 = create_chord("C", "Major_triad", 5)
        
        notes3 = chord3.construct_notes()
        notes5 = chord5.construct_notes()
        
        assert notes3[0].octave == 3
        assert notes5[0].octave == 5
        assert notes5[0].frequency == notes3[0].frequency * 4
    
    def test_get_intervals(self):
        chord = create_chord("C", "Major_triad", 4)
        intervals = chord.get_intervals()
        
        assert "1" in intervals
        assert "3" in intervals
        assert "5" in intervals
    
    def test_invalid_octave(self):
        with pytest.raises(ValueError, match="Octave must be between 0 and 8"):
            Chord(
                root_note=Note("C", 4),
                chord_info=ChordInfo(signature=[1, 3, 5], info="Test"),
                octave=9
            )
    
    def test_create_chord_with_all_parameter(self):
        with pytest.raises(ValueError, match="Cannot create Chord object with 'all' parameter"):
            create_chord("all", "Major_triad", 4)
        
        with pytest.raises(ValueError, match="Cannot create Chord object with 'all' parameter"):
            create_chord("C", "all", 4)


class TestChordIntegration:
    def test_diminished_chord(self):
        chord = create_chord("C", "Diminished", 4)
        notes = chord.construct_notes()
        
        assert len(notes) == 3
        assert notes[0].name == "C"
        assert notes[1].name == "D#"
        assert notes[2].name == "F#"
    
    def test_augmented_chord(self):
        chord = create_chord("C", "Augmented", 4)
        notes = chord.construct_notes()
        
        assert len(notes) == 3
        assert notes[0].name == "C"
        assert notes[1].name == "E"
        assert notes[2].name == "G#"
    
    def test_suspended_chords(self):
        sus2 = create_chord("C", "Suspended_2", 4)
        sus4 = create_chord("C", "Suspended_4", 4)
        
        sus2_notes = sus2.construct_notes()
        sus4_notes = sus4.construct_notes()
        
        assert sus2_notes[1].name == "D"
        assert sus4_notes[1].name == "F"
