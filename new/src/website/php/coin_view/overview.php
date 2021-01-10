<?php

$content = file_get_contents('php://input');
$post    = json_decode($content, true);

switch($post["method"]){
    case "get_overview":
        get_overview();
        break;
    default:
        echo "error method";
}


function get_overview(){
    $rtn = [];
    $redis = new Redis();
    $redis->connect('redis', 6379);
    global $coin_list;
    
    for($i = 0; $i < sizeof($coin_list); $i++){
        
        $market_list = ["OK", "HUOBI"];
        
        $item = [
            "order_coin" => $coin_list[$i][0],
            "base_coin" => $coin_list[$i][1]
        ];
        for($market_index = 0; $market_index < sizeof($market_list); $market_index++){
            
            $key_name = $coin_list[$i][0]."-".$coin_list[$i][1]."-".$market_list[$market_index]."-DEPTH";
            //echo $key_name;
            $res = $redis->get($key_name);
            if($res != false){
                $json_obj = json_decode($res, true);
                $item["up_time_".$market_list[$market_index]] = $json_obj["up_time"];
                $item["forbuy_".$market_list[$market_index]] = $json_obj["forbuy"][0][0];
                $item["forsell_".$market_list[$market_index]] = $json_obj["forsell"][0][0];
                $item["delay_".$market_list[$market_index]] = $json_obj["delay"];
            }
        }
        array_push($rtn, $item);
    }
    echo json_encode($rtn);
}

function get_huobi_sample_info(){
    $rtn = [];
    $redis = new Redis();
    $redis->connect('redis', 6379);
    global $coin_list;
    $coin_market = "HUOBI";
    for($i = 0; $i < sizeof($coin_list); $i++){ 
        $item = [
            "order_coin" => $coin_list[$i][0],
            "base_coin" => $coin_list[$i][1]
        ];
        for($market_index = 0; $market_index < sizeof($market_list); $market_index++){
            //echo $key_name;
            $key_name = $coin_list[$i][0]."-".$coin_list[$i][1]."-".$market_list[$market_index];
            $res = $redis->get($key_name);
            if($res != false){
                $json_obj = json_decode($res, true);
                $item["up_time_".$coin_market] = $json_obj["up_time"];
                $item["forbuy_".$coin_market] = $json_obj["forbuy"][0][0];
                $item["forsell_".$coin_market] = $json_obj["forsell"][0][0];
                $item["delay_".$coin_market] = $json_obj["delay"];
            }
        }
        array_push($rtn, $item);
    }
    echo json_encode($rtn);
}
?>