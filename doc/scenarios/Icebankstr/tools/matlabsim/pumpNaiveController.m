function [res,len] =  pumpNaiveController(ibc,env)
% returns the index of the pump setting which minimizes the
% difference between P and Isp
    dist = abs(ibc.P - ibc.isp);
    res = find(dist==min(dist));
    len = 1;
end
