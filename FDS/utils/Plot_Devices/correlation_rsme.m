function [rmse,P,Mb] = correlation_rsme(XT,X,YT,Y, t0, tn)
% INPUT
% XT time of the variable X
% X  variable to compute the correlation
% YT time of the variable Y
% Y variable to compute the correlation
% t0 initial time
% tm final time
% OUTPUT
% rmse  root of mean square error
% P Pearson's correlation confficient
% Mb ; Mb(1) slope of the linear regression
%      Mb(2) intercept of the linear regression


Maximo = max(length(X), length(Y));

% Interpolation

t = linspace(t0,tn, Maximo);
[C,ia,~] = unique(XT);
XT = C;
X  = X(ia);

XS = spline(XT,X,t);


[C,ia,~] = unique(YT);
YT = C;
Y  = Y(ia);

YS = spline(YT,Y,t);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Regression

A = [XS' ones(length(XS),1)];
Mb = A\YS';
YL = Mb(1)*XS'+Mb(2);

plot(XS,YS,'.')
hold on
plot(XS',YL,'linewidth',2.0)

grid on


rmse = sqrt(sum((XS-YS).^2)/length(XS));

P=corrcoef(XS,YS);






