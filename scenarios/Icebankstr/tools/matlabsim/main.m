function main()
    
    currentFolder = pwd;
    addpath(currentFolder);
    strCostProfile = 'sinusoid';
    strStepSize='15';
    modelFile='icebankmodel.xml';
    queryFile='icebankmodel.q';
    strWeather='default';
    strExpId='1';
    ibconf='1';
    strStrategoParam='empty';
    
    strWeather = 'DRY_merged_6197.csv';
    strCostProfile = 'elspot-prices_2018_hourly_dkk.csv';
    strController='naive';
    %strController='stratego';
    strLearningMet='3';
    strNrSteps='3';
    strConfId='1';
    env = getExpEnv(strController, modelFile, queryFile, strLearningMet, strWeather, ...
                                       strExpId, ibconf, strStrategoParam, ...
                                  strStepSize, strNrSteps,strCostProfile);
    
    ibc = getIBconf(strConfId);
    
    
    SysFun1 = @(t,x,u) ibc.A*x + ibc.B*u;              

    tans=0;
    xans=ibc.x0';

    
    for i=0:env.step:env.simTime
        tspan = linspace(i, i+env.step, env.stepd);
        env.ti = i;
        ibc.u = generateInputs(ibc,env);
        [t,x]=ode45(@(t,x) SysFun1(t,x,ibc.u),tspan,ibc.x);
        ibc.x=x(end,:);
        tans = vertcat(tans,t);      
        xans = vertcat(xans,x); 
    end
    

    figure(1) %room temperature
    plot(tans, xans(:,1))
    title('Room temperature (Celsius)');

    figure(2) %lib
    plot(tans, xans(:,2))
    title('Level of the Icebank (Joule)');
    
    figure(3) %E
    plot(tans, xans(:,3))
    title('Energy consumption (Joule) ');
    
    figure(4) %E
    plot(tans, xans(:,5))
    title('Total cost (Dkk)');
    
    figure(5) %costKWh
    allTime = 0:env.step:env.simTime;
    costVec = @(ti) getCostKWh(env.costProfile,ti);
    plot(allTime, arrayfun(costVec,allTime));
    title('Cost KWh');
end
