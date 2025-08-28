import pytest
from scale import Scale, create_scale
from note import Note
from models import ScaleInfo


class TestScale:
    def test_create_major_scale(self):
        scale = create_scale("C", "Major", "Ionian", 4)
        notes = scale.construct_notes()
        
        assert len(notes) == 8
        assert notes[0].name == "C"
        assert notes[1].name == "D"
        assert notes[2].name == "E"
        assert notes[7].name == "C"
        assert notes[7].octave == 5
    
    def test_create_minor_scale(self):
        scale = create_scale("A", "Minor", "Ionian", 4)
        notes = scale.construct_notes()
        
        assert len(notes) == 8
        assert notes[0].name == "A"
        assert notes[2].name == "C"
        assert notes[5].name == "F"
    
    def test_create_dorian_mode(self):
        scale = create_scale("D", "Major", "Dorian", 4)
        notes = scale.construct_notes()
        
        assert len(notes) == 8
        assert notes[0].name == "D"
    
    def test_invalid_mode_for_pentatonic(self):
        with pytest.raises(ValueError, match="Modes not supported for non-heptatonic scales"):
            scale = create_scale("C", "Major_pentatonic", "Dorian", 4)
            scale.construct_notes()
    
    def test_custom_scale_length(self):
        scale = create_scale("C", "Major", "Ionian", 4, scale_length=15)
        notes = scale.construct_notes()
        
        assert len(notes) == 15
        assert notes[7].name == "C"
        assert notes[7].octave == 5
        assert notes[14].name == "C"
        assert notes[14].octave == 6
        assert notes[14].octave == 6
    
    def test_get_degree_intervals(self):
        scale = create_scale("C", "Major", "Ionian", 4)
        intervals = scale.get_degree_intervals(1)
        
        assert "1" in intervals
        assert "3" in intervals
        assert "5" in intervals
    
    def test_get_possible_chords_for_degree(self):
        scale = create_scale("C", "Major", "Ionian", 4)
        chords = scale.get_possible_chords_for_degree(1)
        
        assert "Major_triad" in chords
        assert "Major_7th" in chords
    
    def test_invalid_mode_name(self):
        with pytest.raises(ValueError, match="Invalid mode name"):
            Scale(
                root_note=Note("C", 4),
                scale_info=ScaleInfo(signature=[2.0, 2.0, 1.0], info="Test"),
                mode_name="InvalidMode"
            )
    
    def test_create_scale_with_all_parameter(self):
        with pytest.raises(ValueError, match="Cannot create Scale object with 'all' parameter"):
            create_scale("all", "Major", "Ionian", 4)
        
        with pytest.raises(ValueError, match="Cannot create Scale object with 'all' parameter"):
            create_scale("C", "all", "Ionian", 4)


class TestScaleIntegration:
    def test_chromatic_scale(self):
        scale = create_scale("C", "Chromatic", "Ionian", 4)
        notes = scale.construct_notes()
        
        assert len(notes) == 13
        note_names = [note.name for note in notes]
        expected_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]
        assert note_names == expected_names
    
    def test_blues_scale(self):
        scale = create_scale("C", "Blues", "Ionian", 4)
        notes = scale.construct_notes()
        
        assert len(notes) == 7
        assert notes[0].name == "C"
        assert notes[-1].name == "C"
        assert notes[-1].octave == 5
