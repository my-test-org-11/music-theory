from pydantic import BaseModel, Field
from models import MusicTheoryConfig, PlaybackConfig, NoteInfo
from typing import Dict


class GlobalConfig:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._config = self._create_default_config()
    
    def _create_default_config(self) -> MusicTheoryConfig:
        from note import basic_notes
        
        basic_notes_models = {}
        for note_name, note_data in basic_notes.items():
            basic_notes_models[note_name] = NoteInfo(**note_data)
        
        return MusicTheoryConfig(
            basic_notes=basic_notes_models,
            playback=PlaybackConfig()
        )
    
    @property
    def config(self) -> MusicTheoryConfig:
        return self._config
    
    def update_playback_config(self, **kwargs):
        if self._config is not None:
            current_playback = self._config.playback.model_dump()
            current_playback.update(kwargs)
            self._config.playback = PlaybackConfig(**current_playback)
    
    def validate_note_name(self, note_name: str) -> bool:
        if self._config is not None:
            return note_name in self._config.basic_notes
        return False
    
    def validate_octave(self, octave: int) -> bool:
        if self._config is not None:
            return self._config.min_octave <= octave <= self._config.max_octave
        return False


def get_global_config() -> GlobalConfig:
    return GlobalConfig()
