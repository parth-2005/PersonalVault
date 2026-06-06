import 'package:workmanager/workmanager.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io' as io;
import 'package:webdav_client/webdav_client.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:typed_data';

@pragma('vm:entry-point')
void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    print("Native background task started: $task");

    try {
      // 1. Get credentials from SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      final url = prefs.getString('server_url');
      final username = prefs.getString('username');
      final password = prefs.getString('password');

      if (url == null) return Future.value(false);

      // 2. Connect to WebDAV
      final client = newClient(
        url,
        user: username ?? '',
        password: password ?? '',
      );

      // 3. Request storage permissions
      await Permission.storage.request();

      // 4. Find DCIM folder
      final directory = await getExternalStorageDirectory();
      if (directory == null) return Future.value(false);

      final dcimPath = '/storage/emulated/0/DCIM/Camera';
      final dcimDir = io.Directory(dcimPath);
      if (!dcimDir.existsSync()) return Future.value(false);

      // 5. Backup files (simplified: upload everything in Camera folder)
      final files = dcimDir.listSync();
      for (var entity in files) {
        if (entity is io.File) {
          final bytes = await entity.readAsBytes();
          await client.write('/backup/dcim/${entity.path.split('/').last}', Uint8List.fromList(bytes));
        }
      }
    } catch (e) {
      print("Backup Error: $e");
      return Future.value(false);
    }

    return Future.value(true);
  });
}

class BackupService {
  static Future<void> init() async {
    await Workmanager().initialize(callbackDispatcher, isInDebugMode: true);
  }

  static void scheduleBackup() {
    Workmanager().registerPeriodicTask(
      "1",
      "backupDCIM",
      frequency: Duration(hours: 12),
      constraints: Constraints(
        networkType: NetworkType.connected,
        requiresBatteryNotLow: true,
      ),
    );
  }
}
