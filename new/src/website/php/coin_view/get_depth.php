<?php

$market = strtoupper($_GET["market"]);
$order_coin = strtoupper($_GET["order_coin"]);
$base_coin = strtoupper($_GET["base_coin"]);

$rtn = ["result"=>TRUE, "data"=>[]];
$redis = new Redis();
$redis->connect('redis', 6379);

$key = "$order_coin-$base_coin-$market-DEPTH";

$res = $redis->get($key);
$rtn["data"] = json_decode($res);

echo json_encode($rtn);
?>