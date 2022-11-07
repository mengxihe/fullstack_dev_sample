
export const rhinoModelLoader = function (modelName, loader){
    return new Promise(function (resolve,reject){
        loader.load(modelName, function (obj) {
            obj.rotateX(-90*(Math.PI/180))
            resolve(obj)
        })
    })
}

export const file3dmLoader = function (file3dm, loader){
    const buffer = convertBase64ToBuffer(file3dm)
    return new Promise(function (resolve, reject){
        loader.parse(buffer, function (obj){
            resolve(obj)
        })
    })
}

const convertBase64ToBuffer = function (base64){
    const arrBuffer = base64ToArrayBuffer(base64)
    return new Uint8Array(arrBuffer).buffer
}

const base64ToArrayBuffer = function (base64){
    var binaryString = window.atob(base64)
    var len = binaryString.length
    var bytes = new Uint8Array(len)
    for (var i=0;i<len;i++){
        bytes[i] = binaryString.charCodeAt(i)
    }
    return bytes.buffer
}