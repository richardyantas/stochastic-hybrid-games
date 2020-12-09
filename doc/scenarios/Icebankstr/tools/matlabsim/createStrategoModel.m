function model = createStrategoModel(ibc,env)
    %in stratego our strategies are a matrix of the form
    %     step_1 step_2 ...
    % v_1   0      1
    % v_2   1      1
    % ...
    % we return only the values V for step_1.     


% Tini,Tg,tStep,nrOfSteps,outsideTemp, ... 
    %                                  tglobal, filename, Vprevious, ...
    %                                  versionNr, nrRooms, floorConf, ...
    %                                  strDC2, env
        
    pathModels = env.pathAutoModels;
    pathLoadModels = env.pathLoadModels;
    versionNr = env.expId;
    %Tenv = buildOutSideTemp();    
    filename = env.modelFileName;    
    stepsInDay = (60*24)/env.controlStepMinutes;
    model = setParameters();    


    function subdatavec = buildData(datavec,ti)
    %datavec is assumed to be in 15minutes intervals
        indexini = ceil((ti+1)/(60*15));
        indexfin = indexini + stepsInDay - 1;
        subdatavec = datavec(indexini:indexfin);
    end


    function model = replaceInModel(modelstr,strToReplace, strNewString)
        k = strfind(modelstr,strToReplace);
        if size(k,2) == 0 
            msg = strcat('fail: could not find str to replace ', strToReplace);
            fprintf(msg);
        end        
        model = strrep(modelstr, strToReplace, strNewString);            
    end
    
    function model = setParameters()
    %the stratego model for addaptative learning
        cd(pathLoadModels);
        new_model = fileread(filename);
        cd(pathModels);
        str_stepsInDay = num2str(stepsInDay);
        
        str_to_replace = ['//PLACEHOLDER_Troom']; 
        str_temp = sprintf('%.3f,' , ibc.troom);
        str_temp = str_temp(1:end-1);    
        str_to_plug = strcat('double Troom = ', str_temp, ';');
        new_model = replaceInModel(new_model,str_to_replace, str_to_plug);

        str_to_replace = ['//PLACEHOLDER_Lib']; 
        str_temp = sprintf('%.3f,' , ibc.lib);
        str_temp = str_temp(1:end-1);    
        str_to_plug = strcat('double Lib = ', str_temp, ';');
        new_model = replaceInModel(new_model,str_to_replace, str_to_plug);
        
        str_to_replace = ['//PLACEHOLDER_TOut']; 
        str_temp = sprintf('%.3f,', buildData(env.outTemp,env.ti));
        str_temp = str_temp(1:end-1);    
        str_to_plug = strcat('const double TOut[',str_stepsInDay,'] = {', str_temp, '};');
        new_model = replaceInModel(new_model,str_to_replace, str_to_plug);
        
        str_to_replace = ['//PLACEHOLDER_Wir']; 
        str_temp = sprintf('%.3f,', buildData(env.outIrr,env.ti));
        str_temp = str_temp(1:end-1);    
        str_to_plug = strcat('const double Wir[',str_stepsInDay,'] = {', str_temp, '};');
        new_model = replaceInModel(new_model,str_to_replace, str_to_plug);
       
        str_to_replace = ['//PLACEHOLDER_CostSpot']; 
        str_temp = sprintf('%.3f,', buildData(env.costProfile,env.ti));
        str_temp = str_temp(1:end-1);    
        str_to_plug = strcat('const double CostSpot[',str_stepsInDay,'] = {', str_temp, '};');
        new_model = replaceInModel(new_model,str_to_replace, str_to_plug);
        
        % %find bool valve[valve_t] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        % %0};
        % str_to_replace = ['//PLACEHOLDER_valve'];
        % str_temp = sprintf('%d,', Vprevious);
        % str_temp = str_temp(1:end-1);    
        % fprintf('create stratego model: predicting using Vprevios = %s \n', str_temp)
        % str_to_plug = strcat('bool valve[valve_t] = {', str_temp, '};');
        % new_model = replaceInModel(new_model,str_to_replace, str_to_plug);
        
        
        version =  strcat(num2str(env.expId),num2str(versionNr));    
        cd(pathModels);
        newFileName = strcat(filename,'_',version,'.xml');          
        fid = fopen(newFileName,'w');           
        if fid ~= -1
            fprintf(fid,'%s\r\n',new_model);    
            fclose(fid);                     
        end
        fprintf('calling stratego with model: %s \n', newFileName);
        model = newFileName;
    end
    
    function matStr = printInUppaalFormat(A)
        numRows = size(A,1);
        numCols = size(A,2);
        matStr = ' { ';
        for i=1:numRows
            strRow = '{ ';
            for j=1:numCols-1
                strRow = sprintf('%s %s',strRow,sprintf('%d,', A(i,j)));
            end
            if (i==numRows)
                strRow = sprintf('%s %s',strRow, sprintf('%d } ', A(i,j+1)));
            else
                strRow = sprintf('%s %s',strRow, sprintf('%d }, ', A(i,j+1)));
            end
            matStr = sprintf('%s %s',matStr, strRow);        
        end
        matStr = sprintf('%s %s', matStr, ' }');
    end
    
    function matStr = printInUppaalFormatDouble(A)
        numRows = size(A,1);
        numCols = size(A,2);
        matStr = ' { ';
        for i=1:numRows
            strRow = '{ ';
            for j=1:numCols-1
                strRow = sprintf('%s %s',strRow,sprintf('%.4f,', A(i,j)));
            end
            if (i==numRows)
                strRow = sprintf('%s %s',strRow, sprintf('%.4f } ', A(i,j+1)));
            else
                strRow = sprintf('%s %s',strRow, sprintf('%.4f }, ', A(i,j+1)));
            end
            matStr = sprintf('%s %s',matStr, strRow);        
        end
        matStr = sprintf('%s %s', matStr, ' }');
    end
end