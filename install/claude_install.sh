#!/bin/bash

set -e
set -o pipefail

cd "$(readlink -f "$(dirname "$0")")"
cd ..

echo "Y" | ./install/python -u ./install/claude_skill_install.py -c