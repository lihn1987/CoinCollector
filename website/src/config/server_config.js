var server_config = {
    url: '',
    //url: 'http://a.com',
    port: '80'
}
var websocket_url = "ws://www.bixiaozhan";
var websocket_config = {
  depth_url:websocket_url+":8000",
  detail_url:websocket_url+":8001",
  analyse_url:websocket_url+":8002"
}
export {
  server_config,
  websocket_config
}