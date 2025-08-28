import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_notes():
    from note import Note
    return [
        Note('C', 4),
        Note('D', 4),
        Note('E', 4),
        Note('F', 4),
        Note('G', 4),
        Note('A', 4),
        Note('B', 4)
    ]

@pytest.fixture
def sample_scale_info():
    return {
        'signature': [1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 0.5],
        'info': 'Major scale'
    }

@pytest.fixture
def sample_chord_info():
    return {
        'signature': ['1', '3', '5'],
        'info': 'Major triad'
    }
