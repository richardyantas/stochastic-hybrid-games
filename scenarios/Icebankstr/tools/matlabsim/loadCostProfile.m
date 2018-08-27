function C = loadCostProfile(strCostProfile)    
    
%strCostProfile = 'data/elspot-prices_2018_hourly_dkk.csv';
    hoursMonth = 24 * 30;
    allData = csvread(strCostProfile);
    C = allData(1:hoursMonth,8)';
    C = normalizeData(C);

% $$$     
% $$$     totalDays = 30;
% $$$     tspan = linspace(0,totalDays,totalDays*24*);
% $$$     
% $$$     
% $$$     switch strCostProfile
% $$$       case 'sinusoid'
% $$$         costKWh = getSinusoid(ti);
% $$$       case 'constant'
% $$$         costKWh = 2.33;
% $$$       otherwise
% $$$     end    
% $$$ 
% $$$ 
% $$$     function sinCost = getSinusoid(ti)
% $$$     %we model a temperature of 10C with min 0C and max 20C. The
% $$$     %period is one day, independent variable is in minutes. Weather
% $$$     %computed for 4 days
% $$$         secsPerDay = 60*24*60;        
% $$$         baseCost = 2.33;
% $$$         sinCost = 1*sin(2*pi/secsPerDay*ti)+baseCost;
% $$$     end

    function vec15min = normalizeData(vec1hour)
        n = 4;
        r = repmat(vec1hour, n, 1);
        vec15min = r(:);
    end   
    
end