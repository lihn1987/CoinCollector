<?php
/*
$market = strtoupper($_GET["market"]);
$order_coin = strtoupper($_GET["order_coin"]);
$base_coin = strtoupper($_GET["base_coin"]);

$rtn = ["result"=>TRUE, "data"=>[]];
$redis = new Redis();
$redis->connect('redis', 6379);

$key = "$order_coin-$base_coin-$market-DEPTH";

$res = $redis->get($key);
$rtn["data"] = json_decode($res);

echo json_encode($rtn);*/
$rtn = ["result"=>TRUE, "data"=>[]];
$redis = new Redis();
$redis->connect('redis', 6379);
$res = $redis->keys("HAIGUI-*-is_buy");
for($i = 0; $i < sizeof($res); $i++){
    $list = explode("-", $res[$i]);
    $order_coin = $list[1];
    $base_coin = $list[2];
    $is_buy = $redis->get("HAIGUI-$order_coin-$base_coin-HUOBI-1min-is_buy");
    $amount = $redis->get("HAIGUI-$order_coin-$base_coin-HUOBI-1min-amount");
    $price = $redis->get("HAIGUI-$order_coin-$base_coin-HUOBI-1min-price");
    $profit = $redis->get("HAIGUI-$order_coin-$base_coin-HUOBI-1min-profit");
    $all = 0;
    if($is_buy){
        $str = $redis->get("$order_coin-$base_coin-HUOBI-DEPTH");
        
        $data = json_decode($str, true);
        $all = $data["forbuy"][0][0]*$amount;
        
    }else{
        $all = $amount;
    }
    array_push($rtn["data"], array("order_coin"=>$order_coin, "base_coin"=>$base_coin, "is_buy"=>$is_buy?"买":"卖", "amount"=>$amount, "price"=>$price, "profit"=>$profit, "all"=>$all));
}
echo json_encode($rtn);
?>