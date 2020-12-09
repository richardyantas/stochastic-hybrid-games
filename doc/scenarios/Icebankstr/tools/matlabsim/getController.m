function [instantControlling,controller] = ...
        getController(controllerStr)
    instantControlling = true;
    switch(controllerStr)
      case 'naive'
        controller = ControllerClass.naive;
      case 'stratego'
        instantControlling = false;
        controller = ControllerClass.stratego;
      otherwise
        warning('Unexpected controller type.');            
    end     
end