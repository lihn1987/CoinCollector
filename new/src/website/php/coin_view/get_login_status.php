<?php
session_start();
$rtn = ["result" => -1];
//var_dump($_SESSION);
if(key_exists("username", $_SESSION) && key_exists("id", $_SESSION)){
    $rtn["username"] = $_SESSION["username"];
    $rtn["id"] = $_SESSION["id"];
    $rtn["result"] = 0;
}
echo json_encode($rtn);
?>