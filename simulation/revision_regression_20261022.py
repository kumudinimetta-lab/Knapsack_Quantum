"""Exploratory regression of actual core-tree nodes, never scheduled queries."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[1]


def main():
    source=ROOT/'research_log/revision_20261022_reference_results.json'
    rows=json.loads(source.read_text())['reference']['rows']
    # T_core is counted by exact branch-and-bound, not algebraically constructed
    # from either predictor. LP gap is computed independently from exact LP and DP.
    # Zero-gap/capped cases are counted explicitly and not silently discarded.
    records=[]
    for row in rows:
        gap=float(Fraction(row['lp_gap']))
        records.append({**row,'gap':gap,'group':f"{row['n']}-{row['seed']}"})
    df=pd.DataFrame(records)
    models=[]
    for name in ['pooled']+list(df['type'].unique()):
        sub=df if name=='pooled' else df[df['type']==name]
        use=sub[(sub['gap']>0)&(~sub['bb_capped'])].copy()
        record={'class':name,'total':len(sub),'excluded_zero_gap':int((sub['gap']==0).sum()),
                'capped':int(sub['bb_capped'].sum()),'included':len(use)}
        if len(use)>=10:
            use['log_gap']=np.log(use['gap'])
            use['log_nodes']=np.log(use['core_nodes'])
            model=smf.ols('log_nodes ~ log_gap + m',data=use).fit()
            folds=[]
            for train,test in GroupKFold(5).split(use,groups=use['group']):
                fit=smf.ols('log_nodes ~ log_gap + m',data=use.iloc[train]).fit()
                folds.append(r2_score(use.iloc[test]['log_nodes'],fit.predict(use.iloc[test])))
            record.update(r2=float(model.rsquared),cv_mean_r2=float(np.mean(folds)),
                          coefficients=dict(model.params),pvalues=dict(model.pvalues))
        models.append(record)
    out={'classification':'DERIVED_EXPLORATORY_STATISTICS','response':'log(core_nodes)',
         'predictors':['log(exact LP minus DP optimum)','core size'],
         'cross_validation':'5-fold GroupKFold, grouping same n/seed across classes',
         'models':models}
    path=ROOT/'research_log/revision_20261022_regression_results.json'
    path.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
