<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getTwitterOnCoinInfo(intval($_GET["index"]),intval($_GET["size"]),intval($_GET["coin_id"]));
?>