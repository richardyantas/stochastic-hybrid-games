strategy Opt = minE (pareto) [<=horizon]: <> GTime>=horizon
simulate 1 [<=horizon] { ppos,visitedPatterns,mode,flag,Tnext,zi,mvalve } under Opt
saveStrategy("strategy.txt", Opt)