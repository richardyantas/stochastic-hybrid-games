function ibc = getIBconf(confIdStr)

    ibc.confId =  str2num(confIdStr);    
    % constants
    cr = 0.00003;
    cjc = -0.0004; % should be a negative constant
    ci = 0.000001;
    ibc.ulib = 1000000;
    ibc.llib = 5000;
    
    % inputs
    ibc.ienv = 10.0;
    ibc.ienvmul = 8;
    ibc.isp = ibc.ienv*ibc.ienvmul;
    ibc.tenv = 10.0;
    ibc.P = [0, 5000, 11000]; %settings of the pump
    ibc.v = 4000/3600;
    ibc.vcur = 0;
    ibc.p = ibc.P(1); % the current setting
    ibc.pe = cop(ibc.p);
    ibc.Ispen = 1.0;
    ibc.Pen = 1.0;
    ibc.ces = ibc.isp;
    ibc.tset = -10;
    ibc.tdelta = 1.0;
    
    
    
    switch (ibc.confId)
      case 1        
        % initial state
        ibc.troom = 10;
        ibc.lib = 10000;
        ibc.e = 0;
        ibc.es = 0;

      otherwise
        warning('Unexpected ib configuration id.');
    end

    ibc.A = [-cr,0,0,0,0 ; 0,0,0,0,0 ; 0,0,0,0,0 ; 0,0,0,0,0; 0,0,0,0,0];
    ibc.B = [ci,0,0,cr,cjc,0,0 ; 0,0,0,0,-1,1.0/60,0; 0,1,0,0,0,0,0 ; ...
             0,0,1,0,0,0,0 ; 0,0,0,0,0,0,1.0 ]; %min(P,Isp) = Isp and
    ibc.x0=[ibc.troom,ibc.lib,ibc.e,ibc.es,0.0]';
    ibc.u0=[ibc.ienv,ibc.p,ibc.ces,ibc.tenv,ibc.vcur,ibc.pe,0]';       
    ibc.u = ibc.u0;
    ibc.x = ibc.x0;
end