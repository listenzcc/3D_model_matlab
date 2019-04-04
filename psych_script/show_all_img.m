close all
clear
clc

PsychDefaultSetup(1);
Screen('CloseAll')
Screen('Preference', 'SkipSyncTests', 0);

fixSize = 3;
sKey = KbName('s');

screenNum = max(Screen('Screens'));
gray = GrayIndex(screenNum);
[windowPtr, rect] = Screen('OpenWindow', screenNum, gray);
[x0, y0] = RectCenter(rect);
fixRect = [x0-fixSize, y0-fixSize, x0+fixSize, y0+fixSize];
colors = eye(3) * 255;
for j = 1 : 3
    Screen('FillRect', windowPtr, colors(j, :), fixRect);
    Screen('Flip', windowPtr);
    pause(1)
end

while 1
    [keyIsDown, ~, keyCode] = KbCheck;
    if keyIsDown && keyCode(sKey)
        % start only when "s" key is pressed
        break;
    end
end



motion_names = {'shenchu', 'taiqi', 'waizhan', 'quzhou'}
for mn = 1 : length(motion_names)
    motion_name = motion_names{mn}
    load(fullfile('movie_in_img4D', sprintf('%s.mat', motion_name)))
    movie_4D = uint8(movie_4D);
    sz = size(movie_4D);
    num = sz(end)
    
    Screen('FillRect', windowPtr, colors(1, :), fixRect);
    Screen('Flip', windowPtr);
    pause(1)
    
    texs = nan(num, 1);
    for j = 1 : num
        imageTexture = Screen('MakeTexture', windowPtr, movie_4D(:, :, :, j));
        texs(j) = imageTexture;
    end
    
    for j = 1 : num
        Screen('DrawTexture', windowPtr, texs(j), [], [], 0);
        Screen('Flip', windowPtr);
        pause(2/num)
    end
    
    %     idx = floor(linspace(1, num, 12));
    %     figure
    %     for j = 1 : length(idx)
    %         subplot(3, 4, j)
    %         imshow(movie_4D(:, :, :, idx(j)))
    %         title(idx(j))
    %     end
    %     set(gcf, 'NumberTitle', 'off', 'Name', motion_name)
end

Screen('CloseAll')