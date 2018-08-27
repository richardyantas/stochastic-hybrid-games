function res = ventilatorController(x,tset,tdelta,v,vcur)    
    troom = x(1);
    if troom > (tset+tdelta)
        res = v;
    elseif troom < (tset-tdelta)
        res = 0;
    else
        res = vcur;
    end
end
