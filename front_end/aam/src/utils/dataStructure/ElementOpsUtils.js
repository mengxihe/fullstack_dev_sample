import * as THREE from "three";
import {getXRotateMatrix, getYRotateMatrix, getZRotateMatrix, getTranslateMatrix, getScaleMatrix} from "../dataStructure/MatrixUtils.js"
import {toRaw} from "vue";

// del three obj form scene
export const removeThreeObjFromScene = function(obj, scene){
    if(scene.children.indexOf(obj)!==-1){
        scene.remove(obj)
        obj.geometry.dispose()
        obj.material.dispose()
    }
}

// total clean up the scene
export const cleanUpScene = function (scene){
    scene.children.forEach((item)=>{
        if(item.type==='Mesh'){
            scene.remove(item)
            // item.geometry.dispose()
            // item.material.dispose()
        }else if(item.type==='Line'){
            scene.remove(item)
            // item.geometry.dispose()
            // item.material.dispose()
        }else if(item.type === 'Points'){
            scene.remove(item)
            // item.geometry.dispose()
            // item.material.dispose()
        }
    })
}

// refCube
export const getRefCube = function (){
    const cubeGeometry = new THREE.BoxGeometry( 10, 10, 10 );
    const cubeMaterial = new THREE.MeshBasicMaterial( {color: 0x00ff00} );
    return  new THREE.Mesh( cubeGeometry, cubeMaterial );
}

// 删掉refCube
export const removeRefCube = function (refCube, store, scene){
    if(refCube!==undefined){
        const offsetRecord = store.state.offsetRecord
        const curChildren = refCube.children
        curChildren.map(item=>item.parent=scene)
        curChildren.map(item=>translateThreeObj(item, offsetRecord[0], offsetRecord[2], -offsetRecord[1]))
        scene.remove(refCube)
        refCube.geometry.dispose()
        refCube.Material.dispose()
    }
}

// 将某个baseElement加入到某个Three object3d中
export const addBaseElementIntoObject3d = function (object3d, element) {
    // as a group and add
    const curGroup = new THREE.Group()
    if (element.geometry !==null) curGroup.add(element.geometry)
    if (element.anchorPt !==null) curGroup.add(element.anchorPt)
    if (element.installPts.length>0) element.installPts.map(item=>curGroup.add(item.pt))
    if (element.rotatePts.length>0) element.rotatePts.map(item=>curGroup.add(item.pt))
    object3d.add(curGroup)
    return curGroup
}

// 将PointElement加入到scene
export const addPointElementToScene = function (pt, scene) {
    scene.add(pt.pt)
}

// 将BaseElement加入到scene
export const addBaseElementToScene = async function (element, scene) {
    // handle cur geometry
    if (element.geometry!==null){
        element.geometry.rotateX(-90*(Math.PI/180))
        scene.add(element.geometry)
    }
    // handle link geometry
    for(let ele of element.linkElement){
        await addBaseElementToScene(ele, scene)
    }
    // handle anchor pt
    if (element.anchorPt!==null){
        element.anchorPt.rotateX(-90*(Math.PI/180))
    }
    // handle install pt
    element.installPts.forEach((pt)=>{
        pt.pt.rotateX(-90*(Math.PI/180))
    })
    // handle rotate pt
    element.rotatePts.forEach((pt)=>{
        pt.pt.rotateX(-90*(Math.PI/180))
    })
}

export const addMultiGeoBaseToScene = function(element, scene) {
    // handle cur geometry
    if (element.geometry!==null){
        for (let mememe of element.geometry){
            mememe.rotateX(-90*(Math.PI/180))
            scene.add(mememe)
        }
    }

}
// 将BaseElement从scene中删除
export const delBaseElementFromScene = function (element, scene){
    // handle cur geometry
    if (element.geometry!==null){
        removeThreeObjFromScene(toRaw(element.geometry), scene)
    }
    // handle link geometry
    for(let ele of element.linkElement){
        delBaseElementFromScene(ele, scene)
    }
    // handle anchor pt
    if (element.anchorPt!==null){
        removeThreeObjFromScene(toRaw(element.anchorPt), scene)
    }
    // handle install pt
    element.installPts.forEach((pt)=>{
        removeThreeObjFromScene(toRaw(pt), scene)
    })
    // handle rotate pt
    element.rotatePts.forEach((pt)=>{
        removeThreeObjFromScene(toRaw(pt), scene)
    })
}

// 将当前BaseElement的所有对象解压出来到一个列表中
export const extractAllBaseElement = function (baseElement){
    const res = []
    if (baseElement.linkElement.length===0){
        res.push(baseElement)
    }else{
        res.push(baseElement)
        baseElement.linkElement.forEach((each)=>{
            res.push(...extractAllBaseElement(each))
        })
    }
    return res
}

// 属于一个array的baseElement，根据其objectName来选择
export const filterBaseElementArrayByObjectName = function (baseElementList, objectNameList, op){
    //op===0时，objectNameList中的那些ele会被过滤，op===1时objectNameList中的那些ele会被保留
    if (op===0){
        return baseElementList.filter(ele=>objectNameList.indexOf(ele.objectName)===-1)
    }else{
        return baseElementList.filter(ele=>objectNameList.indexOf(ele.objectName)!==-1)
    }
}

// recompute center
export const recomputeBaseElementCenter = function (baseElement){
    if (baseElement.geometry!==null) {
        const deltaX = baseElement.geometry.geometry.boundingSphere.center.x
        const deltaY = baseElement.geometry.geometry.boundingSphere.center.y
        const deltaZ = baseElement.geometry.geometry.boundingSphere.center.z
        baseElement.geometry.geometry.center()
        translateThreeObj(baseElement.geometry, deltaX, deltaZ, -deltaY)
    }
    if (baseElement.linkElement.length!==0) baseElement.linkElement.map(ele=>recomputeBaseElementCenter(ele))
}

// compute cur obj center
export const computeBaseElementWorldPosition = function (baseElement){
    if (baseElement.geometry!==null) {
        var worldPosition = new THREE.Vector3()
        baseElement.geometry.getWorldPosition(worldPosition)
        return worldPosition
    }
}

// translate scale three obj
export const translateThreeObj = function (obj, tx, ty, tz){
    obj.applyMatrix4(getTranslateMatrix(tx, ty, tz))
    return obj
}

// scale three obj
export const scaleThreeObj = function (obj, sx, sy, sz){
    obj.scale.set(sx, sy, sz)
    return obj
}


// 移动某个baseElement, 其包含的所有物件都会移动，包括link element
export const translateBaseElement = function ( baseElement, deltaX, deltaY, deltaZ){
    if (baseElement.geometry!==null) translateThreeObj(toRaw(baseElement.geometry), deltaX, deltaY, deltaZ)
    if (baseElement.anchorPt!==null) translateThreeObj(toRaw(baseElement.anchorPt), deltaX, deltaY, deltaZ)
    if (baseElement.installPts.length!==0){} baseElement.installPts.map(pt=>translateThreeObj(pt.pt, deltaX, deltaY, deltaZ))
    if (baseElement.rotatePts.length!==0) baseElement.rotatePts.map(pt=>translateThreeObj(pt.pt, deltaX, deltaY, deltaZ))
    if (baseElement.linkElement.length!==0) baseElement.linkElement.map(ele=>translateBaseElement(toRaw(ele), deltaX, deltaY, deltaZ))
}

export const speecialTranslateBaseElement = function ( baseElement, deltaX, deltaY, deltaZ){
    if (baseElement.geometry!==null) 
        {
            for (let ele of baseElement.geometry){
                translateThreeObj(toRaw(ele), deltaX, deltaY, deltaZ)
              }
               // translateThreeObj(toRaw(baseElement.geometry), deltaX, deltaY, deltaZ
        }
    if (baseElement.anchorPt!==null) translateThreeObj(toRaw(baseElement.anchorPt), deltaX, deltaY, deltaZ)
    if (baseElement.installPts.length!==0){} baseElement.installPts.map(pt=>translateThreeObj(pt.pt, deltaX, deltaY, deltaZ))
    if (baseElement.rotatePts.length!==0) baseElement.rotatePts.map(pt=>translateThreeObj(pt.pt, deltaX, deltaY, deltaZ))
    if (baseElement.linkElement.length!==0) baseElement.linkElement.map(ele=>translateBaseElement(toRaw(ele), deltaX, deltaY, deltaZ))
}

export const specialScaleBaseElement = function ( baseElement, factorX, factorY, factorZ){
    if (baseElement.geometry!==null) 
        {
            for (let ele of baseElement.geometry){
                scaleThreeObj(toRaw(ele), factorX, factorY, factorZ)
              }
               // translateThreeObj(toRaw(baseElement.geometry), deltaX, deltaY, deltaZ
        }
    if (baseElement.anchorPt!==null) scaleThreeObj(toRaw(baseElement.anchorPt), factorX, factorY, factorZ)
    if (baseElement.installPts.length!==0){} baseElement.installPts.map(pt=>scaleThreeObj(pt.pt, factorX, factorY, factorZ))
    if (baseElement.rotatePts.length!==0) baseElement.rotatePts.map(pt=>scaleThreeObj(pt.pt, factorX, factorY, factorZ))
    if (baseElement.linkElement.length!==0) baseElement.linkElement.map(ele=>scaleBaseElement(toRaw(ele), factorX, factorY, factorZ))
}

// 缩放某个baseElement，包括其包含的所有物件
export const scaleBaseElement = function ( baseElement, factorX, factorY, factorZ){
    if (baseElement.geometry!==null) scaleThreeObj(toRaw(baseElement.geometry), factorX, factorY, factorZ)
    if (baseElement.anchorPt!==null) scaleThreeObj(toRaw(baseElement.anchorPt), factorX, factorY, factorZ)
    if (baseElement.installPts.length!==0){} baseElement.installPts.map(pt=>scaleThreeObj(pt.pt, factorX, factorY, factorZ))
    if (baseElement.rotatePts.length!==0) baseElement.rotatePts.map(pt=>scaleThreeObj(pt.pt, factorX, factorY, factorZ))
    if (baseElement.linkElement.length!==0) baseElement.linkElement.map(ele=>scaleBaseElement(toRaw(ele), factorX, factorY, factorZ))
}

// 以某点为旋转中心，进行旋转
export const rotateElementsByPt = function (elements, refCube, radius, axis, rotateCenter){
    if (refCube.children.length ===0){
        // 将物件添加到refCube中
        elements.forEach((ele)=>{
            const curGroup = addBaseElementIntoObject3d(refCube, toRaw(ele))
            translateThreeObj(curGroup, -rotateCenter[0], -rotateCenter[2], rotateCenter[1])
        })
    }
    // 旋转
    if (axis==='x') refCube.rotateX(radius)
    if (axis==='y') refCube.rotateY(radius)
    if (axis==='z') refCube.rotateZ(radius)
}
