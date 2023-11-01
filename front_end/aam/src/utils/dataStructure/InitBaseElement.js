import {file3dmLoader} from "../../threejsUtils/rhinoModelLoader.js"
import BaseElement from "./BaseElement.js";
import PointElement from "./PointElement.js"
import {toRaw} from "vue";


// 将带有file3dm byte的数据转换成真实数据
export const initBaseElement = async function (rowElement, loader){
    // init element
    let file3dmData
    const curElement = new BaseElement(rowElement)
    // 自身的file3dm文件
    // console.log(loader)
    // console.log(rowElement)
    await file3dmLoader(rowElement.file3dm, loader).then((res)=>file3dmData=res)
    // handle layer
    const layers = []
    file3dmData.userData.layers.forEach((layer)=>{layers.push(layer.name)})
    // handle geometry
    file3dmData.children.forEach((geo)=>{
        const curLayer = layers[geo.userData.attributes.layerIndex]
        if (curLayer === 'geometry'){
            curElement.geometry.push(geo)
        }else if (curLayer === 'anchor_pt'){
            curElement.anchorPt = geo
        }else if (curLayer.indexOf('install')===0){
            const curInstallPt = new PointElement(geo, curLayer)
            curElement.installPts.push(curInstallPt)
        }else if (curLayer.indexOf('rotate')===0){
            const curRotatePt = new PointElement(geo, curLayer)
            curElement.rotatePts.push(curRotatePt)
        }
    })
    // handle link element
    if (rowElement.link_element.length>0){
        for (const ele of rowElement.link_element) {
            curElement.linkElement.push(await initBaseElement(ele, loader))
        }
    }
    return toRaw(curElement)
}