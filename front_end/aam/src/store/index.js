import { createStore } from "vuex";

const store = createStore ({
    state () {
        return {
            defaultModelingParams:{
                buildingHight:14.0,
                l1RoadWidth:7.0,
                l2RoadWidth:3.0,
                l4RoadWidth:3.0,
                treeDensity:5,
            },
            // 改装参数
            modelingParams:{
                buildingHight:14.0,
                l1RoadWidth:7.0,
                l2RoadWidth:3.0,
                l4RoadWidth:3.0,
                treeDensity:5,
            },
            materialParams:null,
            // default spoiler
            defaultSpoiler:null,
            // transform 
            refCube:null,
            
            offsetRecord:null,

            fileDownload:null,
        }
    },
    mutations: {
        commitModelingParams(state, payload){
            console.log('modeling params. has been updated')
            state.modelingParams.buildingHight = payload.buildingHight
            state.modelingParams.l1RoadWidth = payload.l1RoadWidth
            state.modelingParams.l2RoadWidth = payload.l2RoadWidth
            state.modelingParams.l4RoadWidth = payload.l4RoadWidth
            state.modelingParams.treeDensity = payload.treeDensity
        },
        commitDefaultSpoiler(state, payload){
            state.defaultSpoiler = payload
        },
        commitRefCube(state, payload){
            state.refCube = payload
        },
        commitOffsetRecord(state, payload){
            state.offsetRecord = payload
        },
        commitFileDownload(state, payload){
            state.fileDownload = payload
        }
    },
    actions: {

    },
    modules: {
        
    }
})

export default store