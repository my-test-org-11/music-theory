from typing import List
from pydantic import BaseModel, Field, field_validator
from note import Note
from models import ChordInfo


class Chord(BaseModel):
    root_note: Note = Field(..., description="Root note of the chord")
    chord_info: ChordInfo = Field(..., description="Chord information")
    octave: int = Field(4, description="Octave for the chord")
    
    model_config = {"arbitrary_types_allowed": True}
    
    @field_validator('octave')
    @classmethod
    def validate_octave(cls, v):
        if v < 0 or v > 8:
            raise ValueError("Octave must be between 0 and 8")
        return v
    
    def construct_notes(self) -> List[Note]:
        from mt_toolbox import construct_scale, note_modifier
        import re
        
        base_scale_notes = construct_scale(self.root_note.name, 'Major', 'Ionian', self.octave, 9)
        chord_notes = []
        
        for index in self.chord_info.signature:
            index_s = int(re.findall(r'\d+', str(index))[0]) if isinstance(index, str) else index
            note = note_modifier(index, base_scale_notes[index_s-1])
            chord_notes.append(note)
        
        return chord_notes
    
    def get_intervals(self) -> List[str]:
        from mt_toolbox import unify_signature_format
        return unify_signature_format(self.chord_info.signature)


def create_chord(root_name: str, chord_name: str, octave: int = 4) -> Chord:
    from mt_toolbox import all_chord_info
    from models import ChordInfo
    
    if root_name == 'all' or chord_name == 'all':
        raise ValueError("Cannot create Chord object with 'all' parameter")
    
    root_note = Note(root_name, octave)
    chord_info_dict = all_chord_info[chord_name]
    chord_info = ChordInfo(**chord_info_dict)
    
    return Chord(
        root_note=root_note,
        chord_info=chord_info,
        octave=octave
    )
