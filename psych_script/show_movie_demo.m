close all
clear
clc

root = pwd;

PsychDefaultSetup(1);
Screen('CloseAll')
Screen('Preference', 'SkipSyncTests', 0);

fixSize = 3;
sKey = KbName('s');

screenNum = max(Screen('Screens'));
theFrameRate = FrameRate(screenNum);
% find the color values which correspond to white and black
white = WhiteIndex(screenNum);
black = BlackIndex(screenNum);
gray = GrayIndex(screenNum);

% open window
[windowPtr, rect] = Screen('OpenWindow', screenNum, gray);
% sets Center for screenRect (x,y)
[x0, y0] = RectCenter(rect);
% set fixation spot rect
fixRect = [x0-fixSize, y0-fixSize, x0+fixSize, y0+fixSize];

% while 1
%     [keyIsDown, ~, keyCode] = KbCheck;
%     if keyIsDown && keyCode(sKey)
%         % start only when "s" key is pressed
%         break;
%     end
% end

motion_names = {'shenchu', 'taiqi', 'waizhan', 'quzhou'}
for mn = 1 : length(motion_names)
    motion_name = motion_names{mn}
    
    colors = eye(3) * 255;
    for j = 1 : 3
        Screen('FillRect', windowPtr, colors(j, :), fixRect);
        Screen('Flip', windowPtr);
        pause(1)
    end
    
    fname = fullfile(root, '..', 'movies',...
        sprintf('%s.mp4', motion_name))
    [movie, dur, ~, imgw, imgh] = Screen('OpenMovie', windowPtr, fname);
    Screen('PlayMovie', movie, dur/4);
    j = 0;
    all_img = nan(imgh+1, imgw+1, 3, 500);
    while 1
        tex = Screen('GetMovieImage', windowPtr, movie);
        if tex<=0
            break;
        end
        Screen('DrawTexture', windowPtr, tex);
        Screen('Flip', windowPtr);
        imageArray = Screen('GetImage', windowPtr);
        j = j + 1
        all_img(:, :, :, j) = imageArray(...
            y0-imgh/2:y0+imgh/2, x0-imgw/2:x0+imgw/2, :);
        Screen('Close', tex);
    end
    num = j;
    all_img = all_img(:, :, :, 1:num);
    Screen('PlayMovie', movie, 0);
    Screen('CloseMovie', movie);
    
    movie_4D = uint8(all_img);
    save(fullfile(root, 'movie_in_img4D', sprintf('%s.mat', motion_name)), 'movie_4D')
    
    for j = 1 : num
        imageTexture = Screen('MakeTexture', windowPtr, all_img(:, :, :, j));
        Screen('DrawTexture', windowPtr, imageTexture, [], [], 0);
        Screen('Flip', windowPtr);
        pause(4/num)
    end
    
end
Screen('CloseAll')


