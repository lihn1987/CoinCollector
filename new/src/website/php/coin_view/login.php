<?php
$servername = "mysql";
$username = "root";
$password = "123456";
$dbname = "coin";
$rtn = ["result"=>-1];
// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}
session_start();
$param = json_decode(file_get_contents("php://input"),true);

$sql = $conn->prepare("select id,username from user where username=? and password=?");
$sql->bind_param("ss", $param["username"], $param["password"]);
$result = $sql->execute();
$sql->store_result();
$sql->bind_result($id, $username);
while ($sql->fetch()){
    $_SESSION["id"] = $id;
    $_SESSION["username"] = $param["username"];
}
//登录成功
if($sql->num_rows == 1){
    $rtn["result"] = 0;
}

echo json_encode($rtn);
?>