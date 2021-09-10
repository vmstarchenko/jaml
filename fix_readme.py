import re
import sys

with open('README.md') as f:
    data = f.read()

print(re.sub(
    r'\n>>> \n>>> # (.*)\n',
    r'\n```\n- \1\n```python\n',
    sys.stdin.read(),
))
