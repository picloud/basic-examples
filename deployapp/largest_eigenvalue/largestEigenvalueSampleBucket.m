function a = largestEigenvalueSampleBucket(data_source)

% Typical values are
% N = 100 (trials)
% M = 200 (size of matrix)

% Download data from bucket
safeSystem(['picloud bucket get ', data_source, ' .'])
% Load data; it is formatted as a vector of [N M]
data = dlmread(data_source)
N = data(1)
M = data(2)

a = zeros(N,1); 

tic; % serial for-loop 
for I = 1:N 
    a(I) = largestEigenvalue(M); 
end
t = toc;

disp(['Time for serial calculation: ', num2str(t), ' seconds.'])

% Save largest eigenvalues of each matrix to a file
dlmwrite('largest_eigenvalues.txt',a);
% Push file to bucket
safeSystem('picloud bucket put largest_eigenvalues.txt largest_eigenvalues.txt')

function y = largestEigenvalue(M)

%%Seed random stream if desired
%%RandStream.setGlobalStream(RandStream('mt19937ar','seed',seed));
y = max(eig(rand(M)));
