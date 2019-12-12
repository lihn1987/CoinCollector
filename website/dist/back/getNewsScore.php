<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getNewsCount(intval($_GET["id"]));
?>