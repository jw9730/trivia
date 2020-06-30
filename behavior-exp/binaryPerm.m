function [seq] = binaryPerm(n,k)
% Generates a random binary sequence made up of n 0s and n 1s,
% Allowing up to k repetition of same number, in O(n^2) time.
% binarySeq(3,2) can generate:
%   [1 1 0 1 0 0]
%   [0 1 0 1 1 0], etc.

% This code uses an algorithm somewhat simillar to typical dynamic programming scheme
A = ones(n+1,n+1);
seq = zeros(1,2*n);

% Marking "Zone-O-death"s (forbidden zone)
for ii = n+1:-1:1
    if (n-k)-k*(n+1-ii)>0
        for jj = (n-2)-2*(n+1-ii):-1:1
            A(ii,jj) = 0;
            A(jj,ii) = 0;
        end
    end
end

% Random (right or down) traverse along the matrix,
% Proceeding to the southeastern end

% 1 + # of down / right moves including current one
D0 = 1; R1 = 1;
% # of repeated moves including current one
cnt = 0;

% First move
seq(1) = randi(2)-1; % New element
if seq(1) % Moving right
    R1 = R1+1;
    fprintf('Right\t[%d,%d]\n',D0,R1);
else % Moving down
    D0 = D0+1;
    fprintf('Down\t[%d,%d]\n',D0,R1);
end

% Second to last move
for ii = 2:2*n
    seq(ii) = randi(2)-1;
    if seq(ii)==seq(ii-1) % Repeated movement
        cnt = cnt+1;
    end
    if seq(ii) % Moving right
        R1 = R1+1;
        if R1>n+1 || ~A(D0,R1) || (cnt>k-1)
        % If current movement leads to forbidden zone / is kth repeated move / array range is exceeded
            seq(ii) = 1-seq(ii); % Change the current element
            R1 = R1-1; D0 = D0+1; % Swap the current movement
            cnt = 0;
        end
        if seq(ii) % Display current move
            fprintf('Right\t[%d,%d]\n',D0,R1);
        else
            fprintf('Down\t[%d,%d]\n',D0,R1);
        end
    else % Moving down
        D0 = D0+1;
        if D0>n+1 || ~A(D0,R1) || (cnt>k-1)
        % If current movement leads to forbidden zone / is kth repeated move / array range is exceeded
            seq(ii) = 1-seq(ii); % Change the current element
            R1 = R1+1; D0 = D0-1; % Swap the current movement
            cnt = 0;
        end
        if seq(ii) % Display current move
            fprintf('Right\t[%d,%d]\n',D0,R1);
        else
            fprintf('Down\t[%d,%d]\n',D0,R1);
        end
    end
end

if D0==n+1 && R1==n+1
    disp('Traversal complete');
    disp(seq);
else
    disp('Error: False traversal');
end
% After all traversal, current cell should be the last southeastern one
end