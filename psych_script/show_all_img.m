close all
clear
clc

load all_img.mat
all_img = uint8(all_img);

idx = floor(linspace(1, 75, 10));

figure
for j = 1 : length(idx)
    subplot(3, 4, j)
    imshow(all_img(:, :, :, idx(j)))
    title(idx(j))
end