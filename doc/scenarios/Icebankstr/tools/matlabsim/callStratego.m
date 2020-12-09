function [V,steps] = callStratego(ibc,env,model)
%in castratego our strategies are a matrix of the form
%     step_1 step_2 ...
% v_1   0      1
% v_2   1      1
% ...
%model,tStep,nrOfSteps,
    learningMet = env.learningMet;
    nrOfSteps = env.nrSteps;
    nrOutputs = 1;
    pathModels = env.pathAutoModels;
    %pathLoadModels = env.pathLoadModels;
    cmdout = executeStratego(model);
    strategy = extractStrategy(cmdout);
    norStrategy = normalizeStrategy(strategy);
    V = norStrategy;    
    V = V + 1; %because index of speeds starts at 1
    steps = size(norStrategy,2);
    
    
    function out = executeStratego(model)
        cd(pathModels);
        % this one is precise, in 5 rooms beats brute-force
        % com1 = ['~/bin/stratego-experimental/bin-Linux/verifyta ' ...
        %         '--good-runs 500  --total-runs 2500 --runs-pr-state ' ...
        %         '250  --eval-runs 50 --filter 0 '];  
        %this one should be very fast 
        com1 = ['time ~/bin/stratego/bin-Linux/verifyta ' ...
                '--good-runs 30  --total-runs 100 --runs-pr-state ' ...
                '15  --eval-runs 15 --filter 0 '];
        learMetStr = sprintf(' --learning-method %d ', learningMet);
        com1 = strcat(com1,learMetStr)
        %this one takes parameters from input.
        % com1 = ['~/bin/stratego-experimental/bin-Linux/verifyta ' ...
        %         '--filter 0 --max-iterations 50 --reset-no-better 100'];
        % nrRuns = env.nrRuns;
        % runsStr = sprintf([' --good-runs %d --total-runs %d ' ...
        %                    '--runs-pr-state %d --eval-runs %d'] ,nrRuns,nrRuns,nrRuns,nrRuns); 
        % paramStr = sprintf(' --max-reset-learning %d', env.max_reset_learning);
        % learMetStr = sprintf(' --learning-method %d', learningMet);
        % com1 = sprintf('%s %s %s
        % %s',com1,learMetStr,runsStr,paramStr)
        queryStr = env.queryStr;
        command = strcat(com1,';;;',model,';;;',queryStr);
        command = strrep(command, ';;;', ' ');
        fprintf(command);
        [status,cmdout] = unix(command,'-echo');
        out = cmdout;
    end

    
    function strategy = extractStrategy(cmdout)
        strategyAns = zeros(1,nrOfSteps);     
        for i=1:nrOutputs
            str_to_find = sprintf('curr_speed:');    
            str_next_to_find = sprintf('\n');
            ka = strfind(cmdout,str_to_find);
            ka_str = cmdout((ka+size(str_to_find,2)+2):end);
            kb = strfind(ka_str,str_next_to_find);            
            cell_ans(i) = {ka_str(1:kb)};            
            %now build a strategy from a single string of the form
            %(0,0) (0,0) (0,1) (0,1) (15,1) (15,1) (15,0) (15,0)
            %(60,0)                        
            strategy_i = extract_single_strategy(char(cell_ans(i)));            
            strategyAns = cat(1,strategyAns,strategy_i);
        end
        strategy = strategyAns(2:end,:);
    end

    
    function single_strategy = ...
            extract_single_strategy(strategy_str)
        fprintf('extract_single_strategy %s \n',strategy_str);
        strategy_ans = zeros(1,env.nrSteps);
        len = size(strategy_str,2);
        last = 0; % meaning last time valve was set to 0
        time = 0;
        for i=1:env.nrSteps
            strToFind = strcat('(',num2str(time),',');
            pos = strfind(strategy_str,strToFind);
            if ( size(pos,2) > 0 )
                pos = pos(end);
                str_val_value = strategy_str( pos + (size(strToFind,2) ...
                                                     ) );
                val_value = str2num(str_val_value);   
            else 
                fprintf('output not found at time %d taking last', time);
                val_value = last;
            end             
            last = val_value;
            strategy_ans(i) = val_value;
            time = env.stepSize*i;
        end
        single_strategy = strategy_ans;
    end

    function norStrategy = normalizeStrategy(strategy)
    %tstep is the switching control step e.g. 15
        tStep = env.controlStep;
        if env.stepSize ~= tStep 
            fprintf(['normalizing strategy']);
            if mod(env.stepSize,tStep) ~= 0 || env.stepSize < tStep
                fprintf(['fail: step size has to be a multiple and ' ...
                         'bigger than tstep']);
                error('wrong in step size check')
            else
                rate = env.stepSize / tStep;
                norStrategy = zeros(size(strategy,1),size(strategy,2)*rate);
                nSindex = 0;
                for i=1:size(strategy,2)
                    nSindex = ((i-1)*rate);
                    for j=1:rate
                        for k=1:size(strategy,1)
                            norStrategy(k,nSindex+j) = strategy(k,i);
                        end
                    end
                end
            end
        else
            norStrategy = strategy;
        end
    end

end