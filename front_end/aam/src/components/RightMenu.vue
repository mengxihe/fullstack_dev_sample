<template>
  <a-drawer
      :width="drawerStatus.drawerWidth"
      placement="right"
      :visible="drawerStatus.drawerVisible"
      :mask="false"
      @close="drawerOnClose"
      :zIndex="9"
  >
  </a-drawer>
  <div class="drawer-content">
    <a-drawer
        class="drawer-main"
        :width="drawerStatus.drawerWidth"
        placement="right"
        :visible="drawerStatus.drawerVisible"
        :mask="false"
        @close="drawerOnClose"
        :zIndex="99"
        :closable="false"
    >
      <div class="drawer-content-container">
        <div class="title-text">Master Plan Generator</div>
        <div class="tab-container">
          <a-tabs v-model:activeKey="activeKey">
            <a-tab-pane key="1">
              <template #tab><span><tool-outlined/>Parameter</span></template>
              <div class="tab-title-text">Modeling Parameter</div>

              <div class="param-content">
                <div class='params-item-name'> Building Height</div>
                <div class="params-item"> 
                  <a-slider v-model:value="generateParams.buildingHight" :min="10" :max="30" :step="1"/>
              </div>

                <div class="params-range">
                  <div class="params-range-text">10 m</div>
                  <div class="params-range-text">30 m</div>
                </div>
              </div>

              <div class="params-content">
                <div class="params-item-name">L1_Road Width</div>
                <div class="params-item"> 
                  <a-slider v-model:value="generateParams.l1RoadWidth" :min="5" :max="10" :step="1"/>
                </div>
                <div class="params-range">
                  <div class="params-range-text">5 m</div>
                  <div class="params-range-text">10 m</div>
                </div>
              </div>

              <div class="params-content">
                <div class="params-item-name">L2_Road Width</div>
                <div class="params-item"> 
                  <a-slider v-model:value="generateParams.l2RoadWidth" :min="2" :max="5" :step="1"/>
                </div>
                <div class="params-range">
                  <div class="params-range-text">2 m</div>
                  <div class="params-range-text">5 m</div>
                </div>
              </div>

              <div class="params-content">
                <div class="params-item-name">L4_Road Width</div>
                <div class="params-item"> 
                  <a-slider v-model:value="generateParams.l4RoadWidth" :min="2" :max="5" :step="1"/>
                </div>
                <div class="params-range">
                  <div class="params-range-text">2 m</div>
                  <div class="params-range-text">5 m</div>
                </div>
              </div>

              <div class="params-content">
                <div class="params-item-name">Trees Density</div>
                <div class="params-item"> 
                  <a-slider v-model:value="generateParams.treeDensity" :min="4" :max="10" :step="1 "/>
                </div>
                <div class="params-range">
                  <div class="params-range-text">4</div>
                  <div class="params-range-text">10</div>
                </div>
              </div>

              <div class="params-content">
                <div class="params-item-name">Visibility</div>
                <div class="params-item"> 
                  <a-select
                      ref="select"
                      v-model:value="generateParams.layerName"
                      style="width: 240px"
                      size="small"
                      @focus="focus"
                      @change="changeLayerName"
                      class="side-board-selector"
                  >
                    <a-select-option value="All">All</a-select-option>
                  </a-select>
                </div>
              </div>
              <a-button type="primary" name="save" v-model:value="generateParams.saveFile" @click="saveRhinoFile">Save File!</a-button>
            </a-tab-pane>
<!--            material panel-->
            <a-tab-pane key="2">
              <template #tab><span><format-painter-outlined />Material</span></template>
              nothing here yet!
            </a-tab-pane>
          </a-tabs>
        </div>
      </div>
    </a-drawer>
  </div>
</template>

<script setup>
  import { ToolOutlined, FormatPainterOutlined } from '@ant-design/icons-vue';
  import {reactive, ref, watch} from "vue";
  import {useStore} from "vuex"
  
  let store = useStore()
  
  const activeKey = ref('1')
  const sideScaleDisable = ref(true)
  const drawerStatus = reactive({
    drawerWidth:350,
    drawerVisible:true,
  })
  // const save = await saveFile()
  const generateParams = reactive({
    buildingHight:14,
    l1RoadWidth:7,
    l2RoadWidth:3,
    l4RoadWidth:3,
    treeDensity:5,
    layerName:'All',
    saveFile: false
  })
  
  function drawerOnClose(){
    drawerStatus.drawerVisible = false
  }
  
  function changeLayerName(value){
    generateParams.layerName = value
  }
  
  function saveRhinoFile(){
    generateParams.saveFile = true
  }
  
  watch([()=>generateParams.buildingHight,
    ()=>generateParams.l1RoadWidth,
    ()=>generateParams.l2RoadWidth,
    ()=>generateParams.l4RoadWidth,
    ()=>generateParams.treeDensity,
    ()=>generateParams.layerName,
  ], (newVal, oldVal)=>{
    store.commit('commitModelingParams', generateParams)
    // console.log(store.state.modelingParams)
  })

  watch([()=>generateParams.saveFile,
  ], (newVal, oldVal)=>{
    store.commit('commitFileDownload', generateParams.saveFile)
    console.log(store.state.fileDownload)
  })
  
  </script>

<style scoped lang="less">
.drawer-content-container{
  padding-top: 40px;
}
.title-text{
  color: #333333;
  font-size: 120%;
  font-weight: bold;
}
.tab-container{
  margin-top: 20px;
}
.tab-title-text{
  color: #969696;
  margin-top: 8px;
  margin-bottom: 8px;
  font-size: 110%;
}
.params-content{
  margin-top: 10px;
  margin-bottom: 20px;
}
.params-item-name{
  color: #333333;
  font-size: 90%;
}
.params-range{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  .params-range-text{
    color: #333333;
    font-size: 90%;
  }
}
.radio-group{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-top: 10px;
}
.side-board-selector{
  margin-top: 10px;
}
</style>