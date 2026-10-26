"""v2.5.5 evidence-based second-review state validation (not a legal audit)."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
assert (root/'data/dmc_second_review.js').exists()
s=(root/'data/content.js').read_text('utf8')
d=json.loads(s.split('=',1)[1].strip().rstrip(';'))
report=json.loads((root/'data/dmc_second_review.json').read_text('utf8'))
assert d['review']['secondPass']['status']=='incomplete'
assert d['review']['secondPass']['fullyVerifiedCount']==0
assert report['fully_verified_units']==0
assert len(d['translations'])==85
assert all('secondReview' in row and row['secondReview']['completeSentenceVerification'] is False for row in d['translations'])
t={row['key']:row for row in d['translations']}
for lang in ['tc','sc']:
 assert all(f'({c})' in t['c23'][lang] for c in ['e','f'])
 assert any(term in t['c23'][lang] for term in ['按金已被動用','按金已被动用'])
 assert any(term in t['c62'][lang] for term in ['整個屋苑或其受影響部分','整个屋苑或其受影响部分'])
assert '31% day of December' not in t['c15']['en'] and '31st day of December' in t['c15']['en']
assert '0／85' in (root/'quality.html').read_text('utf8')
assert all(f in (root/'index.html').read_text('utf8') for f in ['data/content.js?v=2.5.5','app.js?v=2.5.5'])
print('PASS: DMC 85 units, 0 fully verified (truthful), confirmed clause changes and version badges')
