<?php
$servername = "mysql";
$username = "root";
$password = "123456";
$dbname = "coin";
 
// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
} 



$sql = "
    (select * from amount_history where tag = 'huobi_1' order by timestamp desc limit 0,1)
    union
    (select * from amount_history where tag = 'huobi_2' order by timestamp desc limit 0,1);

";
$result = $conn->query($sql);

$rtn = ["result"=>"ok", "data"=>[]];
if ($result->num_rows > 0) {
    // 输出数据
    while($row = $result->fetch_assoc()) {
        array_push($rtn["data"], $row["amount"]);
    }
} else {
    //echo "0 结果";
}


echo json_encode($rtn);
?>