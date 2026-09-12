[app]
title = ROLEX AI
package.name = rolexai
package.domain = org.rolexai
source.dir = .
source.include_exts = py,json,txt,md,png,jpg,jpeg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.3.1,pypdf,python-docx,openpyxl,python-pptx
orientation = portrait
fullscreen = 0

# Native Android service used only when explicitly started by the app.
services = rolex_service:rolex_ai/android/service.py

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 34
android.minapi = 23
android.ndk = 25b
android.ndk_api = 23
android.archs = arm64-v8a
android.accept_sdk_license = True
# Use the stable python-for-android line with the Python 3.11 CI environment.
p4a.branch = master
# Keep native ML packages out of the APK unless a tested p4a recipe is added.
# Current vision/face adapters are optional and safely degrade when unavailable.
android.permissions = INTERNET,RECORD_AUDIO,CAMERA,USE_BIOMETRIC,POST_NOTIFICATIONS,SEND_SMS,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,FOREGROUND_SERVICE
android.allow_backup = False
android.uses_cleartext_traffic = False
source.exclude_dirs = tests,backups,rolex_upgrade,.git
