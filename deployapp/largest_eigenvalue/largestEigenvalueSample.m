function a = largestEigenvalueSample(N,M)

% Typical values are
% N = 100 (trials)
% M = 200 (size of matrix)

% From commandline, arguments come in as strings
N = str2num(N);
M = str2num(M);

a = zeros(N,1); 

tic; % serial for-loop 
for I = 1:N 
    a(I) = largestEigenvalue(M); 
end
t = toc;

disp(['Time for serial calculation: ', num2str(t), ' seconds.'])
dlmwrite('largest_eigenvalues.txt',a);


function y = largestEigenvalue(M)

%%Seed random stream if desired
%%RandStream.setGlobalStream(RandStream('mt19937ar','seed',seed));
y = max(eig(rand(M)));