# 🍒 Cherry Studio App（本仓库说明）

> 本 README 由本 fork 仓库维护（非上游内容），说明本仓库的定位与自动化机制。上游同步合并时若 README 冲突，以本版本为准。

## 这个仓库是干什么的？

**本仓库 = 上游 Cherry Studio Mobile 的"自动同步 + 自动编译"中转站。**

- **上游**：Cherry Studio Mobile（Expo / React Native 客户端，桌面版 Cherry Studio 的移动端）
- **本 fork 的职责**：通过 GitHub Actions **定时拉取上游最新代码**，并在有更新时**自动编译 Android APK**，把成品发布到 Releases 供下载。
- 分支：默认分支 `v0.2`，持续跟随上游 `v0.2`。

## 自动化是怎么运作的？

仓库里有 3 个 workflow（`.github/workflows/`）：

| Workflow | 触发方式 | 职责 |
|---|---|---|
| `sync-upstream.yml` | 定时 / 手动 | 把上游代码同步进本仓库（创建 merge 提交） |
| `build-apk.yml` | 定时（每天 00:10 / 12:10 北京时间）/ 手动 | 检查 12 小时内有无新提交 → 有新提交就编译 ARM64-v8a Release APK → 发布到 Releases |
| `cleanup-releases.yml` | 每周日 / 手动 | 清理 14 天前的 `build-*` 预发布（保留最新 5 个），避免 Releases 堆积 |

**编译产物去哪了？**

- 每次成功构建会在 **Releases** 页生成一个预发布（`build-YYYYMMDD-HHMMSS`），里面就是可安装的 APK；
- 同时会在 Actions 的 Artifacts 里留一份 7 天备份（防丢）。

**如何手动触发编译？**

1. 打开仓库 **Actions** 页；
2. 选择 **编译 APK (ARM64-v8a Release)**；
3. 点 **Run workflow** → 选 `v0.2` 分支 → 运行。

## 构建的关键信息

- **架构**：仅 ARM64-v8a（`-PreactNativeArchitectures=arm64-v8a`，兼顾体积与速度）
- **混淆**：R8 全量开启 + ProGuard 规则（`scripts/write_proguard.py`）
- **签名**：自定义密钥（来自仓库 Secrets：`SIGNING_KEYSTORE_BASE64` / `SIGNING_STORE_PASSWORD` / `SIGNING_KEY_ALIAS` / `SIGNING_KEY_PASSWORD`）
- **APK 体积优化**：`app.json` 中开启了 `android.useLegacyPackaging: true`（原生库 .so 在 APK 内压缩存储，减小 APK 体积）
- **编译加速**：`android/gradle.properties` 在 CI 中临时追加 `-Xmx4096m`、`org.gradle.parallel=true`、`org.gradle.caching=true`；Gradle 依赖走官方 `gradle/actions/setup-gradle` 缓存
- **构建时长**：约 20 分钟（首次冷缓存会稍久），超时上限 90 分钟

## 给贡献者的注意事项

1. **`android/`、`ios/` 目录不提交**（在 `.gitignore` 里），每次构建由 `expo prebuild --clean` 现场生成；
2. 改原生配置要改 `app.json` / `scripts/` 里的脚本，而不是改生成的 `android/`；
3. 依赖锁定：CI 使用 `pnpm install --frozen-lockfile`，改依赖请同步更新 `pnpm-lock.yaml`；
4. 构建失败会自动在本仓库建 Issue（需仓库开启 Issues）；
5. 上游升级若要求 JDK 21，把 `build-apk.yml` 里 `安装 Java 17` 的版本改成 21 即可。

## 常见问题（FAQ）

- **构建失败在哪看？** Actions 页 → 对应 run → 点进失败的步骤看日志。
- **APK 太大？** 已开 `.so` 压缩 + R8；如仍嫌大可在构建命令上去掉 `arm64-v8a` 限制前先评估多 ABI 需求。
- **想本地编译？** 见上游 README（`pnpm install && pnpm android`）。
