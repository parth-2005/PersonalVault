import 'dart:async';
import 'package:flutter/material.dart';
import 'package:receive_sharing_intent/receive_sharing_intent.dart';
import '../providers/app_state.dart';
import '../theme.dart';
import 'dart:io';

class SharingService {
  static Future<void> handleSharedFiles(AppState state, List<SharedMediaFile> files) async {
    if (!state.isConnected) {
      // We can't use ScaffoldMessenger here since we are in a service
      // In a real app, we'd use a global key for the scaffold
      return;
    }

    for (var file in files) {
      if (file.path != null) {
        try {
          final bytes = await File(file.path!).readAsBytes();
          final fileName = file.path!.split('/').last;
          await state.webdavService.uploadFile('/$fileName', bytes);
        } catch (e) {
          debugPrint('Error uploading shared file: $e');
        }
      }
    }
  }
}
