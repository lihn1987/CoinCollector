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

$page_index = $_GET["page_index"]*10;

$sql = "
select SQL_CALC_FOUND_ROWS
    coin_order, coin_base, dir, profit, amount, timestamp 
from 
    trade_history 
where tag='{$_GET['tag']}'
order by `timestamp` desc
limit $page_index, 10";

$result = $conn->query($sql);
$rtn = ["page_size"=>0, "data"=>[]];
while($row = $result->fetch_assoc()) {
    $row["timestamp"] = date("Y-m-d H:i:s", $row["timestamp"]/1000);
    array_push($rtn["data"],[
        "coin_order"=>$row["coin_order"],
        "coin_base"=>$row["coin_base"], 
        "dir"=>$row["dir"], 
        "profit"=>$row["profit"], 
        "amount"=>$row["amount"], 
        "timestamp"=>$row["timestamp"] 
    ]);
}

$sql = "SELECT found_rows() AS rowcount;";

$result = $conn->query($sql);
while($row = $result->fetch_assoc()) {
    $rtn["page_size"] = $row["rowcount"];
}
echo json_encode($rtn);
?>