import {
    extractAllBaseElement,
    specialScaleBaseElement
} from "../dataStructure/ElementOpsUtils.js"
import {toRaw} from "vue";

export const adjustSpoilerBaseDistance = function (spoiler, deltaX, deltaY, deltaZ, curLength, defaultLength){
    const baseList = spoiler
    // console.log(baseList);
    const allBaseElementList = []
    for (let ele of baseList){
        const singleBaseElements = extractAllBaseElement(toRaw(ele))
        allBaseElementList.push(singleBaseElements)
      }
    // console.log(allBaseElementList)
    // const allBaseElements = extractAllBaseElement(toRaw(spoiler))
    const buildingsForTranslate = allBaseElementList[1]
    const meshList = buildingsForTranslate[0]
    const scaleFactorX = curLength/defaultLength
    // speecialTranslateBaseElement(meshList, deltaX, deltaY, deltaZ)
    specialScaleBaseElement(meshList, 1, 1, scaleFactorX)

}
