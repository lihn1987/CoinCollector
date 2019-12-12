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
        $sql = "select * from (
            select coin_base.*, score.score_all from coin_base,(select * from score as a where `time` = 
            (select max(time) from score as b where b.coin_name=a.coin_name )) as score where coin_base.name_en = score.coin_name 
            UNION
            select *,'no' as score_all from coin_base where coin_base.name_en not in (select score.coin_name from score)
            )as base order by  CONVERT(`score_all`,  DECIMAL)  desc limit $index_from, $index_to ";
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
    function getCoinNameEnByID($id){
        $sql = "select name_en from coin_base where `id` = ".$id;
        $result = $this->db_conn->query($sql);
        if ($result->num_rows > 0) {
            // 输出数据
            while($row = $result->fetch_assoc()) {
                echo $row['name_en'];
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
    function getScaleTradeDetail($market, $order_coin, $base_coin, $second){
        $rtn=[];
        $time = time()*1000-$second*1000;
        $sql = "select sum(amount) as amount from trade_detail
        where `trade_time` > $time and
        market=$market and
        order_coin = '$order_coin' and
        base_coin = '$base_coin' and 
        dir = 0;";
        $result = $this->db_conn->query($sql);
        $row = $result->fetch_assoc();
        $rtn['buy_count'] = $row["amount"];
        $sql = "select sum(amount) as amount from trade_detail
        where `trade_time` > $time and
        market=$market and
        order_coin = '$order_coin' and
        base_coin = '$base_coin' and 
        dir = 1;";
        $result = $this->db_conn->query($sql);
        $row = $result->fetch_assoc();
        $rtn['sell_count'] = $row["amount"];
        echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
    }
    function getTwitterInfo($size){
        $rtn=array();
        $sql = "select * from twitter order by `time` desc limit 0, $size";
        $result = $this->db_conn->query($sql);
        /*$row = $result->fetch_assoc();
        $rtn['sell_count'] = $row["amount"];*/
        if ($result->num_rows > 0) {
            // 输出数据
            $rtn['data']=array();
            while($row = $result->fetch_assoc()) {
                array_push($rtn['data'], $row);
            }
            echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
        }
        //echo json_encode($result,JSON_UNESCAPED_UNICODE);
    }
    function getTwitterOnCoinInfo ($index, $size, $coin_id){
        $rtn=array();
        $sql = "select twitter.* from coin_base,twitter where coin_base.`id`=$coin_id and twitter.coin_name = coin_base.name_en order by `time` desc limit $index, $size";
        $result = $this->db_conn->query($sql);
        /*$row = $result->fetch_assoc();
        $rtn['sell_count'] = $row["amount"];*/
        if ($result->num_rows > 0) {
            // 输出数据
            $rtn['data']=array();
            while($row = $result->fetch_assoc()) {
                array_push($rtn['data'], $row);
            }
            echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
        }
        //echo json_encode($result,JSON_UNESCAPED_UNICODE);
    }

    function getCommit ($id){
        $rtn=array();
        $sql = "select max(commit_count) as max,min(commit_count) as min from github,coin_base  where `time`>".(time()-60*60*24*7)." and coin_base.name_en=github.coin_name and coin_base.id=$id group by coin_name";
        $result = $this->db_conn->query($sql);
        $rtn['data'] = array();
        /*$row = $result->fetch_assoc();
        $rtn['sell_count'] = $row["amount"];*/
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                $rtn['data']["max"]=$row["max"];
                $rtn['data']["count"]=$row["max"]-$row["min"];
                break;
            }
            
        }else{
            $rtn['data']["max"]="未开源或未抓取";
            $rtn['data']["count"]="未开源或未抓取";
        }
        echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
    }

    function getNewsCount($id){
        $rtn=array();
        $rtn['data'] = array();
        $sql = "select count(*) as count from coin_base, article_2_coinbase ,article
            where 
            coin_base.id = $id and 
            coin_base.id = article_2_coinbase.coin_id and 
            article_2_coinbase.article_id = article.id and 
            time_utc > ".(time()-60*60*24*7);
        $result = $this->db_conn->query($sql);
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                $rtn['data']['media_news_count'] = $row["count"];
                break;
            }
        }else{
            $rtn['data']['media_news_count'] = 0;
        }
        $sql = "select count(*) as count from twitter,coin_base
        where 
        coin_base.id = $id and
        coin_base.name_en = twitter.coin_name and          
        time > ".(time()*1000-1000*60*60*24*7);
        $result = $this->db_conn->query($sql);
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                $rtn['data']['offical_news_count'] = $row["count"];
                break;
            }
        }else{
            $rtn['data']['offical_news_count'] = "无官网新闻或未抓取";
        }
        echo json_encode($rtn,JSON_UNESCAPED_UNICODE);
    }
};
?>