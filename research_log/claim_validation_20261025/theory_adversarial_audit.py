"""Fresh independent LP-vertex/dual-subset audit; no old code/raw edits."""
import functools,itertools,json,random,sys,hashlib
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'simulation'))
from source_faithful_20261024.compressed_bank import build_compressed_bank,build_dp_free_bank
from source_faithful_20261024.continuous_bank import build_continuous_bank


def order(w,v):
    def compare(i,j):
        cross=v[i]*w[j]-v[j]*w[i]
        return -1 if cross>0 else 1 if cross<0 else i-j
    return tuple(sorted(range(len(w)),key=functools.cmp_to_key(compare)))


def vertices(w,v,R):
    """Enumerate all box vertices and one-fractional-coordinate vertices."""
    best=Q(0);n=len(w)
    for bits in itertools.product((0,1),repeat=n):
        weight=sum(x*y for x,y in zip(w,bits));profit=sum(x*y for x,y in zip(v,bits))
        if weight>R:continue
        best=max(best,Q(profit))
        for j,bit in enumerate(bits):
            if not bit and R-weight<=w[j]:
                best=max(best,Q(profit)+Q(R-weight,w[j])*v[j])
    return best


def dual(w,v,R,lam):return lam*R+sum(max(Q(value)-lam*weight,0) for weight,value in zip(w,v))


def all_subset_interval(w,v,R,K):
    """Use ALL subset affine functions, independently of sorted-prefix code."""
    lo=Q(0);opened=False;hi=None
    for bits in itertools.product((0,1),repeat=len(w)):
        weight=sum(a*b for a,b in zip(w,bits));profit=sum(a*b for a,b in zip(v,bits));D=R-weight;C=K-profit
        if D>0:
            val=Q(C,D)
            if hi is None or val<hi:hi=val
        elif D<0:
            val=Q(C,D)
            if val>lo:lo=val;opened=True
            elif val==lo:opened=True
        elif C<=0:raise AssertionError('Independent interval unexpectedly empty')
    return lo,opened,hi


def flo(value):return value.numerator//value.denominator


def main():
    cases=[]
    # Exhaustive two-item domain specifically targets ties, zero profits,
    # equality, zero residuals and all-fit transition capacities.
    for w in itertools.product(range(1,5),repeat=2):
        for v in itertools.product(range(4),repeat=2):
            for W in range(sum(w)+2):cases.append((list(w),list(v),W,'systematic_n2'))
    rng=random.Random(202610251703)
    for t in range(96):
        n=rng.randrange(3,8);w=[rng.randrange(1,23) for i in range(n)]
        if t%4==0:v=[3*x for x in w]  # many tied ratios
        elif t%4==1:v=[rng.choice([0,0,1,17]) for i in range(n)]
        else:v=[rng.randrange(0,61) for i in range(n)]
        cases.append((w,v,rng.randrange(sum(w)+2),'random_new_seed'))
    counts=dict(instances=len(cases),systematic_n2=sum(c[3]=='systematic_n2' for c in cases),
        feasible_prefixes=0,root_tail_value_mismatches=0,grid_floor_mismatches=0,
        dp_free_floor_mismatches=0,continuous_floor_mismatches=0,
        independent_minimum_certificates=0,minimum_certificate_failures=0,
        independent_critical_interval_checks=0,critical_interval_mismatches=0,
        independent_grid_minimum_certificates=0,grid_minimum_certificate_failures=0,
        grid_critical_coverage_mismatches=0,barrier_endpoint_checks=0,barrier_endpoint_mismatches=0)
    failures=[]
    for num,(w,v,W,panel) in enumerate(cases):
        grid=build_compressed_bank(w,v,W);free=build_dp_free_bank(w,v,W);cont=build_continuous_bank(w,v,W)
        idx=order(w,v);positions={i:j for j,i in enumerate(idx)}
        states={}
        for d in range(len(w)+1):
            for prefix in itertools.product((0,1),repeat=d):
                weight=sum(w[i]*prefix[j] for j,i in enumerate(idx[:d]));P=sum(v[i]*prefix[j] for j,i in enumerate(idx[:d]))
                if weight>W:continue
                sw=[w[i] for i in idx[d:]];sv=[v[i] for i in idx[d:]];R=W-weight
                U=vertices(sw,sv,R);states[(d,R)]=(sw,sv,U)
                counts['feasible_prefixes']+=1
                tail=min(dual(sw,sv,R,Q(*lam)) for lam in grid['root_tail_grid'])
                counts['root_tail_value_mismatches']+=tail!=U
                for name,result in [('grid',grid),('dp_free',free),('continuous',cont)]:
                    bank=min(dual(sw,sv,R,Q(*lam)) for lam in result['bank'])
                    counts[name+'_floor_mismatches']+=flo(bank)!=flo(U)
                    if flo(bank)!=flo(U):failures.append(dict(w=w,v=v,W=W,d=d,prefix=prefix,method=name,U=str(U),bank=str(bank)))
        if cont['status']=='complete':
            critical=[]
            for claim in cont['critical_intervals']:
                key=(claim['depth'],claim['remaining_capacity']);sw,sv,U=states[key]
                actual=all_subset_interval(sw,sv,key[1],flo(U)+1)
                expected=(Q(*claim['lower']),claim['lower_open'],None if claim['upper'] is None else Q(*claim['upper']))
                counts['independent_critical_interval_checks']+=1
                counts['critical_interval_mismatches']+=actual!=expected
                critical.append(actual)
            disjoint=all(a[2] is not None and a[2]<=b[0] for a,b in zip(critical,critical[1:]))
            counts['independent_minimum_certificates']+=1
            counts['minimum_certificate_failures']+=not(disjoint and len(critical)==cont['bank_size'])
        if grid['status']=='complete':
            critical_grid=[];candidates=[Q(*x) for x in grid['root_tail_grid']]
            for claim in grid['greedy_witness_intervals']:
                key=(claim['depth'],claim['remaining_capacity']);sw,sv,U=states[key]
                actual={j for j,lam in enumerate(candidates) if flo(dual(sw,sv,key[1],lam))==flo(U)}
                expected=set(range(claim['left'],claim['right']+1))
                counts['grid_critical_coverage_mismatches']+=actual!=expected
                critical_grid.append(actual)
            disjoint=all(not (a&b) for i,a in enumerate(critical_grid) for b in critical_grid[i+1:])
            counts['independent_grid_minimum_certificates']+=1
            counts['grid_minimum_certificate_failures']+=not(disjoint and len(critical_grid)==grid['bank_size'])
        if failures:
            break
        if num%500==0:print(num+1,'/',len(cases),flush=True)
    boundaries=dict(
        noninteger_threshold=dict(weights=[1,1],values=[1,1],capacity=1,exact_bound='1',continuous_bank_bound='3/2',tau='5/4',exact_prune=True,bank_prune=False),
        nonprefix_assignment=dict(weights=[10,9],values=[100,1],capacity=15,assign_low_density_item_one=True,exact_bound='61',root_tail_bound='905/9',tau=62,exact_prune=True,bank_prune=False),
        item_weight_instead_of_tie_group_weight=dict(weights=[2,2,3],values=[1,1,1],capacity=1,exact_bound='1/2',wrong_multiplier='1/3',wrong_bound='1',tau=1,exact_prune=True,wrong_prune=False),
        nonstrict_radius=dict(weights=[1],values=[1],capacity=0,exact_bound='0',wrong_multiplier='0',wrong_bound='1',tau=1,exact_prune=True,wrong_prune=False),
        negative_multiplier=dict(weights=[1],values=[1],capacity=2,exact_bound='1',wrong_multiplier='-1',wrong_bound='0',tau=1,unsafe_wrong_prune=True),
        weight_gcd_normalization_changes_LP=dict(weights=[2],values=[3],capacity=1,old_LP='3/2',normalized_LP='0',tau=1,old_prune=False,new_prune=True))
    # Compute these boundary witnesses directly, rather than trusting strings.
    assert vertices([1,1],[1,1],1)==1 and dual([1,1],[1,1],1,Q(1,2))==Q(3,2)
    assert 1+vertices([10],[100],6)==61 and min(1+dual([10],[100],6,x) for x in [Q(0),Q(1,9)])==Q(905,9)
    assert vertices([2,2,3],[1,1,1],1)==Q(1,2) and dual([2,2,3],[1,1,1],1,Q(1,3))==1
    assert vertices([1],[1],0)==0 and dual([1],[1],0,Q(0))==1
    assert vertices([1],[1],2)==1 and dual([1],[1],2,Q(-1))==0
    assert vertices([2],[3],1)==Q(3,2) and vertices([1],[3],0)==0
    barriers=[]
    for n in [2,3,5,8]:
        q=n//2;w=[2]*n+[1];v=[4*(n-i)+1 for i in range(n)]+[1];W=2*q+1
        actual_intervals=[]
        for s in range(q,n):
            d=s-q;sw=w[d:];sv=v[d:];U=vertices(sw,sv,W)
            actual=all_subset_interval(sw,sv,W,flo(U)+1)
            rho=Q(v[s],2);expected=(rho-Q(1,2),True,rho+Q(1,2))
            counts['barrier_endpoint_checks']+=1;counts['barrier_endpoint_mismatches']+=actual!=expected
            actual_intervals.append([str(x) for x in actual])
        zero=all_subset_interval([],[],W,1)
        counts['barrier_endpoint_checks']+=1;counts['barrier_endpoint_mismatches']+=zero!=(Q(0),False,Q(1,W))
        barriers.append(dict(main_items=n,expected_minimum=n-q+1,main_coverage_intervals=actual_intervals,zero_leaf=[str(x) for x in zero]))
    files=[ROOT/'simulation/source_faithful_20261024/compressed_bank.py',ROOT/'simulation/source_faithful_20261024/continuous_bank.py',Path(__file__)]
    out=dict(counts=counts,failures=failures,boundary_counterexamples=boundaries,barrier_checks=barriers,
        source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        scope='Fresh exact LP VERTEX and ALL-SUBSET dual interval audit. No circuit simulator or paper changes. Boundary witnesses intentionally violate assumptions; they are not bugs in scoped claims.')
    (HERE/'theory_adversarial_audit_v2.json').write_text(json.dumps(out,indent=2));print(json.dumps(counts),flush=True)
    if failures or any(counts[k] for k in ['root_tail_value_mismatches','grid_floor_mismatches','dp_free_floor_mismatches','continuous_floor_mismatches','minimum_certificate_failures','critical_interval_mismatches','grid_minimum_certificate_failures','grid_critical_coverage_mismatches','barrier_endpoint_mismatches']):
        raise RuntimeError('RESEARCH_INTEGRITY_STOP: affected theorem/code mismatch; raw retained')


if __name__=='__main__':main()
