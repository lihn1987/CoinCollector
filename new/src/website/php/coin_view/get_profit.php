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


$rtn = ["huobi_main"=>[], "huobi_sub1"=>[]];
$huobi_main_coin_list = ["DOGE", "XRP", "ZEC", "ALGO", "LINK","DOT"];
$huobi_sub1_coin_list = ["DOGE", "XRP", "ZEC", "ALGO", "LINK","DOT"];
$redis = new Redis();
$redis->connect('redis', 6379);
for($i = 0; $i < sizeof($huobi_main_coin_list); $i++){
    $item = [];
    $item["latest_time"] = time() - ((int)$redis->get("{$huobi_main_coin_list[$i]}-USDT-1-latest_time"));
    $item["coin_name"] = $huobi_main_coin_list[$i];
    $item["amount"] = 0;
    $item["profit"] = 0;
    $item["profit_sell"] = 0;
    $item["profit_buy"] = 0;
    $item["count"] = 0;
    array_push($rtn["huobi_main"], $item);
}

for($i = 0; $i < sizeof($huobi_sub1_coin_list); $i++){
    $item = [];
    $item["latest_time"] = time() - (int)$redis->get("{$huobi_sub1_coin_list[$i]}-USDT-2-latest_time");
    $item["coin_name"] = $huobi_sub1_coin_list[$i];
    $item["amount"] = 0;
    $item["profit"] = 0;
    $item["profit_sell"] = 0;
    $item["profit_buy"] = 0;
    $item["count"] = 0;
    array_push($rtn["huobi_sub1"], $item);
}

$time = strtotime(date("Y-m-d"))*1000;
//echo $time;
$sql = "
select 
coin_order,dir,
count(*) as `count`,
sum(profit) as `profit`,
sum(amount) as `amount`
from 
trade_history 
where 
`timestamp`>$time
and tag = 'huobi_1'
group by coin_order,dir
order by coin_order";
$result = $conn->query($sql);
 
if ($result->num_rows > 0) {
    // 输出数据
    while($row = $result->fetch_assoc()) {
        //echo "id: " . $row["id"]. " - Name: " . $row["firstname"]. " " . $row["lastname"]. "<br>";
        for($i = 0; $i < sizeof($rtn["huobi_main"]); $i++){
            if($rtn["huobi_main"][$i]["coin_name"] == $row["coin_order"]){
                if(!array_key_exists("amount", $rtn["huobi_main"][$i])){
                    $rtn["huobi_main"][$i]["amount"] = (float)$row["amount"];
                }else{
                    $rtn["huobi_main"][$i]["amount"] += (float)$row["amount"];
                }
                if(!array_key_exists("count", $rtn["huobi_main"][$i])){
                    $rtn["huobi_main"][$i]["count"] = (float)$row["count"];
                }else{
                    $rtn["huobi_main"][$i]["count"] += (float)$row["count"];
                }
                if(!array_key_exists("profit", $rtn["huobi_main"][$i])){
                    $rtn["huobi_main"][$i]["profit"] = (float)$row["profit"];
                }else{
                    $rtn["huobi_main"][$i]["profit"] += (float)$row["profit"];
                }
                if($row["dir"] == 3){
                    $rtn["huobi_main"][$i]["profit_buy"] = (float)$row["profit"];
                }
                if($row["dir"] == 4){
                    $rtn["huobi_main"][$i]["profit_sell"] = (float)$row["profit"];
                }
            }
        }
    }
} else {
    //echo "0 结果";
}

$sql = "
select 
coin_order,dir,
count(*) as `count`,
sum(profit) as `profit`,
sum(amount) as `amount`
from 
trade_history 
where 
`timestamp`>$time
and tag = 'huobi_2'
group by coin_order,dir";
$result = $conn->query($sql);
 
if ($result->num_rows > 0) {
    // 输出数据
    while($row = $result->fetch_assoc()) {
        //echo "id: " . $row["id"]. " - Name: " . $row["firstname"]. " " . $row["lastname"]. "<br>";
        for($i = 0; $i < sizeof($rtn["huobi_sub1"]); $i++){
            if($rtn["huobi_sub1"][$i]["coin_name"] == $row["coin_order"]){
                if(!array_key_exists("amount", $rtn["huobi_sub1"][$i])){
                    $rtn["huobi_sub1"][$i]["amount"] = (float)$row["amount"];
                }else{
                    $rtn["huobi_sub1"][$i]["amount"] += (float)$row["amount"];
                }
                if(!array_key_exists("count", $rtn["huobi_sub1"][$i])){
                    $rtn["huobi_sub1"][$i]["count"] = (float)$row["count"];
                }else{
                    $rtn["huobi_sub1"][$i]["count"] += (float)$row["count"];
                }
                if(!array_key_exists("profit", $rtn["huobi_sub1"][$i])){
                    $rtn["huobi_sub1"][$i]["profit"] = (float)$row["profit"];
                }else{
                    $rtn["huobi_sub1"][$i]["profit"] += (float)$row["profit"];
                }
                if($row["dir"] == 3){
                    $rtn["huobi_sub1"][$i]["profit_buy"] = (float)$row["profit"];
                }
                if($row["dir"] == 4){
                    $rtn["huobi_sub1"][$i]["profit_sell"] = (float)$row["profit"];
                }
            }
        }
    }
} else {
    //echo "0 结果";
}


echo json_encode($rtn);
?>