<?php
$market = strtoupper($_GET["market"]);
$coin_list_str = strtoupper($_GET["coin_list"]);
$coin_list = json_decode($coin_list_str, true);

$key_name = "$market-CONFIG";
$rtn = ["result"=>TRUE, "data"=>[]];
$redis = new Redis();
$redis->connect('redis', 6379);

if($coin_list != false){
    $res = $redis->set($key_name, $coin_list_str);
    $redis->publish($key_name, "something");
}
echo json_encode($rtn);
?>