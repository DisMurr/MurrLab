#!/usr/bin/env python3
"""
Voice Dataset Manager - Download and integrate popular open-source voice datasets
"""

from pathlib import Path
import pandas as pd
from datasets import load_dataset
import torch
import torchaudio

class VoiceDatasetManager:
    def __init__(self, base_path="./voice_datasets"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.available_datasets = {
            "common_voice": {
                "name": "Mozilla Common Voice",
                "description": "Multilingual voice dataset",
                "languages": ["en", "es", "fr", "de", "it", "pt", "zh", "ja"],
                "size": "Large",
                "license": "CC0"
            },
            "librispeech": {
                "name": "LibriSpeech",
                "description": "English audiobook readings",
                "variants": ["clean", "other"],
                "size": "960 hours",
                "license": "CC BY 4.0"
            },
            "vctk": {
                "name": "VCTK Corpus",
                "description": "Multi-speaker English corpus",
                "speakers": 110,
                "size": "44 hours",
                "license": "CC BY 4.0"
            },
            "ljspeech": {
                "name": "LJ Speech",
                "description": "Single speaker (Linda Johnson)",
                "size": "24 hours",
                "license": "Public Domain"
            }
        }
    
    def list_datasets(self):
        """List all available datasets"""
        print("🗂️  Available Voice Datasets:")
        print("=" * 50)
        
        for key, info in self.available_datasets.items():
            print(f"\n📁 {info['name']} ({key})")
            print(f"   Description: {info['description']}")
            print(f"   Size: {info.get('size', 'Unknown')}")
            print(f"   License: {info.get('license', 'Unknown')}")
            
            if 'languages' in info:
                print(f"   Languages: {', '.join(info['languages'][:5])}")
            if 'speakers' in info:
                print(f"   Speakers: {info['speakers']}")
    
    def download_common_voice(self, language="en", split="train", max_samples=1000):
        """Download Mozilla Common Voice dataset"""
        print(f"📥 Downloading Common Voice ({language})...")
        
        try:
            dataset = load_dataset(
                "mozilla-foundation/common_voice_11_0", 
                language, 
                split=f"{split}[:{max_samples}]"
            )
            
            # Save metadata
            dataset_path = self.base_path / f"common_voice_{language}"
            dataset_path.mkdir(exist_ok=True)
            
            # Extract and save samples
            samples_info = []
            for i, sample in enumerate(dataset):
                if i >= max_samples:
                    break
                
                # Save audio
                audio_array = sample['audio']['array']
                sample_rate = sample['audio']['sampling_rate']
                
                audio_path = dataset_path / f"audio_{i:06d}.wav"
                torchaudio.save(str(audio_path), 
                              torch.tensor(audio_array).unsqueeze(0), 
                              sample_rate)
                
                # Collect metadata
                samples_info.append({
                    'file_path': str(audio_path),
                    'text': sample.get('sentence', ''),
                    'speaker_id': sample.get('client_id', ''),
                    'age': sample.get('age', ''),
                    'gender': sample.get('gender', ''),
                    'accent': sample.get('accent', ''),
                    'duration': len(audio_array) / sample_rate
                })
            
            # Save metadata CSV
            df = pd.DataFrame(samples_info)
            df.to_csv(dataset_path / "metadata.csv", index=False)
            
            print(f"✅ Downloaded {len(samples_info)} Common Voice samples")
            return dataset_path
            
        except Exception as e:
            print(f"❌ Error downloading Common Voice: {e}")
            return None
    
    def download_librispeech(self, variant="clean", split="train.clean.100", max_samples=500):
        """Download LibriSpeech dataset"""
        print(f"📥 Downloading LibriSpeech ({variant})...")
        
        try:
            dataset = load_dataset(
                "librispeech_asr", 
                variant, 
                split=f"{split}[:{max_samples}]"
            )
            
            dataset_path = self.base_path / f"librispeech_{variant}"
            dataset_path.mkdir(exist_ok=True)
            
            samples_info = []
            for i, sample in enumerate(dataset):
                if i >= max_samples:
                    break
                
                # Save audio
                audio_array = sample['audio']['array']
                sample_rate = sample['audio']['sampling_rate']
                
                audio_path = dataset_path / f"audio_{i:06d}.wav"
                torchaudio.save(str(audio_path), 
                              torch.tensor(audio_array).unsqueeze(0), 
                              sample_rate)
                
                samples_info.append({
                    'file_path': str(audio_path),
                    'text': sample['text'],
                    'speaker_id': sample['speaker_id'],
                    'chapter_id': sample['chapter_id'],
                    'id': sample['id'],
                    'duration': len(audio_array) / sample_rate
                })
            
            df = pd.DataFrame(samples_info)
            df.to_csv(dataset_path / "metadata.csv", index=False)
            
            print(f"✅ Downloaded {len(samples_info)} LibriSpeech samples")
            return dataset_path
            
        except Exception as e:
            print(f"❌ Error downloading LibriSpeech: {e}")
            return None
    
    def download_ljspeech(self):
        """Download LJ Speech dataset (subset)"""
        print("📥 Downloading LJ Speech dataset...")
        
        try:
            dataset = load_dataset("lj_speech", split="train[:500]")
            
            dataset_path = self.base_path / "ljspeech"
            dataset_path.mkdir(exist_ok=True)
            
            samples_info = []
            for i, sample in enumerate(dataset):
                # Save audio
                audio_array = sample['audio']['array']
                sample_rate = sample['audio']['sampling_rate']
                
                audio_path = dataset_path / f"audio_{i:06d}.wav"
                torchaudio.save(str(audio_path), 
                              torch.tensor(audio_array).unsqueeze(0), 
                              sample_rate)
                
                samples_info.append({
                    'file_path': str(audio_path),
                    'text': sample['text'],
                    'normalized_text': sample['normalized_text'],
                    'id': sample['id'],
                    'duration': len(audio_array) / sample_rate
                })
            
            df = pd.DataFrame(samples_info)
            df.to_csv(dataset_path / "metadata.csv", index=False)
            
            print(f"✅ Downloaded {len(samples_info)} LJ Speech samples")
            return dataset_path
            
        except Exception as e:
            print(f"❌ Error downloading LJ Speech: {e}")
            return None
    
    def analyze_dataset(self, dataset_path):
        """Analyze downloaded dataset"""
        dataset_path = Path(dataset_path)
        metadata_file = dataset_path / "metadata.csv"
        
        if not metadata_file.exists():
            print("❌ No metadata.csv found in the dataset folder")
            return
        
        df = pd.read_csv(metadata_file)
        
        print(f"\n📊 Dataset Analysis: {dataset_path.name}")
        print("=" * 50)
        print(f"Total samples: {len(df)}")
        print(f"Total duration: {df['duration'].sum():.2f} seconds ({df['duration'].sum()/3600:.2f} hours)")
        print(f"Average duration: {df['duration'].mean():.2f} seconds")
        print(f"Min duration: {df['duration'].min():.2f} seconds")
        print(f"Max duration: {df['duration'].max():.2f} seconds")
        
        if 'speaker_id' in df.columns:
            print(f"Unique speakers: {df['speaker_id'].nunique()}")
        
        if 'gender' in df.columns:
            gender_dist = df['gender'].value_counts()
            print("\nGender distribution:")
            for gender, count in gender_dist.items():
                print(f"  {gender}: {count}")
        
        # Text length analysis
        if 'text' in df.columns:
            df['text_length'] = df['text'].astype(str).str.len()
            print(f"\nText length (chars) avg: {df['text_length'].mean():.1f}")
    
    def create_training_splits(self, dataset_path, train_ratio=0.8, val_ratio=0.1):
        """Create train/validation/test splits"""
        dataset_path = Path(dataset_path)
        metadata_file = dataset_path / "metadata.csv"
        
        if not metadata_file.exists():
            print("❌ No metadata.csv found in the dataset folder")
            return
        
        df = pd.read_csv(metadata_file)
        
        # Shuffle dataset
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        n_samples = len(df)
        n_train = int(n_samples * train_ratio)
        n_val = int(n_samples * val_ratio)
        
        # Split
        train_df = df[:n_train]
        val_df = df[n_train:n_train+n_val]
        test_df = df[n_train+n_val:]
        
        # Save splits
        train_df.to_csv(dataset_path / "train.csv", index=False)
        val_df.to_csv(dataset_path / "validation.csv", index=False)
        test_df.to_csv(dataset_path / "test.csv", index=False)
        
        print(f"✅ Created data splits:")
        print(f"  Train: {len(train_df)} samples")
        print(f"  Validation: {len(val_df)} samples")
        print(f"  Test: {len(test_df)} samples")

def main():
    """Download and setup voice datasets"""
    manager = VoiceDatasetManager()
    
    print("🎭 Voice Dataset Manager")
    print("=" * 50)
    
    # List available datasets
    manager.list_datasets()
    
    print("\n📥 Starting downloads...")
    
    # Download datasets
    datasets_downloaded = []
    
    # Common Voice (English)
    cv_path = manager.download_common_voice("en", max_samples=200)
    if cv_path:
        datasets_downloaded.append(cv_path)
        manager.analyze_dataset(cv_path)
        manager.create_training_splits(cv_path)
    
    # LibriSpeech
    ls_path = manager.download_librispeech(max_samples=100)
    if ls_path:
        datasets_downloaded.append(ls_path)
        manager.analyze_dataset(ls_path)
        manager.create_training_splits(ls_path)
    
    # LJ Speech
    lj_path = manager.download_ljspeech()
    if lj_path:
        datasets_downloaded.append(lj_path)
        manager.analyze_dataset(lj_path)
        manager.create_training_splits(lj_path)
    
    print(f"\n✅ Successfully downloaded {len(datasets_downloaded)} datasets!")
    print("📁 Datasets saved in: ./voice_datasets/")
    
    return datasets_downloaded

if __name__ == "__main__":
    main()
