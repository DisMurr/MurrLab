# pyright: reportMissingImports=false
import pytest
from unittest.mock import patch, MagicMock
import torch
import numpy as np

from src.murr.tts import punc_norm, MurrTTS, Conditionals, T3Cond

@pytest.fixture
def mock_models():
    with patch('src.murr.tts.T3') as mock_t3, \
         patch('src.murr.tts.S3Gen') as mock_s3gen, \
         patch('src.murr.tts.VoiceEncoder') as mock_ve, \
         patch('src.murr.tts.EnTokenizer') as mock_tokenizer:
        
        mock_t3_instance = MagicMock()
        mock_t3_instance.hp.speech_cond_prompt_len = 150
        mock_t3_instance.hp.start_text_token = 0
        mock_t3_instance.hp.stop_text_token = 1
        mock_t3.return_value = mock_t3_instance

        mock_s3gen_instance = MagicMock()
        mock_s3gen_instance.tokenizer = MagicMock()
        mock_s3gen.return_value = mock_s3gen_instance
        
        yield {
            "t3": mock_t3,
            "s3gen": mock_s3gen,
            "ve": mock_ve,
            "tokenizer": mock_tokenizer,
            "t3_instance": mock_t3_instance,
            "s3gen_instance": mock_s3gen_instance,
            "ve_instance": mock_ve.return_value,
            "tokenizer_instance": mock_tokenizer.return_value
        }

@pytest.fixture
def tts_instance(mock_models):
    return MurrTTS(
        t3=mock_models["t3_instance"],
        s3gen=mock_models["s3gen_instance"],
        ve=mock_models["ve_instance"],
        tokenizer=mock_models["tokenizer_instance"],
        device="cpu"
    )

# Tests for punc_norm
def test_punc_norm_empty_string():
    assert punc_norm("") == "You need to add some text for me to talk."

def test_punc_norm_capitalization():
    assert punc_norm("hello world.") == "Hello world."

def test_punc_norm_multiple_spaces():
    assert punc_norm("Hello   world.") == "Hello world."

def test_punc_norm_replace_punc():
    assert punc_norm("Hello... world:") == "Hello,  world,"
    assert punc_norm("Hello… world;") == "Hello,  world,"

def test_punc_norm_add_full_stop():
    assert punc_norm("Hello world") == "Hello world."

def test_punc_norm_no_change():
    assert punc_norm("Hello world.") == "Hello world."

# Tests for MurrTTS
@patch('src.murr.tts.hf_hub_download')
@patch('src.murr.tts.MurrTTS.from_local')
def test_from_pretrained(mock_from_local, mock_hf_hub_download):
    MurrTTS.from_pretrained(device="cpu")
    mock_hf_hub_download.assert_called()
    mock_from_local.assert_called()

@patch('src.murr.tts.librosa.load')
def test_prepare_conditionals(mock_librosa_load, tts_instance, mock_models):
    mock_librosa_load.return_value = (np.random.rand(16000 * 10), 16000)
    mock_models["ve_instance"].embeds_from_wavs.return_value = np.random.rand(1, 256)
    
    tts_instance.prepare_conditionals("dummy.wav")
    
    assert tts_instance.conds is not None
    assert isinstance(tts_instance.conds, Conditionals)
    assert isinstance(tts_instance.conds.t3, T3Cond)
    mock_librosa_load.assert_called_with("dummy.wav", sr=48000)
    mock_models["ve_instance"].embeds_from_wavs.assert_called()

def test_generate_no_prompt(tts_instance):
    with pytest.raises(AssertionError, match="Please `prepare_conditionals` first or specify `audio_prompt_path`"):
        tts_instance.generate("test text")

@patch('src.murr.tts.librosa.load')
def test_generate_with_audio_prompt(mock_librosa_load, tts_instance, mock_models):
    # Mock dependencies for prepare_conditionals
    mock_librosa_load.return_value = (np.random.rand(48000 * 10), 48000)
    mock_models["ve_instance"].embeds_from_wavs.return_value = np.random.rand(1, 256)
    mock_models["s3gen_instance"].embed_ref.return_value = {}

    # Mock dependencies for generate
    mock_models["tokenizer_instance"].text_to_tokens.return_value = torch.tensor([[1, 2, 3]])
    mock_models["t3_instance"].inference.return_value = torch.tensor([[4, 5, 6]])
    mock_models["s3gen_instance"].inference.return_value = (torch.tensor([[[0.1, 0.2, 0.3]]]), 48000)

    wav = tts_instance.generate("test text", audio_prompt_path="dummy.wav")

    assert isinstance(wav, torch.Tensor)
    assert wav.shape == (1, 3)
    mock_models["tokenizer_instance"].text_to_tokens.assert_called_with("Test text.")
    mock_models["t3_instance"].inference.assert_called()
    mock_models["s3gen_instance"].inference.assert_called()


def test_generate_with_prepared_conditionals(tts_instance, mock_models):
    # Mock dependencies for generate
    mock_models["tokenizer_instance"].text_to_tokens.return_value = torch.tensor([[1, 2, 3]])
    mock_models["t3_instance"].inference.return_value = torch.tensor([[4, 5, 6]])
    mock_models["s3gen_instance"].inference.return_value = (torch.tensor([[[0.1, 0.2, 0.3]]]), 48000)

    # Manually set conditionals
    tts_instance.conds = Conditionals(
        t3=T3Cond(speaker_emb=torch.rand(1, 256)),
        gen={}
    )

    wav = tts_instance.generate("test text")

    assert isinstance(wav, torch.Tensor)
    assert wav.shape == (1, 3)
    mock_models["tokenizer_instance"].text_to_tokens.assert_called_with("Test text.")
    mock_models["t3_instance"].inference.assert_called()
    mock_models["s3gen_instance"].inference.assert_called()
