"""Adversarial manuscript/evidence checks; writes new audit files only."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,re,sys,itertools,statistics
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'paper-qip';sys.path.insert(0,str(ROOT))
from research_log.claim_validation_20261025.theory_adversarial_audit import vertices,all_subset_interval
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=json.loads((OUT/'audit/original_paper_manifest.json').read_text())
conflicts=[p for p,h in original.items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
assert not conflicts,conflicts
assert set(original)=={str(p.relative_to(ROOT)) for p in (ROOT/'paper').rglob('*') if p.is_file()},'paper file set changed'
# Independently reconstruct the newly typeset one-based family, using the
# primal-vertex/all-subset reference, not the bank constructor.
barrier_checks=0
for m in [2,3,5,8]:
    w=[2]*m+[1];v=[4*(m-i+1)+1 for i in range(1,m+1)]+[1];k=m//2;W=2*k+1
    assert v[-2]==5 and v[-1]==1
    for i in range(k+1,m+1):
        d=i-k-1;U=vertices(w[d:],v[d:],W);rho=Q(v[i-1],2)
        assert all_subset_interval(w[d:],v[d:],W,U.numerator//U.denominator+1)==(rho-Q(1,2),True,rho+Q(1,2))
        barrier_checks+=1
    assert all_subset_interval([],[],W,1)==(Q(0),False,Q(1,W));barrier_checks+=1
# Falsify sign/strictness mistakes in the displayed constant arithmetic by
# exhaustively checking direct rational bounds independently on small fixtures.
identity_checks=0
for w,v,W in [([2,4,1],[1,2,0],3),([17,3],[16,2],1),([],[],0),([1],[0],0),([2,3],[3,1],10)]:
    order=sorted(range(len(w)),key=lambda i:Q(v[i],w[i]),reverse=True)
    bank={Q(0),Q(1,2),*[Q(a,b) for a,b in zip(v,w)]}
    t=max(1,(sum(v)+1).bit_length());tmax=(1<<t)-1
    for d in range(len(w)+1):
      for bits in itertools.product((0,1),repeat=d):
       P=sum(v[i]*x for i,x in zip(order[:d],bits));R=W-sum(w[i]*x for i,x in zip(order[:d],bits))
       for lam in bank:
        a,b=lam.numerator,lam.denominator;c=[b*vi-a*wi for wi,vi in zip(w,v)]
        C=a*W+sum(max(x,0) for x in c)
        D=sum((1-x)*max(c[i],0)+x*max(-c[i],0) for i,x in zip(order[:d],bits))
        F=P+lam*R+sum(max(Q(v[i])-lam*w[i],0) for i in order[d:])
        assert Q(C-D,b)==F
        for tau in range(tmax+1):
         assert (C<D+b*tau)==(F<tau)
         assert 0<=D+b*tau<=sum(abs(c[i]) for i in order[:d])+b*tmax
         identity_checks+=1
main=(OUT/'main.tex').read_text();bib=(OUT/'references.bib').read_text()
labels=re.findall(r'\\label\{([^}]+)\}',main)
refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',main)
assert len(labels)==len(set(labels))
assert not set(refs)-set(labels),set(refs)-set(labels)
keys=set(re.findall(r'@\w+\s*\{([^,]+),',bib));cites=set(k.strip() for m in re.findall(r'\\cite\w*\{([^}]+)\}',main) for k in m.split(','))
assert keys==cites and len(keys)==40
abstract=re.search(r'\\abstract\{(.*?)\}\s*\\keywords',main,re.S).group(1)
assert 150<=len(abstract.split())<=250
assert all(x not in main for x in ['RETAINED_LITERATURE','BARRIER_PROOF_REPLACEMENT','COVERAGE_TABLE','RESOURCE_TABLE'])
result=dict(original_files_verified=len(original),original_conflicts=conflicts,barrier_endpoint_checks=barrier_checks,barrier_mismatches=0,arithmetic_identity_and_width_checks=identity_checks,identity_mismatches=0,reference_entries=len(keys),cited_entries=len(cites),missing_cross_references=0,abstract_words=len(abstract.split()),scope='DERIVED manuscript arithmetic and evidence checks; no new large-circuit simulation; same-agent separate audit pass')
(OUT/'audit/REVISION_VERIFICATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
