close all
clear
clc

PsychDefaultSetup(1);
Screen('CloseAll')
Screen('Preference', 'SkipSyncTests', 1);

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
fixRect = [x0-fixSize y0-fixSize x0+fixSize y0+fixSize];

% while 1
%     [keyIsDown, ~, keyCode] = KbCheck;
%     if keyIsDown && keyCode(sKey)
%         % start only when "s" key is pressed
%         break;
%     end
% end

colors = eye(3) * 255;
for j = 1 : 3
    Screen('FillRect', windowPtr, colors(j, :), fixRect);
    Screen('Flip', windowPtr);
    pause(1)
end

fname = fullfile('c:\Users\liste\Documents\model_3d_test\movies\', 'quzhou.mp4')
[movie, dur, ~, imgw, imgh] = Screen('OpenMovie', windowPtr, fname);
Screen('PlayMovie', movie, 10);
while 1
    tex = Screen('GetMovieImage', windowPtr, movie);
    if tex<=0
        break;
    end
    Screen('DrawTexture', windowPtr, tex);
    Screen('Flip', windowPtr);
    Screen('Close', tex);
end
Screen('PlayMovie', movie, 0);
Screen('CloseMovie', movie);
Screen('CloseAll')

