function [verts, faces]=dispObj(obj)
%
% function display_obj(obj)
%
% displays a TEXTURELESS obj structure
%
% INPUTS:  obj:     object data
%                   - obj.v:    vertices
%                   - obj.vt:   texture coordinates
%                   - obj.f.v:  face definition vertices
%                   - obj.f.vt: face definition texture
%
% Modified by Alutsyah Luthfian (2018)
% Original Author: Bernard Abayowa
% University of Dayton
% 6/16/08
cntr=mean(obj.v,1);
tval=zeros(size(obj.v,1),1);
for i=1:size(obj.v,1)
    tval(i,1)=norm(obj.v(i,:)-cntr);
end
% display object

obj.f.v(obj.f.v==0) = nan;
fv = obj.f.v;
fv = [];
c = ([-6.50, 2.40, 0.05] + [-13.56, -2.75, 1.92]) / 2;
ll = norm(c - [-6.50, 2.40, 0.05]) * 1.1;
for j = 1 : size(obj.f.v, 1)
    x = obj.f.v(j, :);
    for e = x
        if isnan(e)
            continue
        end
        if norm(obj.v(e, :) - c) < ll
            fv = [fv; x];
        end
    end
end
figure
p=patch('vertices',obj.v,'faces', fv,'FaceVertexCData', tval);

shading interp
colormap jet;
colormap bone;
lighting phong;
camlight('right');
camproj('perspective');
axis square;
axis off;
axis equal
axis tight;
%cameramenu
cameratoolbar
verts=get(p,'Vertices');
faces=get(p,'Faces');
