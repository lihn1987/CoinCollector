<?php
$coin_list = array(
    array("1INCH", "USDT"),
    array("SWRV", "USDT"),
    array("EOS", "USDT"),
    array("ACT", "USDT"),
    array("YFI", "USDT"),
    array("UTK", "USDT"),
    array("ANT", "USDT"),
    array("SUN", "USDT"),
    array("BAND", "USDT"),
    array("SWFTC", "USDT"),
    array("SNT", "USDT"),
    array("LRC", "USDT"),
    array("ELF", "USDT"),
    array("BCHA", "USDT"),
    array("NEAR", "USDT"),
    array("BSV", "USDT"),
    array("VSYS", "USDT"),
    array("UMA", "USDT"),
    array("BAL", "USDT"),
    array("EM", "USDT"),
    array("KAN", "USDT"),
    array("TRX", "USDT"),
    array("VALUE", "USDT"),
    array("WTC", "USDT"),
    array("IOTA", "USDT"),
    array("ATOM", "USDT"),
    array("KNC", "USDT"),
    array("EGT", "USDT"),
    array("KCASH", "USDT"),
    array("DOT", "USDT"),
    array("CRV", "USDT"),
    array("XTZ", "USDT"),
    array("DCR", "USDT"),
    array("NULS", "USDT"),
    array("LTC", "USDT"),
    array("REN", "USDT"),
    array("DAI", "USDT"),
    array("CRO", "USDT"),
    array("ABT", "USDT"),
    array("ZIL", "USDT"),
    array("RVN", "USDT"),
    array("OMG", "USDT"),
    array("BTM", "USDT"),
    array("AAVE", "USDT"),
    array("JST", "USDT"),
    array("CMT", "USDT"),
    array("GRT", "USDT"),
    array("BETH", "USDT"),
    array("UNI", "USDT"),
    array("BAT", "USDT"),
    array("HBAR", "USDT"),
    array("FIL", "USDT"),
    array("ITC", "USDT"),
    array("ALGO", "USDT"),
    array("IOST", "USDT"),
    array("ZRX", "USDT"),
    array("LAMB", "USDT"),
    array("STORJ", "USDT"),
    array("NEO", "USDT"),
    array("NAS", "USDT"),
    array("WXT", "USDT"),
    array("AVAX", "USDT"),
    array("YFII", "USDT"),
    array("LBA", "USDT"),
    array("CVC", "USDT"),
    array("RSR", "USDT"),
    array("WAVES", "USDT"),
    array("DHT", "USDT"),
    array("BOT", "USDT"),
    array("ONT", "USDT"),
    array("XEM", "USDT"),
    array("YEE", "USDT"),
    array("ADA", "USDT"),
    array("API3", "USDT"),
    array("DOGE", "USDT"),
    array("NANO", "USDT"),
    array("SUSHI", "USDT"),
    array("MLN", "USDT"),
    array("ETH", "USDT"),
    array("XLM", "USDT"),
    array("WNXM", "USDT"),
    array("BTT", "USDT"),
    array("TRB", "USDT"),
    array("DASH", "USDT"),
    array("XMR", "USDT"),
    array("BTC", "USDT"),
    array("MANA", "USDT"),
    array("COMP", "USDT"),
    array("AE", "USDT"),
    array("CTXC", "USDT"),
    array("THETA", "USDT"),
    array("AAC", "USDT"),
    array("BNT", "USDT"),
    array("AST", "USDT"),
    array("ZEC", "USDT"),
    array("OXT", "USDT"),
    array("XRP", "USDT"),
    array("LINK", "USDT"),
    array("KSM", "USDT"),
    array("FSN", "USDT"),
    array("HC", "USDT"),
    array("QTUM", "USDT"),
    array("SNX", "USDT"),
    array("ICX", "USDT"),
    array("MKR", "USDT"),
    array("BCH", "USDT"),
    array("ETC", "USDT")
);
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
            
            $key_name = $coin_list[$i][0]."-".$coin_list[$i][1]."-".$market_list[$market_index];
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
?>