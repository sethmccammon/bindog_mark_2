% Script for plotting results for SDM project

clear
clc
close all

load('wkr_12_auction.mat')
load('wkr_12_greedy.mat')
load('wkr_12_replan.mat')

x = [2,4,6,8,10,12,14,16,18,20];

figure()

errorbar(x,wkr_12_picked_mean_greedy,wkr_12_picked_std_greedy);

hold on

errorbar(x,wkr_12_picked_mean_auction,wkr_12_picked_std_auction);
errorbar(x,wkr_12_picked_mean_replan,wkr_12_picked_std_replan);

legend({'greedy', 'auction', 'replan'}, 'FontSize', 16, 'Location', 'southeast')
xlim([0 22])
title('Percentage of Apples Picked', 'FontSize', 24)
xlabel('Number of Robots', 'FontSize', 16)
ylabel('Percentage of Apples Picked', 'FontSize', 16)

hold off

figure()

errorbar(x,wkr_12_time_mean_greedy,wkr_12_time_std_greedy);

hold on

errorbar(x,wkr_12_time_mean_auction,wkr_12_time_std_auction);
errorbar(x,wkr_12_time_mean_replan,wkr_12_time_std_replan);

legend({'greedy', 'auction', 'replan'}, 'FontSize', 16)
xlim([0 22])
title('Idle Worker Time', 'FontSize', 24)
xlabel('Number of Robots', 'FontSize', 16)
ylabel('Time Steps Workers Did Not Pick', 'FontSize', 16)

hold off