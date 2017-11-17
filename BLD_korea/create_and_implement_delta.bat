@echo off

set scope=busan changwon_si chungcheongbuk_do chungcheongnam_do daegu daejeon gangwon_do gwangju gyeonggi_do gyeongsangbuk_do gyeongsangnam_do incheon jeju_do jellanam_do jeollabuk_do sejong_si seongnam_si seoul suwon_si ulsan yongin_si

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


FOR %%x IN (%scope%) DO (
	echo Starting BGS for %%x...
	echo.
	set JAVA_OPTS=-Xms32m -Xmx4096m -Xss4m
	set SCRIPTPATH=%~dp0
	java %JAVA_OPTS% -cp "%SCRIPTPATH%configuration";"%SCRIPTPATH%buildings-geometry-simplifier-jar-with-dependencies.jar" com.tomtom.display.simplifier.core.Runner -bldPath C:\Users\pruszyns\Desktop\output\%%x\kor_%%x_bufo.shp -outputPath C:\Users\pruszyns\Desktop\output\%%x\bld -logPath C:\Users\pruszyns\Desktop\logs -adjoiningBuffer 0.15 -snappingTolerance 0.11 -reductionPrecision 1e7 -hausdorffDistanceTolerance 0.15 -edgeSimplifyGeometry -edgeSimplifyTolerance 0.1 -utmZone 52N%*
	echo BGS finished for %%x
	echo.
)

echo Running bld_append_delta.py
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_delta_handler\bld_append_delta.py %*
echo.


echo Running bld_prepare_validation.py
python C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_prepare_validation\bld_prepare_validation.py %*
echo.


FOR %%x IN (%scope%) DO (
	echo Starting BVT for %%x...
	echo.
	buildings-layer_start.bat -display console -cityDir C:\city\Building_layer\02_operations\XX_validation\%%x -cityName %%x -countrycode kor
	echo BVT finished for %%x
	echo.
)

echo Processing done!
echo.

pause