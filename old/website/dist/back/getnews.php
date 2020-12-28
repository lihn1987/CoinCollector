<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getNewsInfo(intval($_GET["offset"]),intval($_GET["size"]));
?>