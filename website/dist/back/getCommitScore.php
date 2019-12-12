<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getCommit(intval($_GET["id"]));
?>