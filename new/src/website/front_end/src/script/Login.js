import axios from 'axios'
import md5 from 'js-md5'
var echarts = require('echarts');
var _this = null;
export default {
  name: 'HelloWorld',
  data () {
    return {
      username:'',
      password:''
    }
  },
  mounted: function () {
    this.get_login_status();
  },
  destroyed: function () {

  },
  methods: {
    login(){
      //alert(this.username + this.password)
      let that = this;
      axios.post("/coin_view/login.php",{username:this.username, password:md5(this.password)}).then(function(result){
        console.log(result.data)
        if(result.data.result == 0){
          that.$router.push({path:'/'});
        }
      })
    },
    get_login_status(){
      let that = this;
      axios.post("/coin_view/get_login_status.php").then(function(result){
        console.log(result.data)
        if(result.data.result == 0){
          that.$router.push({path:'/'});
        }
      })
    }
  }
}