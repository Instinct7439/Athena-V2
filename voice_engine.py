# voice_engine.py - Free Voice Engine for Athena (Python 3.12 compatible)
# Uses: Whisper (local) + gTTS (Google TTS - requires internet for TTS only)

import whisper
from gtts import gTTS
import tempfile
import os
from pathlib import Path


class AthenaVoice:
    """
    Free voice interface compatible with Python 3.12+
    - Speech-to-Text: Whisper (local, offline)
    - Text-to-Speech: gTTS (online, free, natural voice)
    """
    
    def __init__(self, whisper_model="base", tts_lang='en'):
        """Initialize voice engine"""
        self.whisper_model_name = whisper_model
        self.tts_lang = tts_lang
        self.whisper_model = None
        
        print(f"🎙️ Initializing Athena Voice Engine...")
        self._initialize_whisper()
        print(f"   ✅ Voice engine ready!")
    
    def _initialize_whisper(self):
        """Load Whisper model for speech recognition"""
        try:
            print(f"   📥 Loading Whisper '{self.whisper_model_name}' model...")
            self.whisper_model = whisper.load_model(self.whisper_model_name)
            print(f"   ✅ Whisper ready (offline)")
        except Exception as e:
            print(f"   ❌ Error loading Whisper: {e}")
            raise
    
    def transcribe_audio(self, audio_file_path: str, language='en') -> dict:
        """Convert speech to text using Whisper (offline)"""
        try:
            print(f"🎤 Transcribing audio: {Path(audio_file_path).name}")
            result = self.whisper_model.transcribe(
                audio_file_path,
                fp16=False,
                language=language if language != 'auto' else None,
                task='transcribe',
                verbose=False
            )
            
            text = result["text"].strip()
            detected_language = result.get("language", language)
            
            # Confidence calculation
            segments = result.get("segments", [])
            if segments:
                avg_confidence = sum(s.get("no_speech_prob", 0) for s in segments) / len(segments)
                confidence = 1 - avg_confidence
            else:
                confidence = 1.0
            
            print(f"   ✅ Transcribed: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            print(f"   📊 Language: {detected_language}, Confidence: {confidence:.0%}")
            
            return {
                'text': text,
                'language': detected_language,
                'confidence': confidence,
                'success': True
            }
            
        except Exception as e:
            print(f"   ❌ Transcription error: {e}")
            return {
                'text': '',
                'language': 'unknown',
                'confidence': 0.0,
                'success': False,
                'error': str(e)
            }
    
    def speak(self, text: str, output_file: str = None, slow: bool = False) -> str:
        """Convert text to speech using gTTS (requires internet)"""
        try:
            print(f"🔊 Generating speech with Google TTS...")
            print(f"   Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            
            if output_file is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                output_file = temp_file.name
                temp_file.close()
            
            tts = gTTS(text=text, lang=self.tts_lang, slow=slow)
            tts.save(output_file)
            
            print(f"   ✅ Audio generated")
            print(f"   💾 Saved to: {output_file}")
            
            return output_file
            
        except Exception as e:
            print(f"   ❌ TTS error: {e}")
            print(f"   💡 Make sure you have internet connection for TTS")
            return None


# =====================================================================
# 🧪 TEST SUITE
# =====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 ATHENA VOICE ENGINE TEST (gTTS + Whisper)")
    print("=" * 70)
    
    print(f"\n📌 Python version: {os.sys.version}")
    
    # Initialize
    print("\n1️⃣ Initializing voice engine...")
    try:
        voice = AthenaVoice(whisper_model="tiny")  # use tiny for quick tests
        print("   ✅ Initialization successful!\n")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print("   💡 Install dependencies: pip install openai-whisper gtts")
        os.sys.exit(1)
    
    # 2️⃣ TTS Test
    print("2️⃣ Testing Text-to-Speech (requires internet)...")
    try:
        texts = [
            "Hello Sagar! This is Athena speaking.",
            "Testing the voice engine with Google Text-to-Speech."
        ]
        for i, t in enumerate(texts, 1):
            out = f"test_athena_{i}.mp3"
            res = voice.speak(t, out)
            if res:
                print(f"   ✅ Saved as: {out}")
            else:
                print(f"   ❌ Failed TTS for test {i}")
    except Exception as e:
        print(f"   ❌ TTS test failed: {e}")
    
    # 3️⃣ Transcription Test
    print("\n3️⃣ Testing Speech-to-Text (offline)...")
    import sys
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        if not os.path.isabs(audio_file):
            audio_file = os.path.join(os.path.dirname(__file__), audio_file)
        
        print(f"   Testing with: {audio_file}")
        if not os.path.exists(audio_file):
            print(f"   ❌ File not found at: {audio_file}")
        else:
            result = voice.transcribe_audio(audio_file)
            if result['success']:
                print(f"\n   📝 Transcription:")
                print(f"      Text: {result['text']}")
                print(f"      Language: {result['language']}")
                print(f"      Confidence: {result['confidence']:.0%}")
            else:
                print(f"   ❌ Failed: {result.get('error')}")
    else:
        print("   ℹ️  Skipped (provide audio file as argument)")
        print("   Usage: python voice_engine.py test.wav")
    
    print("\n" + "=" * 70)
    print("✅ TESTS COMPLETE!")
    print("=" * 70)
    
    print("\n📊 Voice Engine Features:")
    print("   🎤 Transcription: Offline (Whisper)")
    print("   🔊 Speech: Online (gTTS)")
    print("   🆓 Cost: 100% Free")
    print("   ⭐ Quality: ⭐⭐⭐⭐ (Natural Google voice)")
    
    print("\n💡 Pros:")
    print("   ✅ Works with Python 3.12+")
    print("   ✅ Natural-sounding voice")
    print("   ✅ Easy to use")
    print("   ✅ 100% free")
    
    print("\n⚠️  Note:")
    print("   - TTS requires internet connection")
    print("   - Transcription works offline")
    
    print("\n🎯 Next steps:")
    print("   1. Test: python voice_engine.py test.wav")
    print("   2. Integrate into Streamlit")
    print("   3. Add voice tab to app.py")
