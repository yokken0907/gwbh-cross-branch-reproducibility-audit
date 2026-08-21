#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIP_SUFFIXES = {'.zip', '.docx', '.pdf', '.png', '.jpg', '.jpeg', '.gif'}
FORBIDDEN_LITERAL = [
    '/mnt/c/' + 'Users/', '/home/' + 'kei', 'C:' + '\\' + 'Users' + '\\', '/Users/' + 'KEI/',
    'BEGIN ' + 'OPENSSH PRIVATE KEY', 'BEGIN ' + 'RSA PRIVATE KEY', 'BEGIN ' + 'PRIVATE KEY',
]
SECRET_PATTERNS = [
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'gh[pousr]_[A-Za-z0-9_]{20,}'),
]
TEMP_PATTERNS = [
    re.compile(r'(^|/)__pycache__(/|$)'), re.compile(r'\.pyc$'), re.compile(r'\.tmp$'),
    re.compile(r'\.bak$'), re.compile(r'(^|/)\.DS_Store$'), re.compile(r'(^|/)Thumbs\.db$'),
    re.compile(r'(^|/)desktop\.ini$'), re.compile(r'(^|/)~\$'),
]

issues = []
for p in ROOT.rglob('*'):
    if not p.is_file():
        continue
    rel = p.relative_to(ROOT).as_posix()
    if rel == 'scripts/scan_public_tree.py':
        continue
    if any(rx.search(rel) for rx in TEMP_PATTERNS):
        issues.append((rel, 'temporary_file'))
        continue
    if p.suffix.lower() in SKIP_SUFFIXES:
        continue
    try:
        text = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for token in FORBIDDEN_LITERAL:
        if token in text:
            issues.append((rel, f'forbidden_literal:{token}'))
    for rx in SECRET_PATTERNS:
        if rx.search(text):
            issues.append((rel, f'secret_pattern:{rx.pattern}'))

# The intentionally published research contact address in CITATION.cff is not a secret.
print(f"{'PASS' if not issues else 'FAIL'} public-tree local-path/secret/temp scan")
for rel, why in issues:
    print(' ', rel, why)
raise SystemExit(0 if not issues else 2)
