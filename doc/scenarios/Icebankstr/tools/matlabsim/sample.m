A = [0.1 -0.2; 0.3 0.4];
B = [0.4; 0.5];
x0 = [0.1; 0.2];                                                    % Initial Conditions Vector For ‘ode45’
SysFun = @(t,x,u) A*x + B*u;                                        % Dynamical System Differential Equation
T = 5;                                                              % Length (Time Units) Of Each Segment
Td = 10;                                                            % Length Of ‘tspan’ Vector For Each Time Segment (Number Or Elements In The Vector)
tspan = linspace(0, T, Td);
for i=1:50                                                          % Choose Number Of Time Segments (Here, 50)
    u = (i^4*(-1)^i);                                               % Choose Appropriate Input For Each Time Interval
    [t(:,i),x(:,:,i)]=ode45(@(t,x) SysFun(t,x,u),tspan,x0);
    x0=x(end,:,i);
    tspan = linspace(t(end,i), t(end,i)+T, Td);
    uv(i) = u;
end
tv = reshape(t, [], 1);                                             % Aggregate Time Vector
xp = permute(x, [1 3 2]);                                           % Permute ‘x’
xv = reshape(xp, [], size(x,2));                                    % Correctly-Formatted Output Matrix For ‘x’, Matching ‘tv’
figure(1)
plot(tv, xv)
grid
