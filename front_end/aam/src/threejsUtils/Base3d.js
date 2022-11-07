import * as THREE from "three"
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

class Base3d{
    constructor(selector) {
        this.container = document.querySelector(selector)
        this.camera
        this.scene
        this.control
        this.renderer
        this.init()
        this.animate()
        this.initControl()
    }
    init(){
        // 初始化场景
        this.initScene()
        // 初始化灯光
        this.initLight()
        // 初始化相机
        this.initCamera()
        // 初始化渲染器
        this.initRender()
        // resize
        window.addEventListener('resize', this.onWindowResize.bind(this))
    }
    initScene(){
        // 初始化场景
        this.scene = new THREE.Scene()
        this.scene.background = new THREE.Color( 0xffffff );
    }
    initLight(){
        // 整体环境灯
        this.scene.add( new THREE.AmbientLight( 0xffffff,  0.1) )
        // 添加一个点光源
        const light = new THREE.SpotLight( 0xfffffe, 2 );
        light.position.set( -3000, 10000, 4000 );
        light.angle = Math.PI/3;
        light.distance = 0
        light.castShadow = true;

        // light shadow
        light.shadow.camera.near = 50;
        light.shadow.camera.far = 15000;
        light.shadow.camera.fov = 50
        light.shadow.bias = - 0.000222;
        light.shadow.mapSize.width = 4098;
        light.shadow.mapSize.height = 4098;
        this.scene.add(light)

        // 添加一个底版
        const planeGeometry = new THREE.PlaneGeometry( 100000, 100000 );
        planeGeometry.rotateX( - Math.PI / 3 );
        const planeMaterial = new THREE.ShadowMaterial( { color: 0x000000, opacity: 0.2 } );
        const plane = new THREE.Mesh( planeGeometry, planeMaterial );
        plane.position.y = - 370;
        plane.receiveShadow = true;
        this.scene.add( plane );

        // 灯管辅助器
        const lightHelper = new THREE.SpotLightHelper( light );
        this.scene.add( lightHelper );
        const shadowCameraHelper = new THREE.CameraHelper( light.shadow.camera );
        this.scene.add( shadowCameraHelper );
    }
    initCamera(){
        this.camera = new THREE.PerspectiveCamera(
            50,
            window.innerWidth / window.innerHeight,
            1,
            100000
        )
        this.camera.position.set( 500, 400, 300)
    }
    initRender(){
        this.renderer = new THREE.WebGLRenderer( { antialias: true } )
        this.renderer.setPixelRatio( window.devicePixelRatio )
        this.renderer.setSize( window.innerWidth, window.innerHeight )
        this.renderer.shadowMap.enabled = true
        this.container.appendChild( this.renderer.domElement )
    }
    render(){
        this.renderer.render(this.scene, this.camera)
    }
    animate(){
        this.renderer.setAnimationLoop(this.render.bind(this))
    }
    initControl(){
        this.control = new OrbitControls( this.camera, this.renderer.domElement );
        this.control.damping = 0.5;
        this.control.addEventListener( 'change', this.render.bind(this) );
    }
    onWindowResize(){
        this.camera.aspect = window.innerWidth/window.innerHeight
        this.camera.updateProjectionMatrix()
        this.renderer.setSize(window.innerWidth, window.innerHeight)
    }
}

export default Base3d

