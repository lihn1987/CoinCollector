<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getNewsInfoByCoinId($_GET["offset"],$_GET["size"], $_GET['coin_id']);
?>