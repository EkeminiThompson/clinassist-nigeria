import numpy as np
def rank_biased_overlap(a:list[str],b:list[str],p=.9):
 if not 0<p<1:raise ValueError('p must be between 0 and 1')
 d=max(len(a),len(b))
 if not d:return 1.0
 score=sum((1-p)*p**(k-1)*len(set(a[:k])&set(b[:k]))/k for k in range(1,d+1))
 return float(score+p**d*len(set(a)&set(b))/d)
def explanation_stability(rankings:list[list[str]],p=.9):
 if len(rankings)<2:raise ValueError('Need at least two rankings')
 scores=[rank_biased_overlap(rankings[i],rankings[j],p) for i in range(len(rankings)) for j in range(i+1,len(rankings))]
 return {'mean_rbo':float(np.mean(scores)),'std_rbo':float(np.std(scores)),'n_pairs':len(scores)}
