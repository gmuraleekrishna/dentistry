im = imread('tooth_top.png');
points = roipoly(im);
close
area = sum(sum(points))

