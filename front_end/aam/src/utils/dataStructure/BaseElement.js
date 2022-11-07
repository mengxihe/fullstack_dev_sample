
class BaseElement {
    constructor(elementJson) {
        // geometry
        this.geometry = []
        this.linkElement = []
        this.parentElement = elementJson.parent_element
        this.anchorPt = null
        this.installPts = []
        this.rotatePts = []
        // semantics
        this.id = elementJson.id
        this.objectType = elementJson.object_type
        this.objectName = elementJson.object_name
        this.customSemantics = elementJson.custom_semantics
    }
    // 选择对应的点
    selectPtByLayerName(layerName, op){
        let res
        if (op===0){
            res = this.anchorPt
        }else if(op===1){
            this.installPts.forEach((ele)=>{
                if(ele.layerName===layerName){
                    res = ele
                }
            })
        }else if(op===2){
            this.rotatePts.forEach((ele)=>{
                if(ele.layerName===layerName){
                    res = ele
                }
            })
        }
        return res
    }
}
export default BaseElement

