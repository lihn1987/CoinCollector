<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getNewsInfo($_GET["offset"],$_GET["size"]);
?>