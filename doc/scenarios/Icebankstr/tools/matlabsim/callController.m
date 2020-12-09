function [p,len] = callController(ibc,env)    
    switch(env.controller)
      case ControllerClass.naive
        [p,len] = pumpNaiveController(ibc,env);
      case ControllerClass.stratego
        [p,len] = strategoController(ibc,env);            
      otherwise
        warning('Unexpected controller type.');
    end
end
