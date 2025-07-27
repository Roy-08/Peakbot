<?php

$python_path = "\"C:\\Program Files\\Python311\\python.exe\""; 
$app_path = "\"C:\\xampp\\htdocs\\Peakbot\\app.py\""; 

$command = "start /B ".$python_path." ".$app_path." >nul 2>&1";

pclose(popen($command, "r"));
sleep(9);

header("Location: http://127.0.0.1:5000");
exit();
?>
