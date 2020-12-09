function [Tenv,Irr] = loadWeather(strWeather)    
%strWeather = 'data/DRY_merged_6197.csv';
    hoursMonth = 24 * 30;
    allWeather = csvread(strWeather);
    Tenv = allWeather(1:hoursMonth,1)';
    Irr = allWeather(1:hoursMonth,3)';
    Tenv = normalizeWeather(Tenv);
    Irr = normalizeWeather(Irr);
    
    function vec15min = normalizeWeather(vec1hour)
        n = 4;
        r = repmat(vec1hour, n, 1);
        vec15min = r(:);
    end   
end