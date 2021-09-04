import os
import sys
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ez_path = os.path.join(src_path, "EzAudioMeta")
sys.path.insert(0, ez_path)
from main import cli
from audio.base_audio import BaseAudio
