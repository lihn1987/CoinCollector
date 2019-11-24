<?php
function ConnectToServer(){
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "coin";
    $conn = new mysqli($servername, $username, $password, $dbname);
    if($conn->connect_error){
        return null;
    }
    return $conn;
};
class CoinBase{
    var $db_conn;
    function __construct(){
        $this->db_conn = ConnectToServer();
        $this->db_conn->query("SET NAMES utf8");
    }
    function getAllBaseInfo($index_from, $index_to){
        $rtn = array();
        $sql = "SELECT count(*) as `count` FROM coin_base";
        $result = $this->db_conn->query($sql);
        $row = $result->fetch_assoc();
        $rtn['count'] = $row['count'];
        $rtn['list'] = array();
        $sql = "SELECT `id`, `index`, `name`, `name_en`, `name_cn`, `official_website` FROM `coin_base` order by CONVERT(`index`, UNSIGNED INTEGER) limit $index_from, $index_to ";
        $result = $this->db_conn->query($sql);

        if ($result->num_rows > 0) {
            // 输出数据
            while($row = $result->fetch_assoc()) {
                array_push($rtn['list'], $row);
            }
            echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
        } else {
            echo "0 结果";
        }
    }
    function getCoinDescribe($id){
        $sql = "select description from coin_base where `id` = ".$id;
        $result = $this->db_conn->query($sql);
        if ($result->num_rows > 0) {
            // 输出数据
            while($row = $result->fetch_assoc()) {
                echo $row['description'];
                return;
            }
        }
    }
    function getNewsInfo($offset, $size){
        $rtn = array();
        $sql = "SELECT count(*) as `count` FROM article";
        $result = $this->db_conn->query($sql);
        $row = $result->fetch_assoc();
        $rtn['count'] = $row['count'];
        $rtn['list'] = array();
        $sql = "SELECT `time_utc`,`title`,`desc`,`author`,`source_media`,`source_addr` FROM article order by time_utc desc limit $offset, $size ";
        $result = $this->db_conn->query($sql);

        if ($result->num_rows > 0) {
            // 输出数据
            while($row = $result->fetch_assoc()) {
                array_push($rtn['list'], $row);
            }
            echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
        } else {
            echo "0 结果";
        }
    }

    function getNewsInfoByCoinId($offset, $size, $coin_id){
        $rtn = array();
        $sql = "SELECT count(*) as count
        from article, article_2_coinbase
        where article_2_coinbase.article_id = article.id and article_2_coinbase.coin_id = $coin_id";
        $result = $this->db_conn->query($sql);
        $row = $result->fetch_assoc();
        $rtn['count'] = $row['count'];
        $rtn['list'] = array();
        $sql = "select article.`time_utc`, 
        article.`title`,
        article.`desc`,
        article.`author`,
        article.`source_media`,
        article.`source_addr` 
        from article, article_2_coinbase
        where article_2_coinbase.article_id = article.id and article_2_coinbase.coin_id = $coin_id
        order by article.time_utc desc limit $offset, $size";
        $result = $this->db_conn->query($sql);

        if ($result->num_rows > 0) {
            // 输出数据
            while($row = $result->fetch_assoc()) {
                array_push($rtn['list'], $row);
            }
            echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
        } else {
            echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
        }
    }
    
};
?>