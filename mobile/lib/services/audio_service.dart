import 'package:just_audio/just_audio.dart';
class CampusAudioService { final _player=AudioPlayer(); Stream<PlayerState> get state=>_player.playerStateStream; Future<void> toggle(String url) async { if (_player.playing) return _player.pause(); if (url.isNotEmpty) await _player.setUrl(url); await _player.play(); } Future<void> dispose()=>_player.dispose(); }
