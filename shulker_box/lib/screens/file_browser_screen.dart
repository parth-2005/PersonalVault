import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/app_state.dart';
import '../theme.dart';
import 'package:webdav_client/webdav_client.dart';
import 'package:file_picker/file_picker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:flutter/services.dart';
import 'dart:io' as io;
import 'package:path/path.dart' as p;

class FileBrowserScreen extends StatefulWidget {
  const FileBrowserScreen({super.key});

  @override
  State<FileBrowserScreen> createState() => _FileBrowserScreenState();
}

class _FileBrowserScreenState extends State<FileBrowserScreen> {
  String _currentPath = "/";
  List<File> _files = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadFiles();
  }

  Future<void> _loadFiles() async {
    setState(() => _isLoading = true);
    try {
      final state = Provider.of<AppState>(context, listen: false);
      final files = await state.webdavService.listFiles(_currentPath);
      setState(() {
        _files = files;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error loading files: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _navigateTo(String path) {
    setState(() => _currentPath = path);
    _loadFiles();
  }

  void _goBack() {
    if (_currentPath == "/") return;
    final parts = _currentPath.split('/').where((p) => p.isNotEmpty).toList();
    if (parts.isEmpty) {
      setState(() => _currentPath = "/");
    } else {
      parts.removeLast();
      setState(() => _currentPath = "/" + parts.join('/'));
    }
    _loadFiles();
  }

  Future<void> _downloadFile(File file) async {
    final state = Provider.of<AppState>(context, listen: false);
    try {
      final bytes = await state.webdavService.downloadFile('${_currentPath.endsWith('/') ? _currentPath : '$_currentPath/'}${file.name}');

      final directory = await getApplicationDocumentsDirectory();
      final filePath = '${directory.path}/${file.name}';
      final fileOnDisk = io.File(filePath);
      await fileOnDisk.writeAsBytes(bytes);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Downloaded to: $filePath')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Download failed: $e')),
      );
    }
  }

  Future<void> _uploadFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null) {
      PlatformFile file = result.files.first;
      if (file.path == null) return;

      final state = Provider.of<AppState>(context, listen: false);
      try {
        final bytes = await io.File(file.path!).readAsBytes();
        final remotePath = '${_currentPath.endsWith('/') ? _currentPath : '$_currentPath/'}${file.name}';
        await state.webdavService.uploadFile(remotePath, bytes);

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Uploaded ${file.name} successfully')),
        );
        _loadFiles();
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Upload failed: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = Provider.of<AppState>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(_currentPath, style: const TextStyle(fontFamily: 'JetBrains Mono')),
        leading: _currentPath != "/"
          ? IconButton(icon: const Icon(Icons.arrow_back), onPressed: _goBack)
          : null,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              state.disconnect();
            },
          ),
        ],
      ),
      body: _isLoading
        ? const Center(child: CircularProgressIndicator(color: AppColors.accent))
        : ListView.builder(
            itemCount: _files.length,
            itemBuilder: (context, index) {
              final file = _files[index];
              return ListTile(
                leading: Icon(
                  file.isDir == true ? Icons.folder : Icons.insert_drive_file,
                  color: file.isDir == true ? AppColors.accent : AppColors.textSecondary,
                ),
                title: Text(file.name ?? 'Unknown', style: const TextStyle(color: AppColors.textPrimary)),
                subtitle: Text(
                  file.isDir == true ? 'Folder' : '${(file.size ?? 0 / 1024).toStringAsFixed(2)} KB',
                  style: const TextStyle(color: AppColors.textSecondary),
                ),
                onTap: () {
                  if (file.isDir == true) {
                    _navigateTo('${_currentPath.endsWith('/') ? _currentPath : '$_currentPath/'}${file.name}');
                  } else {
                    _downloadFile(file);
                  }
                },
              );
            },
          ),
      floatingActionButton: FloatingActionButton(
        onPressed: _uploadFile,
        backgroundColor: AppColors.accent,
        foregroundColor: Colors.black,
        child: const Icon(Icons.upload),
      ),
    );
  }
}
