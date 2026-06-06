import 'package:webdav_client/webdav_client.dart';
import 'package:flutter/foundation.dart';
import 'dart:typed_data';

class WebDAVService {
  Client? _client;
  String? _currentUrl;

  bool get isConnected => _client != null;

  Future<bool> connect(String url, {String? username, String? password}) async {
    try {
      _currentUrl = url;
      _client = newClient(
        url,
        user: username ?? '',
        password: password ?? '',
      );

      // Verify connection by listing root
      await _client!.readDir("/");
      return true;
    } catch (e) {
      debugPrint('WebDAV Connection Error: $e');
      _client = null;
      return false;
    }
  }

  Future<void> disconnect() async {
    _client = null;
    _currentUrl = null;
  }

  Future<List<File>> listFiles(String path) async {
    if (_client == null) throw Exception('Not connected to server');
    return await _client!.readDir(path);
  }

  Future<void> uploadFile(String remotePath, List<int> bytes) async {
    if (_client == null) throw Exception('Not connected to server');
    await _client!.write(remotePath, Uint8List.fromList(bytes));
  }

  Future<List<int>> downloadFile(String remotePath) async {
    if (_client == null) throw Exception('Not connected to server');
    return await _client!.read(remotePath);
  }

  String? get url => _currentUrl;
}
