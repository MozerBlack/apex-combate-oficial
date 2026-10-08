#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$ROOT/.." && pwd)"
SDK_ROOT="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-/tmp/android-sdk}}"
PLATFORM="${APEX_ANDROID_PLATFORM:-33}"
BUILD_TOOLS_VERSION="${APEX_ANDROID_BUILD_TOOLS:-33.0.2}"
ANDROID_JAR="$SDK_ROOT/platforms/android-$PLATFORM/android.jar"
BUILD_TOOLS="$SDK_ROOT/build-tools/$BUILD_TOOLS_VERSION"
AAPT2="$BUILD_TOOLS/aapt2"
D8="$BUILD_TOOLS/d8"
ZIPALIGN="$BUILD_TOOLS/zipalign"
APKSIGNER="$BUILD_TOOLS/apksigner"
BUILD_DIR="$ROOT/build"
RELEASE_DIR="$PROJECT_ROOT/releases"
OUTPUT="$RELEASE_DIR/Apex-Combate-Demo-v44.apk"
SIGNING_KEY_PEM="${APEX_ANDROID_SIGNING_KEY_PEM:-$PROJECT_ROOT/deploy-keys/apex-combate-android-demo.key}"
SIGNING_KEY="${APEX_ANDROID_SIGNING_KEY:-$PROJECT_ROOT/deploy-keys/apex-combate-android-demo.pk8}"
SIGNING_CERT="${APEX_ANDROID_SIGNING_CERT:-$PROJECT_ROOT/deploy-keys/apex-combate-android-demo.pem}"

for required in "$ANDROID_JAR" "$AAPT2" "$D8" "$ZIPALIGN" "$APKSIGNER"; do
  if [[ ! -e "$required" ]]; then
    printf 'Ferramenta Android ausente: %s\n' "$required" >&2
    printf 'Defina ANDROID_SDK_ROOT para um SDK com platform-%s e build-tools %s.\n' "$PLATFORM" "$BUILD_TOOLS_VERSION" >&2
    exit 1
  fi
done
for required_command in java javac zip openssl awk sha256sum; do
  if ! command -v "$required_command" >/dev/null 2>&1; then
    printf 'Comando obrigatório ausente: %s\n' "$required_command" >&2
    exit 1
  fi
done

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/generated" "$BUILD_DIR/classes" "$BUILD_DIR/dex" "$RELEASE_DIR" "$(dirname "$SIGNING_KEY")"

"$AAPT2" compile --dir "$ROOT/src/main/res" -o "$BUILD_DIR/resources.zip"
"$AAPT2" link \
  -o "$BUILD_DIR/apex-unsigned.apk" \
  -I "$ANDROID_JAR" \
  --manifest "$ROOT/src/main/AndroidManifest.xml" \
  --java "$BUILD_DIR/generated" \
  --min-sdk-version 23 \
  --target-sdk-version 33 \
  --version-code 44 \
  --version-name 44.0-demo \
  "$BUILD_DIR/resources.zip"

mapfile -t JAVA_SOURCES < <(find "$ROOT/src/main/java" "$BUILD_DIR/generated" -name '*.java' -type f | sort)
javac -encoding UTF-8 -source 8 -target 8 -bootclasspath "$ANDROID_JAR" -d "$BUILD_DIR/classes" "${JAVA_SOURCES[@]}"
(
  cd "$BUILD_DIR/classes"
  zip -q -r "$BUILD_DIR/classes.jar" .
)
"$D8" --lib "$ANDROID_JAR" --min-api 23 --output "$BUILD_DIR/dex" "$BUILD_DIR/classes.jar"
(
  cd "$BUILD_DIR/dex"
  zip -q -j "$BUILD_DIR/apex-unsigned.apk" classes.dex
)
"$ZIPALIGN" -f -p 4 "$BUILD_DIR/apex-unsigned.apk" "$BUILD_DIR/apex-aligned.apk"

if [[ -f "$SIGNING_KEY_PEM" && ! -f "$SIGNING_CERT" ]] || [[ ! -f "$SIGNING_KEY_PEM" && -f "$SIGNING_CERT" ]]; then
  printf 'Assinatura Android incompleta. Restaure a chave e o certificado originais antes de gerar uma atualização.\n' >&2
  exit 1
fi
if [[ ! -f "$SIGNING_KEY_PEM" ]]; then
  openssl genpkey -algorithm RSA \
    -pkeyopt rsa_keygen_bits:3072 \
    -out "$SIGNING_KEY_PEM"
  openssl req -new -x509 -sha256 \
    -key "$SIGNING_KEY_PEM" \
    -out "$SIGNING_CERT" \
    -days 10000 \
    -subj "/C=BR/O=Apex Combate/OU=Mobile/CN=Apex Combate Demo"
fi
if [[ ! -f "$SIGNING_KEY" || "$SIGNING_KEY_PEM" -nt "$SIGNING_KEY" ]]; then
  openssl pkcs8 -topk8 -inform PEM -outform DER -nocrypt \
    -in "$SIGNING_KEY_PEM" \
    -out "$SIGNING_KEY"
fi
chmod 600 "$SIGNING_KEY_PEM" "$SIGNING_KEY" "$SIGNING_CERT"

"$APKSIGNER" sign \
  --v4-signing-enabled false \
  --key "$SIGNING_KEY" \
  --cert "$SIGNING_CERT" \
  --out "$OUTPUT" \
  "$BUILD_DIR/apex-aligned.apk"

"$APKSIGNER" verify --verbose --print-certs "$OUTPUT"
"$ZIPALIGN" -c -p 4 "$OUTPUT"
CHECKSUM="$(sha256sum "$OUTPUT" | awk '{print $1}')"
printf '%s  %s\n' "$CHECKSUM" "$(basename "$OUTPUT")" | tee "$OUTPUT.sha256"
printf '\nAPK gerado: %s\n' "$OUTPUT"
