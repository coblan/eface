<template>
    <div class="coordinateMap">
        <div class="coordinateMap_input">
            <el-input
                    v-model="lng"
                    placeholder="点击地图或输入经度"
                    @change="lnglatChange"
            ></el-input>
            <div style="width:50px"></div>
            <el-input
                    v-model="lat"
                    placeholder="点击地图或输入纬度"
                    @change="lnglatChange"
            ></el-input>
        </div>
        <div
                id="map"
                class="map"
        >
        </div>
    </div>
</template>

<script>
    /*
    * 调用高德选择经纬度。
    * 现在暂时未使用，如果后期有精细的选择需求，可以扩展该组件
    * */
    var map
    var mouseTool
    export default {
        data() {
            return {
                lastDot: '',
                marker: null,
                lng: '',
                lat: '',
            }
        },
        mounted() {
            this.initMap()
            //监听用户的点击事件
            map.on('click', (e) => {
                this.lng = e.lnglat.getLng()
            this.lat = e.lnglat.getLat()
            this.addDot()
        })
        },
        methods: {
            initMap() {
                map = new AMap.Map('map', {
                    resizeEnable: true, //是否监控地图容器尺寸变化
                    zoom: 11, //初始化地图层级
//                    center: [116.46,39.92] //初始化地图中心点
                });
                //获取用户所在城市信息
//                function showCityInfo() {
//                    //实例化城市查询类
//                    var citysearch = new AMap.CitySearch();
//                    //自动获取用户IP，返回当前城市
//                    citysearch.getLocalCity(function(status, result) {
//                        if (status === 'complete' && result.info === 'OK') {
//                            if (result && result.city && result.bounds) {
//                                var cityinfo = result.city;
//                                var citybounds = result.bounds;
//                                document.getElementById('info').innerHTML = '您当前所在城市：'+cityinfo;
//                                //地图显示当前城市
//                                map.setBounds(citybounds);
//                            }
//                        } else {
//                            document.getElementById('info').innerHTML = result.info;
//                        }
//                    });
//                }
//                showCityInfo();
            },
            lnglatChange() {
                this.addDot()
                //自适应中心点
                map.setFitView();
            },
            //增加点标记
            addDot(){
                if (this.marker) {
                    this.marker.setMap(null);
                    this.marker = null;
                }
                this.marker = new AMap.Marker({
                    position: new AMap.LngLat(this.lng, this.lat)
                });
                let lnglat = {}
                lnglat.lng = Number(this.lng)
                lnglat.lat = Number(this.lat)
                this.$emit("giveLnglat", lnglat);
                map.add(this.marker);
            },
        }
    }
</script>

<style lang="scss" scoped>
    .coordinateMap {
        width: 500px;
        .coordinateMap_input {
            display: flex;
            margin-bottom: 15px;
        }
        .map {
            width: 500px;
            height: 300px;
            border-radius:6px;
        }
    }
</style>
