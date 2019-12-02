<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    if(
        array_key_exists("method", $_GET) && 
        array_key_exists("page_idx", $_GET) && 
        array_key_exists("page_size", $_GET) && 
        $_GET['method']=="get_all")
    {
        $coin_base->getAllBaseInfo(intval($_GET["page_idx"]), intval($_GET['page_size']));
    }else if(
        array_key_exists('method',$_GET) &&
        array_key_exists('id',$_GET) &&
        $_GET['method'] == 'get_description')
    {
        $coin_base->getCoinDescribe(intval($_GET["id"]));
    }else if(
        array_key_exists('method',$_GET) &&
        array_key_exists('id',$_GET) &&
        $_GET['method'] == 'get_coin_name_en')
    {
        $coin_base->getCoinNameEnByID(intval($_GET["id"]));
    }

?>