"""Predeclare core builds and exact duplicate reuse; no outcome selection."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def save_new(name,obj):
    path=HERE/name
    if path.exists() and json.loads(path.read_text(encoding='utf8'))!=obj:
        raise RuntimeError('Refuse to overwrite different resource panel')
    if not path.exists(): path.write_text(json.dumps(obj,indent=2),encoding='utf8')

def main():
    originals=json.loads((HERE/'inputs.json').read_text(encoding='utf8'))
    cores=json.loads((HERE/'inputs_core700.json').read_text(encoding='utf8'))
    index={r['id']:r for r in originals['records']}
    changed=[]; aliases=[]
    for core in cores['records']:
        base=index[core['original_id']]
        equal=all(core[k]==base[k] for k in ['weights','values','capacity'])
        aliases.append(dict(core_id=core['id'],resource_id=base['id'] if equal else core['id'],
            source_panel='main_single_v1 / representative_wrappers_v1' if equal else 'core_changed',
            identical_weights_values_capacity=equal))
        if not equal: changed.append(core)
    panel=dict(schema_version=1,description='All changed cores; unchanged cores explicitly reuse identical circuit inputs',
        source_registry_sha256=hashlib.sha256((HERE/'inputs_core700.json').read_bytes()).hexdigest(),
        pilot_ids=[r['id'] for r in changed if r['pilot']],records=changed)
    save_new('inputs_core_changed_resources.json',panel)
    save_new('inputs_core_wrapper_resources.json',dict(panel,records=[r for r in changed if r['trial']<3]))
    save_new('core_resource_aliases.json',dict(records=aliases,
        explanation='Reused only when the full ordered input arrays and capacity match exactly; not dropped observations'))
    print(json.dumps(dict(core_inputs=len(aliases),changed_builds=len(changed),identical_reused=len(aliases)-len(changed),
        changed_wrapper_builds=sum(r['trial']<3 for r in changed))))

if __name__=='__main__': main()
