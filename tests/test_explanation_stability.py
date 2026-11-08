from ml.explainability.stability import explanation_stability,rank_biased_overlap
def test_identical_rankings():assert rank_biased_overlap(['a','b'],['a','b'])>.99
def test_pairwise():assert explanation_stability([['a','b'],['a','c'],['b','a']])['n_pairs']==3
