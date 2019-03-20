close all
clear
clc

% obj = readwObj(fullfile('objs', '12682_arm_v1_FINAL.obj'));

obj = readwObj(fullfile('objs', 'malebody_BETA1.obj'));

% obj = readwObj(fullfile('objs', 'isa_BP3D_4.0_obj_99', 'FJ3207.obj'));

[verts, faces] = dispObj(obj);

save(fullfile('parts', 'body_f.txt'), 'faces', '-ascii')
save(fullfile('parts', 'body_v.txt'), 'verts', '-ascii')
