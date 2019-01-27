REM mysql -u root -p --verbose  < F:\git\md_length\utils\db.sql; 
IF "%DATABASE_URL%" == "" GOTO NOPATH 
:YESPATH
@ECHO The DATABASE_URL environment variable was detected.
@ECHO Overwriting environment variable. Check conflicts manually!
@ECHO Previous variable value %DATABASE_URL%
set DATABASE_URL=mysql+pymysql://length:k0lk2Kyla@localhost/length
GOTO END
:NOPATH
@ECHO The DATABASE_URL environment variable was NOT detected.
set DATABASE_URL=mysql+pymysql://length:k0lk2Kyla@localhost/length
GOTO END
:END
