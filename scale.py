from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator
from note import Note
from models import ScaleInfo, ModeInfo


class Scale(BaseModel):
    root_note: Note = Field(..., description="Root note of the scale")
    scale_info: ScaleInfo = Field(..., description="Scale information")
    mode_name: str = Field("Ionian", description="Mode name")
    scale_length: Optional[int] = Field(None, description="Custom scale length")
    
    model_config = {"arbitrary_types_allowed": True}
    
    @field_validator('mode_name')
    @classmethod
    def validate_mode_name(cls, v):
        valid_modes = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]
        if v not in valid_modes:
            raise ValueError(f"Invalid mode name: {v}. Must be one of {valid_modes}")
        return v
    
    def construct_notes(self) -> List[Note]:
        from mt_toolbox import mode_info, get_modal_scale_signature, S, T
        
        scale_signature = self.scale_info.signature
        scale_length = self.scale_length or len(scale_signature) + 1
        
        if self.mode_name != 'Ionian':
            if len(scale_signature) != 7:
                raise ValueError("Modes not supported for non-heptatonic scales")
            scale_signature = get_modal_scale_signature_internal(scale_signature, self.mode_name)
        
        scale_notes = [self.root_note]
        note = self.root_note
        
        for i in range(scale_length - 1):
            halfstep_count = 1 if scale_signature[i % len(scale_signature)] == S else 2 if scale_signature[i % len(scale_signature)] == T else 3
            note = note.get_next_step_note(halfstep_count)
            scale_notes.append(note)
        
        return scale_notes
    
    def get_degree_intervals(self, degree: int) -> List[str]:
        from mt_toolbox import tone_to_chrom_positions, positions_to_intervals, get_rotated_signature
        
        original_signature = self.scale_info.signature
        degree_rooted_signature = get_rotated_signature(original_signature, degree)
        positions = tone_to_chrom_positions(degree_rooted_signature)
        scale_intervals = positions_to_intervals(positions)
        return scale_intervals
    
    def get_possible_chords_for_degree(self, degree: int) -> List[str]:
        from mt_toolbox import all_chord_info, unify_signature_format
        
        possible_chords = []
        intervals = self.get_degree_intervals(degree)
        
        for chord_name in all_chord_info:
            chord_sig = all_chord_info[chord_name]['signature']
            chord_sig = unify_signature_format(chord_sig)
            if set(chord_sig).issubset(set(intervals)):
                possible_chords.append(chord_name)
        
        return possible_chords


def get_modal_scale_signature_internal(signature: List[float], mode_name: str) -> List[float]:
    from mt_toolbox import mode_info, get_rotated_signature
    
    mode_degree = mode_info[mode_name]
    return get_rotated_signature(signature, mode_degree)


def create_scale(root_name: str, scale_name: str, mode_name: str = "Ionian", 
                octave: int = 4, scale_length: Optional[int] = None) -> Scale:
    from mt_toolbox import all_scale_info
    from models import ScaleInfo
    
    if root_name == 'all' or scale_name == 'all':
        raise ValueError("Cannot create Scale object with 'all' parameter")
    
    root_note = Note(root_name, octave)
    scale_info_dict = all_scale_info[scale_name]
    scale_info = ScaleInfo(**scale_info_dict)
    
    return Scale(
        root_note=root_note,
        scale_info=scale_info,
        mode_name=mode_name,
        scale_length=scale_length
    )
