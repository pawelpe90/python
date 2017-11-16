@echo off

echo Running bld_extractor.py
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_extractor\bld_extractor.py %*
echo. 

 
echo Running bld_delta_provider.py
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_delta_provider\bld_delta_provider.py %*
echo.

 
echo Running bld_clean_delta.py
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_clean_delta\bld_clean_delta.py %*
echo.


echo Running bld_remove_delta.py
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_delta_handler\bld_remove_delta.py %*
echo.


echo Running bld_prepare_delta.py
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_delta_handler\bld_prepare_delta.py %*
echo.


echo Starting BGS...

FOR %%x IN (incheon) DO (
	set JAVA_OPTS=-Xms32m -Xmx4096m -Xss4m
	set SCRIPTPATH=%~dp0
	java %JAVA_OPTS% -cp "%SCRIPTPATH%configuration";"%SCRIPTPATH%buildings-geometry-simplifier-jar-with-dependencies.jar" com.tomtom.display.simplifier.core.Runner -bldPath C:\Users\pruszyns\Desktop\output\%%x\kor_%%x_bufo.shp -outputPath C:\Users\pruszyns\Desktop\output\%%x\bld -logPath C:\Users\pruszyns\Desktop\logs -adjoiningBuffer 0.15 -snappingTolerance 0.11 -reductionPrecision 1e7 -hausdorffDistanceTolerance 0.15 -edgeSimplifyGeometry -edgeSimplifyTolerance 0.1 -utmZone 52N%*
	echo BGS finished for %%x
	echo.
)

echo Processing done!

pause