<template>
    <div class="page-container" id="modelView">
      <Navbar class="nav-bar-component"></Navbar>
      <RightMenu class="right-menu-component"></RightMenu>
      <BottomContent class="bottom-component"></BottomContent>
  </div>
</template>

<script setup>
import Navbar from "../components/NavBar.vue"
import RightMenu from "../components/RightMenu.vue"
import BottomContent from "../components/BottomContent.vue"
import {onMounted, watch} from "vue";
import {useStore} from "vuex";
import Base3d from "../threejsUtils/Base3d.js"
import {init3dmLoader, initRhinoModule} from "../threejsUtils/rhinoModule";
// import { getCube, getDefaultSpoiler } from '../api/index.js';}
import {initBaseElement} from '../utils/dataStructure/InitBaseElement'
import {
  addBaseElementToScene, cleanUpScene,
  delBaseElementFromScene,
  getRefCube,
  removeRefCube,
  addMultiGeoBaseToScene
} from "../utils/dataStructure/ElementOpsUtils.js";
import {adjustSpoilerBaseDistance} from "../utils/SpoilerUtils/SpoilerUtils.js"
import { getDefaultSpoiler, getBuilding, saveMyFile } from '../api/index.js';
// import {initSpoilerMaterial} from "../utils/SpoilerUtils/SpoilerMaterial";

let rhino
let modelLoader
let sampleCar
let threeScene
let refCube
let store = useStore()

onMounted(async()=>{
  rhino = initRhinoModule()
  modelLoader = init3dmLoader()
  threeScene = new Base3d('#modelView')
  threeScene.scene.updateWorldMatrix(true)
  // 获得初始化的尾翼
  const allDefaultSpoilers = []
  // const cube = await getCube()
  const spoiler = await getDefaultSpoiler()
  
  // console.log(spoiler);
  for (let ele of spoiler.data){
    allDefaultSpoilers.push(await initBaseElement(ele, modelLoader))
  }
  for (let ele of allDefaultSpoilers){
    // console.log(ele);
    // console.log(ele.geometry)
    await addMultiGeoBaseToScene(ele, threeScene.scene)
  }
  // console.log(allDefaultSpoilers)
  // await initSpoilerMaterial(allDefaultSpoilers[0])
  store.commit('commitDefaultSpoiler', allDefaultSpoilers)
  
})

watch(()=>store.state.modelingParams.buildingHight, (newVal, oldVal)=>{
  if (refCube===undefined) removeRefCube(refCube, store, threeScene.scene)
  const deltaZ = (newVal-oldVal)
  // const extendLength = store.state.modelingParams.sideExtendDistance
  const defaultLength = store.state.defaultModelingParams.buildingHight
  const curLength = newVal+defaultLength
  adjustSpoilerBaseDistance(store.state.defaultSpoiler, 0, 0, deltaZ, curLength, defaultLength)
})

async function generateSpoiler () {
  if (refCube===undefined) removeRefCube(refCube, store, threeScene.scene)
  // 将已有的物件都先删除
  cleanUpScene(threeScene.scene)
  const allSpoilers = []
  const resultData = await getBuilding(store.state.modelingParams)
  for (let ele of resultData.data){
    allSpoilers.push(await initBaseElement(ele, modelLoader))
  }
  // 添加新的
  for (let ele of allSpoilers){
    // print(ele)
    // console.log(ele);
    await addMultiGeoBaseToScene(ele, threeScene.scene)
  }
  //store the default spoiler
  store.commit('commitDefaultSpoiler', allSpoilers)
}

async function generateRhinoFile () {
  saveMyFile(store.state.modelingParams)
  store.commit('commitFileDownload', false)
  console.log('success!');
  console.log(store.state.fileDownload)
}


watch([
  // ()=>store.state.modelingParams.buildingHight,
  ()=>store.state.modelingParams.l1RoadWidth,
  ()=>store.state.modelingParams.l2RoadWidth,
  ()=>store.state.modelingParams.l4RoadWidth,
  ()=>store.state.modelingParams.treeDensity], ()=>{
  console.log(store.state.modelingParams)
  cleanUpScene(threeScene.scene)
  generateSpoiler()
  // console.log(store.state.defaultSpoiler);
})

watch([
  ()=>store.state.fileDownload], ()=>{
  generateRhinoFile()
  // console.log(store.state.defaultSpoiler);
})

// console.log(store.state.modelingParams)

</script>

<style scoped lang="less">
  .page-container{
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .nav-bar-component{
    position: absolute;
    z-index: 100;
    top: 0;
  }
  .bottom-component{
    position: absolute;
    z-index: 100;
    bottom: 1vh;
  }
  .right-menu-component{
    position: absolute;
    right: 0;
  }
  </style>