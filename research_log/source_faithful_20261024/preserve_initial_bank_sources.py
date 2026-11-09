"""Recover initial source snapshots ONLY when pre-recorded raw hashes match."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
folder = Path(__file__).parent
record = {key.replace('\\', '/'): value for key, value in
          json.loads((folder / 'qft_bank_pilot_results.json').read_text())['source_sha256'].items()}
cases = [
    ('simulation/source_faithful_20261024/qft_bank.py', 'qft_bank_initial_source_snapshot.py', [
       ('all(type(x) is int for x in value)', 'all(isinstance(x, int) for x in value)'),
       ('if type(depth) is not int or not 0 <= depth <= len(weights):', 'if not 0 <= depth <= len(weights):')]),
    ('research_log/source_faithful_20261024/qft_bank_pilot.py', 'qft_bank_pilot_initial_source_snapshot.py', [
       ('               overlapping_reject_flag_columns=0,',
        '               exact_rational_bank_predicate_disagreements=0, overlapping_reject_flag_columns=0,')])]
out = []
for source, target, replacements in cases:
    content = (ROOT / source).read_bytes()
    for before, after in replacements:
        before, after = before.encode(), after.encode()
        if content.count(before) != 1:
            raise RuntimeError('Unexpected source shape; do not fabricate snapshot')
        content = content.replace(before, after)
    actual = hashlib.sha256(content).hexdigest()
    if actual != record[source]:
        raise RuntimeError('Snapshot does not match PRE-RECORDED raw pilot source hash')
    path = folder / target
    with path.open('xb') as stream:
        stream.write(content)
    out.append(dict(source=source, recovered_snapshot=target, sha256=actual,
                    status='BYTE_HASH_MATCH_TO_PRE_RECORDED_RAW_PILOT'))
(folder / 'qft_bank_initial_source_snapshots.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
