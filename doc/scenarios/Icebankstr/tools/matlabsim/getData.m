function data = getData(datavec,ti)
%datavec is a vector of data e.g. irradiance, out temp, every 15
%minutes.  ti is current time in seconds
    index = ceil((ti+1)/(60*15));
    data = datavec(index);
    
end