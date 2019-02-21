require('./confirm_win.scss')

Vue.component('com-wechat-confirm-win',{
    props:['ctx'],
    template:`<div class="com-wechat-confirm-win">
    <div class="row">请确认微信支付是否已经完成</div>
    <hr>
    <div class="has-finish row" @click="finish('pay:ok')">已完成支付</div>
    <hr>
    <div class="has-problem row" @click="finish('pay:error')">支付遇到问题，重新支付</div>
    </div>`,
    methods:{
        finish:function(str){
            this.$emit('finish',str)
        }
    }
})