function env = getExpEnv(strController, modelFile, queryFile, strLearningMet, strWeather, ...
                                       strExpId, ibconf, strStrategoParam,strStepSize,strNrSteps,strCostProfile)
    %contains experiment variables
    %weather opt: winter,summer,sinusoid,constant
    
    %PATHS
    env.expId = str2num(strExpId);    
    env.pathMain = pwd();    
    env.pathAutoModels = strcat(env.pathMain,'/automodels');
    env.pathLoadModels = strcat(env.pathMain,'/models');
    env.pathData = strcat(env.pathMain,'/data');
    env.stepSize = str2num(strStepSize); %this is for stratego, it will looke further
                                         %in the future 
    env.queryStr = 'icebankmodel.q';
    
    %SETTING PARAMETERS FOR LEARNING
    [~,env.controller] = getController(strController);
    env.useStrategy = usesStrategy(strController);
    env.nrSteps = str2num(strNrSteps);
    env.strWeather = strcat(env.pathData,'/',strWeather);
    env.modelFileName = modelFile;
    env.queryFile = queryFile;
    env.strLearningMet = strLearningMet;
    env.learningMet = str2num(strLearningMet);
    [env.flagInstantControlling,env.controller] = getController(strController);
    

    env.step = 60;                                                              
    env.stepd = 100;
    env.oneDaySec = 60*24*60;  % day in seconds                      
    env.simTime = env.oneDaySec*3; % simulation in seconds
    env.controlStep = 15*60;
    env.controlStepMinutes = 15;
    env.stepSize = env.controlStep; % de strategy controlling points
    env.strCostProfile = strcat(env.pathData,'/',strCostProfile);
    env.costProfile = loadCostProfile(env.strCostProfile);
    [env.outTemp,env.outIrr] = loadWeather(env.strWeather);
    env.ti = 0;
    

    function setStrategoParameter(strStrategoParam)
    %the stratego parameters should be comma separated and in a
    %fixed order
    %strStrategoParam = nrRuns,max_reset_learning
    %if strategoParam should be 'empty' if  no parameters 
        if (strcmp(strStrategoParam,'empty') == 1)
            env.nrRuns = 20;
            env.max_reset_learning = 0;
        else
            nrValidParams = 2;
            params = strsplit(strStrategoParam,'-')
            nrParams = size(params,2);
            if (nrParams ~= nrValidParams)
                fprintf('fail in parsing stratego parameter'); 
                return;
            else
                env.nrRuns = str2num(char(params(1)))
                env.max_reset_learning = str2num(char((params(2))))
            end
        end
    end

    
    function res = usesStrategy(strController)
        [~,controller] = getController(strController);        
        switch(controller)
          case ControllerClass.stratego
            res = true;
          otherwise
            res = false;                        
        end
    end    
    
end
