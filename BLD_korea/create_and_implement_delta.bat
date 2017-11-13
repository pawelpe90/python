@echo off

echo "Running bld_extractor.py"
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_extractor\bld_extractor.py %*

echo "Running bld_delta_provider.py"
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_delta_provider\bld_delta_provider.py %*

echo "Running bld_clean_delta.py"
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_clean_delta\bld_clean_delta.py %*

echo "Processing done!"

pause