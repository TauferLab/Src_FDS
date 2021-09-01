close all
clear all
load whole.mat

Whole2 = Whole;

Whole2(1:183,2) = 2*Whole(1:183,2);

Whole2(184:287,2) = 0.7*Whole(184:287,2);

plot(Whole(:,2),'b')

hold on

plot(Whole2(:,2),'r')