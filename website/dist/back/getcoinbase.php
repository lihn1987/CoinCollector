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
        $coin_base->getAllBaseInfo($_GET["page_idx"], $_GET['page_size']);
    }else if(
        array_key_exists('method',$_GET) &&
        array_key_exists('id',$_GET) &&
        $_GET['method'] == 'get_description')
    {
        $coin_base->getCoinDescribe($_GET["id"]);
    }

?>