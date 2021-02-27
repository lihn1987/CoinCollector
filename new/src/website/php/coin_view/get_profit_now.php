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
$huobi_main_coin_list = ["ETH", "DOGE", "XRP", "ZEC", "ALGO", "LINK","DOT"];
$huobi_sub1_coin_list = ["XLM","EOS","UNI","1INCH", "CRV","SNX","NEO"];
$redis = new Redis();
$redis->connect('redis', 6379);
$sql = "
    select * from trade_now";
$result = $conn->query($sql);
 
if ($result->num_rows > 0) {
    // 输出数据
    while($row = $result->fetch_assoc()) {
        if($row["tag"] == "huobi_1"){
            //var_dump($row);
            array_push($rtn["huobi_main"],[
                "coin_order"=>$row["coin_order"],
                "coin_base"=>$row["coin_base"],
                "dir"=>$row["dir"],
                "profit"=>$row["profit"],
                "profit_rate"=>$row["profit_rate"],
                "position_margin"=>$row["position_margin"]
            ]);
        }else if ($row["tag"] == "huobi_2"){
            //var_dump($row);
            array_push($rtn["huobi_sub1"],[
                "coin_order"=>$row["coin_order"],
                "coin_base"=>$row["coin_base"],
                "dir"=>$row["dir"],
                "profit"=>$row["profit"],
                "profit_rate"=>$row["profit_rate"],
                "position_margin"=>$row["position_margin"]
            ]);
        }
    }
} else {
    //echo "0 结果";
}

echo json_encode($rtn);
?>