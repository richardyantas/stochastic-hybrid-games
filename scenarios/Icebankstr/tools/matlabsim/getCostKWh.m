function costKWh = getCostKWh(cost,ti)
%cost is a vector with costs per 15 minutes
%ti is current time in seconds
    tax = 10;
    index = ceil((ti+1)/(60*15));
    costKWh = (cost(index)/1000)*tax;
    
    
    
    % switch strCost
    %   case 'sinusoid'
    %     costKWh = getSinusoid(ti);
    %   case 'constant'
    %     costKWh = 2.33;
    %   otherwise
    %     error('cost not defined');
    % end    


    % function sinCost = getSinusoid(ti)
    % %we model a temperature of 10C with min 0C and max 20C. The
    % %period is one day, independent variable is in minutes. Weather
    % %computed for 4 days
    %     secsPerDay = 60*24*60;        
    %     baseCost = 2.33;
    %     sinCost = 1*sin(2*pi/secsPerDay*ti)+baseCost;
    % end

end