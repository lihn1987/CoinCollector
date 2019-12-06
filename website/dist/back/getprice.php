<?php
require("db.php")
?>
<?php
    $redis = new Redis();  
    $redis->connect('localhost', 6379);//serverip port
    $arr = explode("|", $_GET["symbel"]);
    $data = [];
    for($i = 0; $i < sizeof($arr); $i++){
        $json_obj = json_decode($redis->get(strtoupper($arr[$i])."_PRICE24"),true);
        //var_dump($json_obj);
        $json_obj["coin"]=strtoupper($arr[$i]);
        array_push($data,$json_obj);
    }
    $rtn = array("data"=>$data);
    echo json_encode($rtn);
    
?>