<template>
    <div class="nav-bar">
      <div class="left-title-content">
        <div class="logo-img-content"><img src="../assets/imgs/logo-black.png" alt="logo" class="logo-img"></div>
        <div class="small-title-text">Solo</div>
      </div>
      <div class="right-title-content">
        <a-avatar :size="24" style="background-color: #333333"><template #icon><UserOutlined /></template></a-avatar>
      </div>
    </div>
  </template>
  
  <script setup>
  import { UserOutlined } from '@ant-design/icons-vue';
  
  </script>
  
  <style scoped lang="less">
    .nav-bar{
      width: 100vw;
      height:40px;
      background-color: white;
      box-shadow:  0px 3px 2px #eeeeee;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-left: 30px;
      padding-right: 30px;
    }
  
    .left-title-content{
      display: flex;
      justify-items: baseline;
    }
    .logo-img{
      width: 50px;
      margin-right: 10px;
    }
    .small-title-text{
      font-weight: bold;
      font-size: 80%;
      margin-top: 6px;
    }
  </style>