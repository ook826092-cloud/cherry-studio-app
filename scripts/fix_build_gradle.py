import re, os, base64, sys, glob

# 1. 解码签名文件
b64 = os.environ.get('KEYSTORE_B64', '')
with open('android/app/keystore.jks', 'wb') as f:
    f.write(base64.b64decode(b64))

# 2. 注入签名配置和 R8 到 build.gradle
with open('android/app/build.gradle', 'r') as f:
    c = f.read()

sb = '''
    signingConfigs {
        release {
            storeFile file('keystore.jks')
            storePassword System.getenv('SIGNING_STORE_PASSWORD')
            keyAlias System.getenv('SIGNING_KEY_ALIAS')
            keyPassword System.getenv('SIGNING_KEY_PASSWORD')
        }
    }
'''

c = re.sub(r'(android\s*\{)', r'\1' + sb, c)
c = re.sub(r'(buildTypes\s*\{.*?release\s*\{)',
    r'\1\n            minifyEnabled true\n            proguardFiles getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"\n            signingConfig signingConfigs.release',
    c, flags=re.DOTALL)

with open('android/app/build.gradle', 'w') as f:
    f.write(c)

# 3. 保留 react-native-nitro-healthkit，使用上游 patch 修复后的版本
#    （上游已在 patches/react-native-nitro-healthkit@1.0.0.patch 修复 Android 构建）
#    如果后续编译仍报错，可临时恢复下方排除逻辑

# 3a. 从 settings.gradle 移除（已注释）
# sg_path = 'android/settings.gradle'
# if os.path.exists(sg_path):
#     with open(sg_path, 'r') as f:
#         sg = f.read()
#     old_sg = sg
#     sg = re.sub(r'\n\s*include\s+[:\'"]react-native-nitro-healthkit[\'"]?.*', '', sg)
#     sg = re.sub(r'\n\s*project\([:\'"]react-native-nitro-healthkit[\'"]?\).*?(?:\n|$)', '', sg)
#     sg = re.sub(r'\n\s*.*nitro-healthkit.*projectDir.*', '', sg)
#     sg = re.sub(r'\n{2,}', '\n\n', sg)
#     if sg != old_sg:
#         with open(sg_path, 'w') as f:
#             f.write(sg)
#         print('✅ 已从 settings.gradle 移除 nitro-healthkit')

# 3b. 从 app/build.gradle 移除依赖（已注释）
# with open('android/app/build.gradle', 'r') as f:
#     abg = f.read()
# old_abg = abg
# abg = re.sub(r'\n\s*implementation\s+project\([:\'"]react-native-nitro-healthkit[\'"]?\)', '', abg)
# abg = re.sub(r'\n.*nitro-healthkit.*', '', abg)
# abg = re.sub(r'\n{2,}', '\n\n', abg)
# if abg != old_abg:
#     with open('android/app/build.gradle', 'w') as f:
#         f.write(abg)
#     print('✅ 已从 app/build.gradle 移除 nitro-healthkit 依赖')

# 3c. 移除 node_modules 中的安卓原生代码（已注释）
# target = os.path.join('node_modules', 'react-native-nitro-healthkit', 'android', 'build.gradle')
# if os.path.exists(target):
#     os.remove(target)
#     print('✅ 已移除 nitro-healthkit/android/build.gradle')
# target_dir = 'node_modules/react-native-nitro-healthkit/android'
# if os.path.exists(target_dir):
#     bak = target_dir + '_disabled'
#     if os.path.exists(bak):
#         import shutil as sh
#         sh.rmtree(bak)
#     os.rename(target_dir, bak)
#     print(f'✅ 已重命名 {target_dir} → android_disabled')

print('✅ 所有构建配置已完成')
