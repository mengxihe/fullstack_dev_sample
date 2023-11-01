import axios from "axios";

const request = axios.create({
    // 配置接口请求的基准路径
    baseURL:"http://127.0.0.1:8888"
  })
  


export const getDefaultSpoiler = () =>{
  return request({
    method:"POST",
    url:"/getSpoiler"
  })
}


export const getBuilding = (params)=>{
  return request({
      method:"POST",
      url:"/generate_building",
      data:{params}
  })
}

export const saveMyFile = (param) => {
  return request({
    method: "POST",
    url: "/save_file",
    data: {param},
  })
}


