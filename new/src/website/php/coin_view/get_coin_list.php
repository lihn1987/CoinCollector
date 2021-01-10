<?php
$market = strtoupper($_GET["market"]);
$key_name = "$market-CONFIG";
$rtn = ["result"=>TRUE, "data"=>[]];
$redis = new Redis();
$redis->connect('redis', 6379);
$res = $redis->get($key_name);
if($res != false){
    $json_obj = json_decode($res, true);
    $rtn["data"] = $json_obj;
}
echo json_encode($rtn);
?>