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
$rtn = [];
$data=file_get_contents("php://input");
$data = json_decode($data, TRUE);
$start_time = $data["data"]["start_time"];
$coin_name = $data["data"]["coin_name"];
$statistic_type = $data["data"]["statistic_type"];
$key=$data["data"]["key"];

$coin_name_str =  "";
if($coin_name != 'ALL'){
    $coin_name_str = " and coin_order = '$coin_name' ";
}
$sql = "select sum(amount) as amount, sum(profit) as profit, count(*) as count ,date_format(FROM_UNIXTIME((timestamp+1000*60*60*8)/1000), '%Y-%m-%d') as time
from trade_history 
where tag='$key' and timestamp >= $start_time
$coin_name_str
group by 
date_format(FROM_UNIXTIME((timestamp+1000*60*60*8)/1000), '%Y-%m-%d') order by timestamp;";

$result = $conn->query($sql);
while($row = $result->fetch_assoc()) {
    array_push($rtn, [
        "profit"=>$row["profit"],
        "amount"=>$row["amount"],
        "count"=>$row["count"],
        "time"=>$row["time"]
    ]);
}



echo json_encode($rtn);
