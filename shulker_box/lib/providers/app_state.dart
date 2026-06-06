import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/webdav_service.dart';

class AppState extends ChangeNotifier {
  final WebDAVService _webdavService = WebDAVService();
  WebDAVService get webdavService => _webdavService;

  bool _isConnected = false;
  bool get isConnected => _isConnected;

  Future<bool> connect(String url, {String? username, String? password}) async {
    _isConnected = await _webdavService.connect(url, username: username, password: password);
    notifyListeners();
    return _isConnected;
  }

  void disconnect() {
    _webdavService.disconnect();
    _isConnected = false;
    notifyListeners();
  }
}
