import pytest
from note import Note, basic_notes, MAX_OCTAVE, MIN_OCTAVE


class TestNote:
    def test_note_creation_valid(self):
        note = Note('C', 4)
        assert note.name == 'C'
        assert note.octave == 4
        assert note.frequency == 261.63
        assert note.midi_id == 60
    
    def test_note_creation_with_sharp(self):
        note = Note('C#', 4)
        assert note.name == 'C#'
        assert note.alt_name == 'Db'
        assert note.frequency == 277.18
        assert note.midi_id == 61
    
    def test_note_creation_with_alt_name(self):
        note = Note('Db', 4)
        assert note.name == 'C#'
        assert note.alt_name == 'Db'
    
    def test_note_creation_lowercase(self):
        note = Note('c', 4)
        assert note.name == 'C'
    
    def test_invalid_note_name(self):
        with pytest.raises(ValueError, match="Invalid note name"):
            Note('H', 4)
    
    def test_invalid_octave_high(self):
        with pytest.raises(ValueError, match="Invalid octave value"):
            Note('C', MAX_OCTAVE + 1)
    
    def test_invalid_octave_low(self):
        with pytest.raises(ValueError, match="Invalid octave value"):
            Note('C', MIN_OCTAVE - 1)
    
    def test_octave_frequency_relationship(self):
        c4 = Note('C', 4)
        c5 = Note('C', 5)
        c3 = Note('C', 3)
        
        assert abs(c5.frequency - c4.frequency * 2) < 0.01
        assert abs(c3.frequency - c4.frequency / 2) < 0.01
    
    def test_midi_id_octave_relationship(self):
        c4 = Note('C', 4)
        c5 = Note('C', 5)
        c3 = Note('C', 3)
        
        assert c5.midi_id == c4.midi_id + 12
        assert c3.midi_id == c4.midi_id - 12
    
    def test_note_equality(self):
        note1 = Note('C', 4)
        note2 = Note('C', 4)
        note3 = Note('C', 5)
        note4 = Note('D', 4)
        
        assert note1 == note2
        assert note1 != note3
        assert note1 != note4
        assert note1 != "not a note"
    
    def test_get_next_step_note(self):
        c4 = Note('C', 4)
        c_sharp = c4.get_next_step_note(1)
        d4 = c4.get_next_step_note(2)
        
        assert c_sharp.name == 'C#'
        assert c_sharp.octave == 4
        assert d4.name == 'D'
        assert d4.octave == 4
    
    def test_get_next_step_note_octave_wrap(self):
        b4 = Note('B', 4)
        c5 = b4.get_next_step_note(1)
        
        assert c5.name == 'C'
        assert c5.octave == 5
    
    def test_get_next_step_note_negative(self):
        c4 = Note('C', 4)
        b3 = c4.get_next_step_note(-1)
        
        assert b3.name == 'B'
        assert b3.octave == 3
    
    def test_get_consecutive_notes(self):
        c4 = Note('C', 4)
        chromatic_scale = c4.get_consecutive_notes(13)
        
        assert len(chromatic_scale) == 13
        assert chromatic_scale[0] == c4
        assert chromatic_scale[12].name == 'C'
        assert chromatic_scale[12].octave == 5
    
    def test_octave_converter(self):
        c4 = Note('C', 4)
        c5 = Note('C', 5)
        c3 = Note('C', 3)
        
        assert c4.octave_converter() == 1.0
        assert c5.octave_converter() == 2.0
        assert c3.octave_converter() == 0.5
    
    def test_octave_setter(self):
        note = Note('C', 4)
        note.octave = 5
        
        assert note.octave == 5
        assert note.frequency == 523.26
        assert note.midi_id == 72
    
    def test_basic_notes_structure(self):
        assert 'C' in basic_notes
        assert 'frequency' in basic_notes['C']
        assert 'midi_id' in basic_notes['C']
        assert 'alt_name' in basic_notes['C']
        
        assert len(basic_notes) == 12
        
        for note_name, note_info in basic_notes.items():
            assert isinstance(note_info['frequency'], float)
            assert isinstance(note_info['midi_id'], int)
            assert isinstance(note_info['alt_name'], str)
