from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt
import matplotlib.figure
import matplotlib.axes
import numpy as np
from note import Note


class BaseVisualizer(ABC):
    def __init__(self):
        self.note_colors = ['firebrick', 'saddlebrown', 'orange', 'darkkhaki', 'yellow', 
                           'limegreen', 'darkolivegreen', 'dodgerblue', 'slategrey', 
                           'slateblue', 'darkviolet', 'indigo']
        self.chromatic_note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.interval_list = ['1', 'm2', '2', 'm3', '3', '4', 'A4', '5', 'm6', '6', 'm7', '7']
    
    def get_note_color(self, note_name: str) -> str:
        try:
            index = self.chromatic_note_names.index(note_name)
            return self.note_colors[index]
        except ValueError:
            return 'gray'
    
    def get_chromatic_position(self, note_name: str) -> int:
        try:
            return self.chromatic_note_names.index(note_name)
        except ValueError:
            return 0
    
    def rotate_note_names(self, root_name: str) -> List[str]:
        root_pos = self.get_chromatic_position(root_name)
        return self.chromatic_note_names[root_pos:] + self.chromatic_note_names[:root_pos]
    
    def rotate_colors(self, root_name: str) -> List[str]:
        root_pos = self.get_chromatic_position(root_name)
        return self.note_colors[-root_pos:] + self.note_colors[:-root_pos]
    
    @abstractmethod
    def setup_plot(self) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
        pass
    
    @abstractmethod
    def show_notes(self, notes: List[str], **kwargs):
        pass
    
    @abstractmethod
    def set_title(self, title: str):
        pass
    
    def display(self):
        plt.show()


class CommonVisualizationMixin:
    def extract_note_names(self, notes: List[Note]) -> List[str]:
        return [note.name for note in notes]
    
    def validate_notes(self, notes: List[str]) -> bool:
        valid_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return all(note in valid_notes for note in notes)
    
    def get_note_positions(self, notes: List[str], reference_list: List[str]) -> List[int]:
        positions = []
        for note in notes:
            try:
                positions.extend([i for i, ref_note in enumerate(reference_list) if ref_note == note])
            except ValueError:
                continue
        return positions
