import * as THREE from "three"
import {extractAllBaseElement} from "../dataStructure/ElementOpsUtils";
import {toRaw} from "vue";

export const defaultMaterial = new THREE.MeshPhongMaterial({
    color:0xffffff,
    sheenRoughness:0.336,
    metalness: 0.73,
    reflectivity:1.0,
    clearcoat:0.36,
    clearcoatRoughness:0.1,
    flatShading:true,
    side:THREE.DoubleSide,
    shadowSide:THREE.BackSide
})

export const blackSteel = new THREE.MeshPhongMaterial({
    color:0x6200ea,
    sheenRoughness:0.336,
    metalness: 0.73,
    reflectivity:1.0,
    clearcoat:0.36,
    clearcoatRoughness:0.1,
    flatShading:true,
    side:THREE.DoubleSide,
    shadowSide:THREE.BackSide
})

export const graySteel = new THREE.MeshPhongMaterial({
    color:0xf50057,
    sheenRoughness:0.336,
    metalness: 0.73,
    reflectivity:1.0,
    clearcoat:0.36,
    clearcoatRoughness:0.1,
    flatShading:true,
    side:THREE.DoubleSide,
    shadowSide:THREE.BackSide
})

const initMaterialByName = function (ele){
    let curMaterial
    if (ele.objectName==='left_base_model') curMaterial = blackSteel
    if (ele.objectName==='right_base_model') curMaterial = blackSteel
    if (ele.objectName==='left_connector_model') curMaterial = blackSteel
    if (ele.objectName==='right_connector_model') curMaterial = blackSteel

    if (ele.objectName==='left_side_board_model') curMaterial = graySteel
    if (ele.objectName==='right_side_board_model') curMaterial = graySteel
    if (ele.objectName==='spoiler_body_model') curMaterial = graySteel

    if (ele.objectType==='SectionElement') ele.geometry.visible = false
    if (ele.geometry!==null){
        ele.geometry.material = curMaterial
        ele.geometry.castShadow = true
        ele.geometry.receiveShadow = true
    }
}

export const initSpoilerMaterial = function (spoiler){
    const allBaseElements = extractAllBaseElement(toRaw(spoiler))
    allBaseElements.map(ele=>initMaterialByName(ele))
}