<?php
$market = strtoupper($_GET["market"]);
$coin = strtoupper($_GET["coin"]);

$key_name = "$coin-$market-BALANCE";
$rtn = ["result"=>TRUE, "data"=>0];
$redis = new Redis();
$redis->connect('redis', 6379);
$rtn["data"] = $redis->get($key_name);
echo json_encode($rtn);
?>