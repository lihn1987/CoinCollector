<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getNewsInfoByCoinId(intval($_GET["offset"]),intval($_GET["size"]), intval($_GET['coin_id']));
?>