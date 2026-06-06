import 'package:flutter/material.dart';

class AppColors {
  static const Color background = Color(0xFF0D0D0D);
  static const Color backgroundSecondary = Color(0xFF0F1117);
  static const Color accent = Color(0xFFF5A623);
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFA1A1AA);
}

ThemeData shulkerBoxTheme = ThemeData(
  useMaterial3: true,
  brightness: Brightness.dark,
  colorScheme: ColorScheme.dark(
    surface: AppColors.background,
    onSurface: AppColors.textPrimary,
    primary: AppColors.accent,
    onPrimary: Colors.black,
    secondary: AppColors.backgroundSecondary,
    onSecondary: AppColors.textSecondary,
  ),
  scaffoldBackgroundColor: AppColors.background,
  textTheme: const TextTheme(
    headlineMedium: TextStyle(
      fontFamily: 'JetBrains Mono',
      fontWeight: FontWeight.bold,
      color: AppColors.textPrimary,
    ),
    bodyLarge: TextStyle(
      fontFamily: 'Inter',
      color: AppColors.textPrimary,
    ),
    bodyMedium: TextStyle(
      fontFamily: 'Inter',
      color: AppColors.textSecondary,
    ),
  ),
);
