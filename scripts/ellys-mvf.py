#!/usr/bin/env python3
# scripts/ellys-mvf.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mvf.cli.main import cli

if __name__ == '__main__':
    cli()