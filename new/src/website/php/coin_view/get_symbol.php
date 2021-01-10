<?php

$market = strtoupper($_GET["market"]);
$order_coin = strtoupper($_GET["order_coin"]);
$base_coin = strtoupper($_GET["base_coin"]);

$rtn = ["result"=>TRUE, "data"=>[]];
$redis = new Redis();
$redis->connect('redis', 6379);

$key_list = [
    "base-coin",
    "order-coin",
    "price-precision",
    "amount-precision",
    "symbol-partition",
    "symbol",
    "state",
    "value-precision",
    "limit-order-min-order-amt",
    "limit-order-max-order-amt",
    "sell-market-min-order-amt",
    "sell-market-max-order-amt",
    "buy-market-max-order-value",
    "min-order-value"
];
for($i = 0; $i < sizeof($key_list); $i++){
    $key = "${order_coin}_$base_coin-$market-${key_list[$i]}";
    $res = $redis->get($key);
    $rtn["data"][str_replace("-", "_", $key_list[$i])] = $res;
}
echo json_encode($rtn);
?>