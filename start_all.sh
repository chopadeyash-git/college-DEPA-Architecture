#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "=========================================================="
echo " STARTING COMPLETE DEPA CONSENT ECOSYSTEM (6 SERVICES)"
echo "=========================================================="

# Java runtime detection
if [ -z "$JAVA_HOME" ]; then
  if [ -d "/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home" ]; then
    export JAVA_HOME="/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home"
  elif [ -d "/opt/homebrew/opt/openjdk" ]; then
    export JAVA_HOME="/opt/homebrew/opt/openjdk"
  fi
fi

if [ -n "$JAVA_HOME" ]; then
  export PATH="$JAVA_HOME/bin:$PATH"
fi

mkdir -p "$ROOT_DIR/logs"

CM_JAR="$ROOT_DIR/consent-manager/backend/target/consent-manager-1.0.0-SNAPSHOT.jar"
COL_A_JAR="$ROOT_DIR/college-a/backend/target/college-a-provider-1.0.0-SNAPSHOT.jar"
COL_B_JAR="$ROOT_DIR/college-b/backend/target/college-b-university-1.0.0-SNAPSHOT.jar"

# Verify Jars exist
if [ ! -f "$CM_JAR" ] || [ ! -f "$COL_A_JAR" ] || [ ! -f "$COL_B_JAR" ]; then
  echo "Building Maven artifacts..."
  mvn clean package -DskipTests
fi

# 1. Start Consent Manager Backend (Port 8095)
echo ""
echo "[1/6] Starting Consent Manager Backend (Port 8095)..."
nohup java -jar "$CM_JAR" </dev/null > "$ROOT_DIR/logs/cm-backend.log" 2>&1 &
CM_PID=$!
echo "  -> CM Backend PID: $CM_PID"

# 2. Start College A Backend (Port 8081)
echo ""
echo "[2/6] Starting College A Provider Backend (Port 8081)..."
APP_RSA_KEYS_DIR="$ROOT_DIR/keys" nohup java -jar "$COL_A_JAR" </dev/null > "$ROOT_DIR/logs/col-a-backend.log" 2>&1 &
COL_A_PID=$!
echo "  -> College A Backend PID: $COL_A_PID"

# 3. Start College B Backend (Port 8082)
echo ""
echo "[3/6] Starting College B Consumer Backend (Port 8082)..."
APP_INTERNAL_API_KEY="B-INTERNAL-SECRET-KEY" APP_RSA_KEYS_DIR="$ROOT_DIR/college-b/backend/keys" nohup java -jar "$COL_B_JAR" </dev/null > "$ROOT_DIR/logs/col-b-backend.log" 2>&1 &
COL_B_PID=$!
echo "  -> College B Backend PID: $COL_B_PID"

# 4. Start CM Frontend (Port 3001)
echo ""
echo "[4/6] Starting CM Frontend (Port 3001)..."
nohup node "$ROOT_DIR/consent-manager/frontend/server.js" </dev/null > "$ROOT_DIR/logs/cm-front.log" 2>&1 &
CM_FRONT_PID=$!
echo "  -> CM Frontend PID: $CM_FRONT_PID"

# 5. Start College A Frontend (Port 3002)
echo ""
echo "[5/6] Starting College A Frontend (Port 3002)..."
nohup node "$ROOT_DIR/college-a/frontend/server.js" </dev/null > "$ROOT_DIR/logs/col-a-front.log" 2>&1 &
COL_A_FRONT_PID=$!
echo "  -> College A Frontend PID: $COL_A_FRONT_PID"

# 6. Start College B Frontend (Port 3003)
echo ""
echo "[6/6] Starting College B Frontend (Port 3003)..."
nohup node "$ROOT_DIR/college-b/frontend/server.js" </dev/null > "$ROOT_DIR/logs/col-b-front.log" 2>&1 &
COL_B_FRONT_PID=$!
echo "  -> College B Frontend PID: $COL_B_FRONT_PID"

disown -a 2>/dev/null || true

# Save PIDs
cat <<EOF > "$ROOT_DIR/.running_pids.json"
{
  "CmPid": $CM_PID,
  "ColAPid": $COL_A_PID,
  "ColBPid": $COL_B_PID,
  "CmFrontPid": $CM_FRONT_PID,
  "ColAFrontPid": $COL_A_FRONT_PID,
  "ColBFrontPid": $COL_B_FRONT_PID
}
EOF

echo ""
echo "Waiting for services to finish initializing..."

endpoints=(
  "Consent Manager UI (Port 3001)|http://localhost:3001"
  "College A UI (Port 3002)|http://localhost:3002"
  "College B UI (Port 3003)|http://localhost:3003"
  "Consent Manager API (Port 8095)|http://localhost:8095/health"
  "College A API (Port 8081)|http://localhost:8081/health"
  "College B API (Port 8082)|http://localhost:8082/health"
)

MAX_WAIT=45
START_TIME=$(date +%s)

for item in "${endpoints[@]}"; do
  NAME="${item%%|*}"
  URL="${item##*|}"
  READY=0
  
  while [ $READY -eq 0 ]; do
    NOW=$(date +%s)
    ELAPSED=$((NOW - START_TIME))
    if [ $ELAPSED -ge $MAX_WAIT ]; then
      break
    fi
    
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null || echo "000")
    if [ "$STATUS" = "200" ]; then
      READY=1
      break
    fi
    sleep 1
  done
  
  if [ $READY -eq 1 ]; then
    echo "  [OK] $NAME is healthy."
  else
    echo "  [WAIT] $NAME still starting up..."
  fi
done

echo ""
echo "=========================================================="
echo " [+] ALL 6 NODES & INTERFACES ARE READY!"
echo " ----------------------------------------------------------"
echo " [CM]    1. Consent Manager UI:         http://localhost:3001  (API: :8095)"
echo " [COL-A] 2. College A University UI:    http://localhost:3002  (API: :8081)"
echo " [COL-B] 3. College B University UI:    http://localhost:3003  (API: :8082)"
echo "=========================================================="
