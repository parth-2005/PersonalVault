import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'theme.dart';
import 'providers/app_state.dart';
import 'screens/connection_screen.dart';
import 'screens/file_browser_screen.dart';
import 'package:receive_sharing_intent/receive_sharing_intent.dart';
import 'dart:async';
import 'dart:io';
import 'services/sharing_service.dart';
import 'services/backup_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize background backup service
  await BackupService.init();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
      ],
      child: const ShulkerBoxApp(),
    ),
  );
}

class ShulkerBoxApp extends StatefulWidget {
  const ShulkerBoxApp({super.key});

  @override
  State<ShulkerBoxApp> createState() => _ShulkerBoxAppState();
}

class _ShulkerBoxAppState extends State<ShulkerBoxApp> {
  StreamSubscription? _intentSub;

  @override
  void initState() {
    super.initState();
    _initSharing();
  }

  void _initSharing() {
    _intentSub = ReceiveSharingIntent.instance.getMediaStream().listen((List<SharedMediaFile> value) {
      if (!mounted) return;
      final state = Provider.of<AppState>(context, listen: false);
      SharingService.handleSharedFiles(state, value);
    }, onError: (err) {
      debugPrint('ReceiveSharingIntent error: $err');
    });

    ReceiveSharingIntent.instance.getInitialMedia().then((List<SharedMediaFile> value) {
      if (!mounted) return;
      final state = Provider.of<AppState>(context, listen: false);
      SharingService.handleSharedFiles(state, value);
    });
  }

  @override
  void dispose() {
    _intentSub?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ShulkerBox',
      theme: shulkerBoxTheme,
      home: Consumer<AppState>(
        builder: (context, state, child) {
          return state.isConnected
            ? const FileBrowserScreen()
            : const ConnectionScreen();
        },
      ),
      debugShowCheckedModeBanner: false,
    );
  }
}
