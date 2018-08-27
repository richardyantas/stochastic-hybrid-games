function [V,steps] = strategoController(ibc,env)
    verNr1 = 1; 
    model1 = createStrategoModel(ibc,env);    
    [V1,strSteps] = callStratego(ibc,env,model1);
    V = V1(1);
    steps = 1;    
end