function res=pumpBuiltInController(x,ip,P,llib,ulib)
    numSettings = size(P,2);
    if x(2) <= llib
        res = numSettings;
    elseif x(2) >= ulib
        res =  1;
    else
        res = ip;
    end
end