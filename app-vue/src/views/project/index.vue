<!-- 项目 -->
<template>
  <div class="projcet">
    <div class="projcet-title">
      <span class="title-label">我的项目</span>
    </div>
    <div class="app-container">
      <div class="card add-card">
        <div class="card-content" @click="onAddAPP">
          <div class="container">
            <div class="inner">
              <PlusOutlined style="font-size: 16px;" />
              <p style="margin-top: 5px;">新建项目</p>
            </div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-content">
          <div class="container">
            <div class="title">
              <span class="title-icon">D</span>
              <span class="title-name">Demo项目1</span>
            </div>
            <div class="project_managers">
              管理员
            </div>
            <div class="department"> 部门 </div>
            <div class="description"> 描述 </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <Modal v-model:open="visabled" title="创建项目" :mask="false" @ok="handleOk">
    <Modify ref="modifyRef" />
  </Modal>
</template>

<script lang="ts" setup>
import { PlusOutlined } from '@ant-design/icons-vue';
import { Modal } from 'ant-design-vue';
import { ref } from 'vue';
import Modify from './modify.vue';

const visabled = ref(false)

const onAddAPP = () => {
  visabled.value = true
}
const modifyRef = ref()
const handleOk = (e: MouseEvent) => {
  console.dir(modifyRef.value, 'modifyRef.value==');

  modifyRef.value.onFinish()
};
</script>
<style lang='less' scoped>
.projcet {
  height: 100%;
  background-color: #fff !important;
  padding: 0 20px 0 20px;
  overflow: auto;
  box-sizing: border-box;

  .projcet-title {
    height: 64px;
    background-color: #fff;
    display: flex;
    justify-content: flex-start;
    align-items: center;

    .title-label {
      font-weight: bold;
      font-size: 20px;
      line-height: 64px;
      color: rgba(0, 0, 0, .85);
      font-weight: 700;
    }
  }

  .app-container {
    padding-top: 4px;
    margin: 0 -10px;

    .card {
      width: 20%;
      display: inline-block;
      vertical-align: top;
      padding: 0 9px 20px 9px;
      box-sizing: border-box;

      .card-content {
        width: 100%;
        border: 1px solid #e4e5eb;
        border-radius: 3px;
        height: 182px;
        background-color: #fff;
        vertical-align: middle;
        text-align: center;
        cursor: pointer;
        transition: box-shadow .1s linear, -webkit-box-shadow .1s linear;

        &:hover {
          box-shadow: 3px 3px 8px 2px rgba(0, 0, 0, .06);
        }

        .container {
          height: 100%;
          width: 100%;
          padding: 0 20px;
          text-align: left;
          box-sizing: border-box;

          .title {
            height: 56px;
            font-size: 16px;
            line-height: 56px;
            color: rgba(0, 0, 0, .85);
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
            display: flex;
            align-items: center;

            .title-icon {
              font-size: 20px;
              width: 32px;
              height: 32px;
              color: #0052d9;
              display: inline-flex;
              align-items: center;
              justify-content: center;
              background-color: #ecf2fe;
              border-radius: 3px;
              margin-right: 8px;
            }

            .title-name {
              flex: 1;
              flex-wrap: nowrap;
              display: inline-block;
              overflow: hidden;
              text-overflow: ellipsis;
              font-weight: 700;
              font-size: 18px;
            }
          }

          .project_managers,
          .department,
          .description {
            color: #666;
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
          }

          .description {
            padding: 10px 0;
            box-sizing: border-box;
            word-break: keep-all;
          }

        }

      }

      &.add-card {
        .card-content {
          border-style: dashed;

          .container {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            .inner {
              color: #999;
              text-align: center;
            }
          }
        }
      }
    }
  }
}
</style>
