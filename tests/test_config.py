import pytest
from config import GlobalConfig, get_global_config
from models import PlaybackConfig


class TestGlobalConfig:
    def test_singleton_pattern(self):
        config1 = GlobalConfig()
        config2 = GlobalConfig()
        config3 = get_global_config()
        
        assert config1 is config2
        assert config2 is config3
    
    def test_default_config_creation(self):
        config = get_global_config()
        
        assert config.config is not None
        assert len(config.config.basic_notes) == 12
        assert config.config.max_octave == 8
        assert config.config.min_octave == 0
    
    def test_validate_note_name(self):
        config = get_global_config()
        
        assert config.validate_note_name("C") == True
        assert config.validate_note_name("C#") == True
        assert config.validate_note_name("H") == False
        assert config.validate_note_name("") == False
    
    def test_validate_octave(self):
        config = get_global_config()
        
        assert config.validate_octave(4) == True
        assert config.validate_octave(0) == True
        assert config.validate_octave(8) == True
        assert config.validate_octave(-1) == False
        assert config.validate_octave(9) == False
    
    def test_update_playback_config(self):
        config = get_global_config()
        original_midi = config.config.playback.midi
        
        config.update_playback_config(midi=not original_midi)
        assert config.config.playback.midi == (not original_midi)
        
        config.update_playback_config(volume=80, tempo=120)
        assert config.config.playback.volume == 80
        assert config.config.playback.tempo == 120
    
    def test_playback_config_validation(self):
        config = get_global_config()
        
        with pytest.raises(ValueError):
            config.update_playback_config(volume=128)
        
        with pytest.raises(ValueError):
            config.update_playback_config(sample_rate=-1)
