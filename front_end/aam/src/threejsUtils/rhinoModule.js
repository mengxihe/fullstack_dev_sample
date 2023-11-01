import rhino3dm from "https://cdn.jsdelivr.net/npm/rhino3dm@7.14.0/rhino3dm.module.js";
import { Rhino3dmLoader } from "three/examples/jsm/loaders/3DMLoader.js"

export const initRhinoModule = function (){
    let rhino
    rhino3dm().then(async m => {
        rhino = m; // global
    })
    return rhino
}

export const init3dmLoader = function (){
    return new Rhino3dmLoader().setPath("models/").setLibraryPath('js/')
}