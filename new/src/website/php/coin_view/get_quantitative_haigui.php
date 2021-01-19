<?php

$market = strtoupper($_GET["market"]);
$order_coin = strtoupper($_GET["order_coin"]);
$base_coin = strtoupper($_GET["base_coin"]);

$rtn = ["result"=>TRUE, "data"=>[]];
$redis = new Redis();
$redis->connect('redis', 6379);


$key_list = [
    "max_profit",
    "best_buy_width_range",
    "best_buy_point",
    "best_sell_point_low",
    "best_sell_point_hight",
    "normal_profit"
];
$kline_list = [
    "1min", "5min", "15min", "30min", "60min", "4hour"
];
for($kline_index = 0; $kline_index < sizeof($kline_list); $kline_index++){
    $rtn["data"][$kline_list[$kline_index]] = [];
    for($i = 0; $i < sizeof($key_list); $i++){
        $key = "HAIGUI-$order_coin-$base_coin-$market-${kline_list[$kline_index]}-${key_list[$i]}";
        $res = $redis->get($key);
        $rtn["data"][$kline_list[$kline_index]][$key_list[$i]] = $res;
    }
}
echo json_encode($rtn);
?>