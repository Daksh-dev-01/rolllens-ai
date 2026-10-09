#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/../frontend"
npm install
printf '\nFrontend dependencies installed.\nRun: npm run dev\n'
