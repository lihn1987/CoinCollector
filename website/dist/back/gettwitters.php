<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getTwitterInfo(intval($_GET["size"]));
?>