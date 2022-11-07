import * as THREE from "three";

class PointElement {
    constructor(point, layerName) {
        // geometry
        this.pt = point
        this.layerName = layerName
    }
    rotatePt(rotateMatrix){
        this.pt.geometry.applyMatrix4(rotateMatrix)
    }
}
export default PointElement