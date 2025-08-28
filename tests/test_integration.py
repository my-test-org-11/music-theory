import pytest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from note import Note
from scale import create_scale
from chord import create_chord
import mt_toolbox as mt


class TestIntegration:
    def test_scale_chord_integration(self):
        scale = create_scale("C", "Major", "Ionian", 4)
        scale_notes = scale.construct_notes()
        
        chord = create_chord("C", "Major_triad", 4)
        chord_notes = chord.construct_notes()
        
        assert chord_notes[0].name == scale_notes[0].name
        assert chord_notes[1].name == scale_notes[2].name
        assert chord_notes[2].name == scale_notes[4].name
    
    def test_backward_compatibility_construct_scale(self):
        old_way = mt.construct_scale("C", "Major", "Ionian", 4)
        
        new_way = create_scale("C", "Major", "Ionian", 4)
        new_notes = new_way.construct_notes()
        
        assert len(old_way) == len(new_notes)
        for old_note, new_note in zip(old_way, new_notes):
            if isinstance(old_note, Note) and isinstance(new_note, Note):
                assert old_note.name == new_note.name
                assert old_note.octave == new_note.octave
    
    def test_backward_compatibility_construct_chord(self):
        old_way = mt.construct_chord("C", "Major_triad", 4)
        
        new_way = create_chord("C", "Major_triad", 4)
        new_notes = new_way.construct_notes()
        
        assert len(old_way) == len(new_notes)
        for old_note, new_note in zip(old_way, new_notes):
            if isinstance(old_note, Note) and isinstance(new_note, Note):
                assert old_note.name == new_note.name
                assert old_note.octave == new_note.octave
    
    def test_all_scales_creation(self):
        for scale_name in mt.all_scale_info.keys():
            try:
                scale = create_scale("C", scale_name, "Ionian", 4)
                notes = scale.construct_notes()
                assert len(notes) > 0
                assert all(isinstance(note, Note) for note in notes)
            except ValueError as e:
                if "Modes not supported" in str(e):
                    continue
                else:
                    raise
    
    def test_all_chords_creation(self):
        for chord_name in mt.all_chord_info.keys():
            chord = create_chord("C", chord_name, 4)
            notes = chord.construct_notes()
            assert len(notes) > 0
            assert all(isinstance(note, Note) for note in notes)
    
    def test_all_modes_with_major_scale(self):
        for mode_name in mt.mode_info.keys():
            scale = create_scale("C", "Major", mode_name, 4)
            notes = scale.construct_notes()
            assert len(notes) == 8
            assert all(isinstance(note, Note) for note in notes)
    
    @patch('builtins.print')
    def test_mt_toolbox_print_functions(self, mock_print):
        mt.print_chord("C", "Major_triad", [Note("C", 4), Note("E", 4), Note("G", 4)])
        mock_print.assert_called()
        
        mt.print_scale("C", "Major", [Note("C", 4), Note("D", 4)], "Ionian")
        assert mock_print.call_count >= 2
    
    def test_note_relationships_in_scales(self):
        c_major = create_scale("C", "Major", "Ionian", 4)
        c_major_notes = c_major.construct_notes()
        
        a_minor = create_scale("A", "Minor", "Ionian", 4)
        a_minor_notes = a_minor.construct_notes()
        
        c_major_names = [note.name for note in c_major_notes[:-1]]
        a_minor_names = [note.name for note in a_minor_notes[:-1]]
        
        assert set(c_major_names) == set(a_minor_names)
    
    def test_octave_wrapping_in_scales(self):
        scale = create_scale("B", "Major", "Ionian", 4, scale_length=15)
        notes = scale.construct_notes()
        
        assert notes[0].octave == 4
        assert any(note.octave == 5 for note in notes)
        assert any(note.octave == 6 for note in notes)
    
    def test_chord_progression_generation(self):
        chord_list, type_list, octave_list = mt.get_chord_list_from_progression("C", [1, 4, 5, 1], 4)
        
        assert len(chord_list) == 4
        assert len(type_list) == 4
        assert len(octave_list) == 4
        assert chord_list[0] == "C"
        assert chord_list[1] == "F"
        assert chord_list[2] == "G"
        assert chord_list[3] == "C"
