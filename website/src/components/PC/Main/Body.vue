<template>
  <div class="Body">
    <div class="body_content">
      <div class="line_item1">111001101010</div>
      <div class="line_item1">001010100110</div>
      <div class="line_item1">111001101000</div>
      <div class="line_item1">001110110011</div>
      <div class="line_item2">一切为了看清</div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'HeaBodyder',
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "../../../style/index.scss";
.Body{
  background-color:rgb(216,216,216);
  height:800px;
}
.body_content {
  padding-top:180px;
}
.line_item1{
  font-size:52px;
  color:rgb(95,188,118);
}
.line_item2{
  font-size:52px;
  color:rgb(95,188,118);
}

</style>
