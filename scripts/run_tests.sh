#!/bin/bash
set -e

BROWSER=${1:-chromium}
RUN_ENV=${2:-cicd}
HEADLESS=${3:-true}
TESTS_PATH=${4:-web_ui/ui_tests}
HOST=${5:-}

echo "Browser: $BROWSER"
echo "Run env: $RUN_ENV"
echo "Headless: $HEADLESS"
echo "Tests path: $TESTS_PATH"

export env=$RUN_ENV
export BROWSER_HEADLESS=$HEADLESS

if [ -n "$HOST" ]; then
  export host=$HOST
  echo "Host: $HOST"
fi

mkdir -p reports
mkdir -p allure-results

pytest -v "$TESTS_PATH" \
  --browser "$BROWSER" \
  --screenshot only-on-failure \
  --video retain-on-failure \
  --junitxml="reports/junit-${BROWSER}.xml" \
  --alluredir="allure-results"