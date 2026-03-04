"""Adiciona scripts/ ao sys.path para imports dos testes."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
