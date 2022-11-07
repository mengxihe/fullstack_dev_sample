import * as THREE from "three";

// translate matrix
export const getTranslateMatrix = function (tx, ty, tz) {
    return new THREE.Matrix4().set(
        1, 0, 0, tx,
        0, 1, 0, ty,
        0, 0, 1, tz,
        0, 0, 0, 1
    )
}

// scale matrix
export const getScaleMatrix = function (sx, sy, sz){
    return new THREE.Matrix4().set(
        sx, 0, 0, 0,
        0, sy, 0, 0,
        0, 0, sz, 0,
        0, 0, 0, 1
    )
}

// X rotate matrix
export const getXRotateMatrix = function (angle) {
    return new THREE.Matrix4().set(
        1, 0, 0, 0,
        0, Math.cos(angle), Math.sin(angle), 0,
        0, -Math.sin(angle), Math.cos(angle), 0,
        0, 0, 0, 1
    )
}

// Y rotate matrix
export const getYRotateMatrix = function (angle) {
    return new THREE.Matrix4().set(
        Math.cos(angle), 0, -Math.sin(angle), 0,
        0, 1, 0, 0,
        Math.sin(angle), 0, Math.cos(angle), 0,
        0, 0, 0, 1
    )
}

// Z rotate matrix
export const getZRotateMatrix = function (angle) {
    return new THREE.Matrix4().set(
        Math.cos(angle), -Math.sin(angle), 0, 0,
        Math.sin(angle), Math.sin(angle), 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    )
}