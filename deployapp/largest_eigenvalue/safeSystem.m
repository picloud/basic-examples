
function retval = safeSystem(cmd)
% Execute system(cmd) with LD_LIBRARY_PATH set correctly

% Save library paths
MatlabPath = getenv('LD_LIBRARY_PATH');
% Make Matlab use system libraries
setenv('LD_LIBRARY_PATH','');
retval = system( cmd );
% Reassign old library paths
setenv('LD_LIBRARY_PATH',MatlabPath);