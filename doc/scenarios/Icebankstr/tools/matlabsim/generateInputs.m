function res = generateInputs(ibc,env)
%x0,u0,ti,P,llib,ulib,v,costProfile)
    numInputs = size(ibc.u,2);
    %u0=[ienv,p,ces,tenv,vcur,pe,Cs]';
    u0 = ibc.u;
    u1 = ibc.u;
    ti = env.ti;
    %Ienv get from file
    %ienv = u0(1);     
    ibc.ienv = getData(env.outIrr,ti);
    ibc.isp = ibc.ienv*ibc.ienvmul; % is this ok?

    %p pump
    p = u0(2);
    ip = find(ibc.P==p);
    indexp1 = ip;
    if mod(ti,env.controlStep)==0
        indexp1 = callController(ibc,env);
    end
    % the built in controller overrides all other controllers
    indexp1 = pumpBuiltInController(ibc.x,indexp1,ibc.P,ibc.llib,ibc.ulib);
    p1 = ibc.P(indexp1);


    %Ces 
    % ibc.tenv = 25.0;

    ces = ibc.isp;
    if (ibc.isp - p1 < 0) 
        ces = p1;
    end

    %Tenv get from file
    ibc.tenv = getData(env.outTemp,ti);

    %ventilator V
    vcur = u0(5);
    v1 = ventilatorController(ibc.x,ibc.tset,ibc.tdelta,ibc.v,vcur);


    %Pe effective cooling power
    pe = cop(p1);


    %Cs compute the rate cost given KWh
    costKWh = getCostKWh(env.costProfile,ti);
    jcost = costPerJoule(costKWh);        
    if (p1-ibc.isp < 0) 
        costnow = 0;
    else 
        costnow = jcost * (p1-ibc.isp) ;
    end

    u1(1) = ibc.ienv;
    u1(2) = p1;
    u1(3) = ces;
    u1(4) = ibc.tenv;
    u1(5) = v1;
    u1(6) = pe;
    u1(7) = costnow;
    res = u1;
end
