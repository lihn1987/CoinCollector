<?php
require("db.php")
?>
<?php
    $coin_base = new CoinBase();
    $coin_base->getScaleTradeDetail($_GET["market"], $_GET["order_coin"], $_GET["base_coin"], $_GET["second"]);

?>