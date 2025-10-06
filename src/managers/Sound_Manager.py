import os
import sys

import glob
from typing import Dict, Optional

from PyQt5.QtCore import QUrl, QSettings
from PyQt5.QtMultimedia import QSoundEffect, QMediaPlayer, QMediaContent

# Project Imports
from managers.Resource_Manager import get_external_resource
from managers.Debug_Manager import debug

# ===================================================================
# Globals
# ===================================================================
_EFFECTS: Dict[str, QSoundEffect] = {}
_INITIALIZED = False

_bgm_player: Optional[QMediaPlayer] = None
_sfx_muted: bool = False
_bgm_muted: bool = False

_loop_current: bool = True      # default = loop the current track
_loop_all: bool = False         # default = don’t loop all
_current_track_index: int = 0   # keeps track of position in folder
_current_folder: Optional[str] = None

# ===================================================================
# Settings helpers
# ===================================================================
# Fetch the settings
def _get_settings() -> QSettings:
    return QSettings(get_external_resource("Settings.ini"), QSettings.IniFormat)

# Check if sound should be played
def should_play_sounds() -> bool:
    return not _sfx_muted

# Check if bgm should be played
def is_bgm_muted() -> bool:
    return _bgm_muted

# Return saved SFX volume 0 – 100
def get_volume() -> float:
    settings = _get_settings()
    vol_int = settings.value("sfx_volume", 80, type=int)
    return max(0, min(100, vol_int)) / 100.0


# ===================================================================
# SFX mute/volume
# ===================================================================

# Mute/unmute all sound effects and persist settings
def set_sfx_muted(muted: bool):
    global _sfx_muted
    _sfx_muted = muted
    debug.debug("SFX mute state set to: %s", muted)

    settings = _get_settings()
    settings.setValue("disable_sounds", muted)
    debug.debug("Persisted 'disable_sounds' = %s to settings", muted)

    for eff in _EFFECTS.values():
        eff.setMuted(muted)

# Set volume for all SFX and persist to settings
def set_volume_for_all(volume: float):
    vol_int = int(volume * 100)
    debug.debug("Setting global SFX volume to: %d%%", vol_int)

    settings = _get_settings()
    settings.setValue("sfx_volume", vol_int)

    for eff in _EFFECTS.values():
        eff.setVolume(volume)


# ===================================================================
# BGM management
# ===================================================================

# Get available songs in the BGM folder
def get_available_bgm_tracks(folder: str) -> list:
    full_path = get_external_resource(folder)
    if not os.path.exists(full_path):
        debug.error("BGM folder not found: %s", full_path)
        return []

    # Determine which extensions to use based on platform
    if sys.platform == "win32":
        exts = ("*.mp3", "*.wav")  # Windows only supports mp3/wav reliably
    else:
        exts = ("*.ogg",)          # Linux/macOS can use ogg

    tracks = []
    for ext in exts:
        tracks.extend(glob.glob(os.path.join(full_path, ext)))

    # Return filenames only (not full paths)
    return [os.path.basename(t) for t in tracks]


# Play a specific track by name (from folder)
def play_bgm_track(folder: str, track_name: str, loop: Optional[bool] = None):
    global _bgm_player, _current_folder, _current_track_index
    if _bgm_player is None:
        debug.debug("Initializing BGM player...")
        _bgm_player = QMediaPlayer()
        _bgm_player.setVolume(_get_settings().value("bgm_volume", 80, type=int))
        _bgm_player.setMuted(_bgm_muted)

    tracks = get_available_bgm_tracks(folder)
    if track_name not in tracks:
        debug.error("Requested BGM track '%s' not found in %s", track_name, folder)
        return

    _current_folder = folder
    _current_track_index = tracks.index(track_name)

    full_path = get_external_resource(os.path.join(folder, track_name))
    if os.path.exists(full_path):
        debug.info("Playing BGM track: %s", full_path)
        _bgm_player.setMedia(QMediaContent(QUrl.fromLocalFile(full_path)))
        _bgm_player.play()

        # Save chosen track to settings
        settings = _get_settings()
        settings.setValue("bgm_track", track_name)

        # Decide whether to loop based on explicit argument or stored settings
        effective_loop = _loop_current or _loop_all if loop is None else loop
        if effective_loop:
            try:
                _bgm_player.mediaStatusChanged.disconnect(_restart_if_finished)
            except Exception:
                pass
            _bgm_player.mediaStatusChanged.connect(_restart_if_finished)
    else:
        debug.error("BGM track not found: %s", full_path)


# Method which stops the bgm
def stop_bgm():
    if _bgm_player:
        debug.debug("Stopping BGM")
        _bgm_player.stop()

# Method which loops the bgm (can be set to loops at speical times)
def _restart_if_finished(status):
    global _current_track_index
    if status == QMediaPlayer.EndOfMedia:
        if _loop_current:
            debug.debug("Restarting current BGM track (loop current)")
            _bgm_player.setPosition(0)
            _bgm_player.play()
        elif _loop_all and _current_folder:
            tracks = get_available_bgm_tracks(_current_folder)
            if tracks:
                _current_track_index = (_current_track_index + 1) % len(tracks)
                next_track = tracks[_current_track_index]
                debug.debug("Looping to next BGM track: %s", next_track)
                play_bgm_track(_current_folder, next_track, loop=True)



# Method for setting the volume
def set_bgm_volume(value: float):
    vol_int = int(value * 100)
    debug.debug("Setting BGM volume to: %d%%", vol_int)

    if _bgm_player:
        _bgm_player.setVolume(vol_int)

    settings = _get_settings()
    settings.setValue("bgm_volume", vol_int)

# Mute/unmute background music and persist setting.
def set_bgm_muted(muted: bool):
    global _bgm_muted
    _bgm_muted = muted
    debug.debug("BGM mute state set to: %s", muted)

    if _bgm_player:
        _bgm_player.setMuted(muted)
        if not muted and _bgm_player.state() != QMediaPlayer.PlayingState:
            # Resume last played track
            settings = _get_settings()
            last_track = settings.value("bgm_track", "", type=str)
            if last_track:
                debug.debug("Resuming BGM with last track: %s", last_track)
                play_bgm_track("Music", last_track, loop=True)
            else:
                debug.warning("No last BGM track found to resume after unmute")
        elif muted:
            debug.debug("BGM muted (staying stopped or paused)")

    settings = _get_settings()
    settings.setValue("disable_bgm", muted)


# ===================================================================
# Loop settings
# ===================================================================

# Loop Current Toggle Handler
def handle_loop_current_toggle(settings: QSettings, controls: dict, current_enabled: bool):
    settings.setValue("loop_current", current_enabled)
    debug.debug("Saved 'loop_current' = %s to settings", current_enabled)

    # Disable loop all if loop current is on
    if "loop_all" in controls and "checkbox" in controls["loop_all"]:
        controls["loop_all"]["checkbox"].setEnabled(not current_enabled)
        if current_enabled:
            controls["loop_all"]["checkbox"].setChecked(False)
            settings.setValue("loop_all", False)
        debug.debug("Loop All checkbox %s", "disabled" if current_enabled else "enabled")

    # Call into Sound_Manager
    set_loop_current(current_enabled)

# Loop All Toggle Handler
def handle_loop_all_toggle(settings: QSettings, controls: dict, all_enabled: bool):
    settings.setValue("loop_all", all_enabled)
    debug.debug("Saved 'loop_all' = %s to settings", all_enabled)

    # Disable loop current if loop all is on
    if "loop_current" in controls and "checkbox" in controls["loop_current"]:
        controls["loop_current"]["checkbox"].setEnabled(not all_enabled)
        if all_enabled:
            controls["loop_current"]["checkbox"].setChecked(False)
            settings.setValue("loop_current", False)
        debug.debug("Loop Current checkbox %s", "disabled" if all_enabled else "enabled")

    # Call into Sound_Manager
    set_loop_all(all_enabled)

def set_loop_current(enabled: bool):
    global _loop_current, _loop_all
    _loop_current = enabled
    if enabled:
        _loop_all = False  # ensure exclusivity
    debug.debug("Loop current track set to: %s (loop_all=%s)", _loop_current, _loop_all)

    settings = _get_settings()
    settings.setValue("loop_current", _loop_current)
    settings.setValue("loop_all", _loop_all)


def set_loop_all(enabled: bool):
    global _loop_all, _loop_current
    _loop_all = enabled
    if enabled:
        _loop_current = False  # ensure exclusivity
    debug.debug("Loop all tracks set to: %s (loop_current=%s)", _loop_all, _loop_current)

    settings = _get_settings()
    settings.setValue("loop_all", _loop_all)
    settings.setValue("loop_current", _loop_current)

# ===================================================================
# SFX initialization and play
# ===================================================================
def _load_sound(effect: QSoundEffect, relative_path: str, label: str):
    full_path = get_external_resource(relative_path)
    if os.path.exists(full_path):
        debug.debug("Loading sound effect '%s' from: %s", label, full_path)
        effect.setSource(QUrl.fromLocalFile(full_path))
    else:
        debug.error("Sound effect '%s' not found: %s", label, full_path)


def _ensure_initialized():
    global _INITIALIZED
    if _INITIALIZED:
        return
    debug.debug("Initializing sound effects...")

    def make(label: str, rel: str) -> QSoundEffect:
        eff = QSoundEffect()
        eff.setVolume(get_volume())
        eff.setMuted(_sfx_muted)
        _load_sound(eff, rel, label)
        return eff

    _EFFECTS["menu_open"]         = make("Menu open",         "Audio/Effects/Menu_Open_Sound.wav")
    _EFFECTS["menu_cancel"]       = make("Menu cancel",       "Audio/Effects/Menu_Cancel_Sound.wav")
    _EFFECTS["menu_select"]       = make("Menu select",       "Audio/Effects/Menu_Select_Sound.wav")
    _EFFECTS["menu_failed"]       = make("Menu failed",       "Audio/Effects/Menu_Failed_Sound.wav")
    _EFFECTS["menu_save_popup"]        = make("Menu save_popup",        "Audio/Effects/Menu_Save_Popup.wav")
    _EFFECTS["menu_save_complete"]        = make("Menu save_complete",        "Audio/Effects/Menu_Save_Complete.wav")
    _EFFECTS["menu_message_skip"] = make("Menu message_skip", "Audio/Effects/Menu_Message_Skip.wav")
    _EFFECTS["menu_cursor_move"]  = make("Menu cursor_move",  "Audio/Effects/Menu_Cursor_Move.wav")
    _EFFECTS["menu_about_open"]   = make("Menu about_open",   "Audio/Effects/Menu_About_Open.wav")
    _EFFECTS["menu_about_close"]  = make("Menu about_close",  "Audio/Effects/Menu_About_Close.wav")
    _EFFECTS["menu_theme_switch"]  = make("Menu theme_switch",  "Audio/Effects/Menu_Theme_Switch.wav")
    _EFFECTS["menu_theme_save"]  = make("Menu theme_save",  "Audio/Effects/Menu_Theme_Save.wav")
    
    debug.info("Sound effects initialized: %s", list(_EFFECTS.keys()))
    _INITIALIZED = True


def get_effect(name: str) -> Optional[QSoundEffect]:
    _ensure_initialized()
    return _EFFECTS.get(name)


def play_sound_by_name(name: str):
    eff = get_effect(name)
    if eff:
        try:
            eff.play()
            debug.info("Playing sound effect: %s", name)
        except Exception as e:
            debug.error("Failed to play sound '%s': %s", name, e)
    else:
        debug.warning("Requested sound '%s' not loaded", name)


# ===================================================================
# Load saved settings immediately
# ===================================================================
def _load_initial_settings():
    global _bgm_muted, _sfx_muted, _loop_current, _loop_all
    settings = _get_settings()

    _sfx_muted = settings.value("disable_sounds", False, type=bool)
    _bgm_muted = settings.value("disable_bgm", False, type=bool)
    _loop_current = settings.value("loop_current", True, type=bool)
    _loop_all = settings.value("loop_all", False, type=bool)
    
    debug.debug(
    "Initial settings loaded: disable_sounds=%s, disable_bgm=%s, loop_current=%s, loop_all=%s", _sfx_muted, _bgm_muted, _loop_current, _loop_all)

_load_initial_settings()