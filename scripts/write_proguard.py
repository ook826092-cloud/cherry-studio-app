rules = """-keep class com.facebook.react.** { *; }
-keep class com.facebook.hermes.** { *; }
-keep class com.facebook.jni.** { *; }
-keep class expo.** { *; }
-keep class com.facebook.hermes.unicode.** { *; }
-keepattributes *Annotation*
-keepclassmembers class * {
    @com.facebook.react.uimanager.annotations.ReactProp <methods>;
    @com.facebook.react.uimanager.annotations.ReactPropGroup <methods>;
}
-keep class * extends com.facebook.react.ReactPackage { *; }
-dontwarn com.facebook.hermes.**
-dontwarn com.facebook.jni.**
"""

with open('android/app/proguard-rules.pro', 'w') as f:
    f.write(rules)
print('OK')
