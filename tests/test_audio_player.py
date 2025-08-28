import pytest
from unittest.mock import Mock, patch, MagicMock
from audio_player import AudioPlayer
from note import Note
from models import PlaybackConfig
import numpy


class TestAudioPlayer:
    @patch('audio_player.pygame')
    def test_audio_player_initialization(self, mock_pygame):
        config = PlaybackConfig(sample_rate=48000)
        player = AudioPlayer(config=config)
        
        assert player.config.sample_rate == 48000
        mock_pygame.mixer.init.assert_called_once_with(48000, -16, 1)
    
    @patch('audio_player.pygame')
    def test_sine_wave_generation(self, mock_pygame):
        player = AudioPlayer()
        wave = player.sine_wave(440.0, 1000, 1000)
        
        assert isinstance(wave, numpy.ndarray)
        assert len(wave) == 1000
        assert wave.dtype == numpy.int16
    
    @patch('audio_player.pygame')
    def test_play_wave(self, mock_pygame):
        player = AudioPlayer()
        mock_sound = Mock()
        mock_pygame.sndarray.make_sound.return_value = mock_sound
        
        wave = numpy.array([1, 2, 3], dtype=numpy.int16)
        player.play_wave(wave, 100)
        
        mock_pygame.sndarray.make_sound.assert_called_once()
        mock_sound.play.assert_called_once_with(-1)
        mock_pygame.time.delay.assert_called_once_with(100)
        mock_sound.stop.assert_called_once()
    
    @patch('audio_player.pygame')
    def test_play_note_wave_mode(self, mock_pygame):
        player = AudioPlayer(config=PlaybackConfig(midi=False))
        note = Note("C", 4)
        
        with patch.object(player, 'play_wave') as mock_play_wave:
            with patch.object(player, 'sine_wave') as mock_sine_wave:
                mock_sine_wave.return_value = numpy.zeros(player.config.sample_rate, dtype=numpy.int16)
                player.play_note(note, 500)
                
                mock_sine_wave.assert_called_once_with(note.frequency, player.config.sampling)
                mock_play_wave.assert_called_once()
    
    @patch('audio_player.pygame')
    def test_play_note_midi_mode(self, mock_pygame):
        player = AudioPlayer(config=PlaybackConfig(midi=True))
        note = Note("C", 4)
        
        with patch.object(player, 'create_midi') as mock_create_midi:
            with patch.object(player, 'play_midi_file') as mock_play_midi:
                player.play_note(note, 500)
                
                mock_create_midi.assert_called_once_with([note], 'note')
                mock_play_midi.assert_called_once_with('out.mid')
    
    @patch('audio_player.pygame')
    def test_play_chord_wave_mode(self, mock_pygame):
        player = AudioPlayer(config=PlaybackConfig(midi=False, arpeggiate=False))
        notes = [Note("C", 4), Note("E", 4), Note("G", 4)]
        
        with patch.object(player, 'play_wave') as mock_play_wave:
            with patch.object(player, 'sine_wave') as mock_sine_wave:
                mock_sine_wave.return_value = numpy.zeros(player.config.sample_rate, dtype=numpy.int16)
                player.play_chord(notes)
                
                assert mock_sine_wave.call_count == 3
                mock_play_wave.assert_called()
    
    @patch('audio_player.pygame')
    def test_play_chord_with_arpeggiation(self, mock_pygame):
        player = AudioPlayer(config=PlaybackConfig(midi=False, arpeggiate=True))
        notes = [Note("C", 4), Note("E", 4), Note("G", 4)]
        
        with patch.object(player, 'play_wave') as mock_play_wave:
            with patch.object(player, 'sine_wave') as mock_sine_wave:
                mock_sine_wave.return_value = numpy.zeros(player.config.sample_rate, dtype=numpy.int16)
                player.play_chord(notes)
                
                assert mock_play_wave.call_count >= 4
    
    @patch('audio_player.pygame')
    def test_play_scale(self, mock_pygame):
        player = AudioPlayer(config=PlaybackConfig(midi=False, reverse_scale=False))
        notes = [Note("C", 4), Note("D", 4), Note("E", 4)]
        
        with patch.object(player, 'play_piece') as mock_play_piece:
            player.play_scale(notes, 300)
            
            mock_play_piece.assert_called_once_with(notes, 300)
    
    @patch('audio_player.pygame')
    def test_play_scale_with_reverse(self, mock_pygame):
        player = AudioPlayer(config=PlaybackConfig(midi=False, reverse_scale=True))
        notes = [Note("C", 4), Note("D", 4), Note("E", 4)]
        
        with patch.object(player, 'play_piece') as mock_play_piece:
            player.play_scale(notes, 300)
            
            assert mock_play_piece.call_count == 2
    
    @patch('audio_player.pygame')
    @patch('builtins.open', create=True)
    @patch('audio_player.MIDIFile')
    def test_create_midi(self, mock_midi_file, mock_open, mock_pygame):
        player = AudioPlayer()
        notes = [Note("C", 4), Note("E", 4)]
        mock_midi = Mock()
        mock_midi_file.return_value = mock_midi
        
        player.create_midi(notes, 'chord')
        
        mock_midi_file.assert_called_once_with(1)
        mock_midi.addProgramChange.assert_called_once()
        mock_midi.addTempo.assert_called_once()
        assert mock_midi.addNote.call_count == 2
        mock_midi.writeFile.assert_called_once()
    
    @patch('audio_player.pygame')
    def test_play_midi_file(self, mock_pygame):
        player = AudioPlayer()
        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock
        mock_pygame.mixer.music.get_busy.side_effect = [True, True, False]
        
        player.play_midi_file('test.mid')
        
        mock_pygame.mixer.music.load.assert_called_once_with('test.mid')
        mock_pygame.mixer.music.play.assert_called_once()
        assert mock_clock.tick.call_count >= 2
    
    @patch('audio_player.pygame')
    def test_play_midi_file_keyboard_interrupt(self, mock_pygame):
        player = AudioPlayer()
        mock_pygame.mixer.music.get_busy.side_effect = KeyboardInterrupt()
        
        with pytest.raises(SystemExit):
            player.play_midi_file('test.mid')
        
        mock_pygame.mixer.music.fadeout.assert_called_once_with(1000)
        mock_pygame.mixer.music.stop.assert_called_once()
