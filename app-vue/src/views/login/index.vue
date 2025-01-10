<!-- 登录页面 -->
<template>
  <div class="main">
    <a-form id="formLogin" class="user-layout-login" @submit="handleSubmit" :model="formRef">
      <a-tabs :activeKey="formRef.type" :tabBarStyle="{ textAlign: 'center', borderBottom: 'unset' }"
        @change="handleTabClick">
        <!-- 账户密码登录 -->
        <a-tab-pane key="passwordType" tab="密码登录">
          <a-alert v-if="isLoginError" type="error" showIcon style="margin-bottom: 24px" message="账户或密码错误" />
          <a-form-item v-bind="validateInfos.phone">
            <a-input size="large" type="text" placeholder="邮箱/手机号码" v-model:value="formRef.phone">
              <template #prefix>
                <UserOutlined :style="{ color: 'rgba(0,0,0,.25)' }" />
              </template>
            </a-input>
          </a-form-item>

          <a-form-item v-bind="validateInfos.password">
            <a-input-password size="large" placeholder="登录密码" v-model:value="formRef.password">
              <template #prefix>
                <LockOutlined :style="{ color: 'rgba(0,0,0,.25)' }" />
              </template>
            </a-input-password>
          </a-form-item>
        </a-tab-pane>
        <!-- 手机号登录 -->
        <!-- <a-tab-pane :disabled="true" key="phoneType" tab="手机号登录">
          <a-form-item v-bind="validateInfos.mobile">
            <a-input size="large" type="text" placeholder="输入手机号" v-model:value="formRef.mobile">
              <MobileOutlined :style="{ color: 'rgba(0,0,0,.25)' }" />
            </a-input>
          </a-form-item>
          <a-row :gutter="16">
            <a-col class="gutter-row" :span="16">
              <a-form-item v-bind="validateInfos.captcha">
                <a-input size="large" type="text" placeholder="输入验证码" v-model:value="formRef.captcha">
                  <MailOutlined :style="{ color: 'rgba(0,0,0,.25)' }" />
                </a-input>
              </a-form-item>
            </a-col>
            <a-col class="gutter-row" :span="8">
              <a-button class="getCaptcha" tabindex="-1" :disabled="state.smsSendBtn" @click.stop.prevent="getCaptcha">
                {{ (!state.smsSendBtn && "获取验证码") || state.time + " s" }}
              </a-button>
            </a-col>
          </a-row>
        </a-tab-pane> -->
      </a-tabs>

      <a-form-item v-bind="validateInfos.rememberMe">
        <a-checkbox v-model:checked="formRef.rememberMe" style="float: left">
          自动登录
        </a-checkbox>
        <router-link to="/" class="forge-password" style="float: right">
          忘记密码
        </router-link>
      </a-form-item>

      <a-form-item style="margin-top: 24px">
        <a-button size="large" type="primary" htmlType="submit" class="login-button" :loading="state.loginBtn"
          :disabled="state.loginBtn">
          登录
        </a-button>
      </a-form-item>

      <!-- <div class="user-login-other">
        <span>其他登录方式</span>
        <a>
          <AlipayCircleOutlined />
        </a>
        <a>
          <TaobaoCircleOutlined />
        </a>
        <a>
          <WeiboCircleOutlined />
        </a>
        <router-link class="register" :to="{ name: 'register' }">
          注册账户
        </router-link>
      </div> -->
    </a-form>
  </div>
</template>

<script lang="ts" setup>
import { Form, notification } from "ant-design-vue";
import { defineComponent, UnwrapRef, reactive, ref } from "vue";
// import { LoginFormStateStruct, LoginResStruct } from "@/interface/user";
import {
  MobileOutlined,
  MailOutlined,
  AlipayCircleOutlined,
  TaobaoCircleOutlined,
  WeiboCircleOutlined,
  UserOutlined,
  LockOutlined,
} from "@ant-design/icons-vue";
import { useGetCaptcha } from "./helper";
import { getQueryVariable, timeFix } from "@/utils/utils";
import { useRouter, useRoute } from "vue-router";
import { useAppStore } from "@/store/app";

const appStore = useAppStore()

const useForm = Form.useForm;
const isLoginError = ref(false);
const router = useRouter();
const route = useRoute();

// #region 表单相关
const formRef: UnwrapRef<any> = reactive({
  rememberMe: false,
  phone: "",
  password: "",
  mobile: "",
  captcha: "",
  type: "passwordType",
});
/** 表单 */
const handleSubmit = (e: Event) => {
  e.preventDefault();
  state.loginBtn = true;
  const validateFieldsKey =
    formRef.type === "passwordType"
      ? ["phone", "password"]
      : ["mobile", "captcha"];

  validate(validateFieldsKey)
    .then(async () => {
      // formRef.password = encryptByMd5(formRef.password);
      state.loginBtn = true;
      appStore.login(formRef)
        .then((result: any) => {
          state.loginBtn = false;
          notification.success({
            message: "欢迎",
            description: `${timeFix()}，欢迎回来`,
          });
          setTimeout(() => {
            const url: any = route.query?.redirect ?? "/";
            router.push({ path: url });
          }, 500);
        })
        .catch((err) => {
          state.loginBtn = false;
        });
    })
    .catch((e) => {
      state.loginBtn = false;
    });
};

/** 标签页 */
const handleTabClick = (key: any) => {
  formRef.type = key;
};

const state = reactive({
  time: 60,
  loginBtn: false,
  // login type: 0 email, 1 phone, 2 telephone
  loginType: 0,
  smsSendBtn: false,
});

const handlephoneOrEmail = (_rule: any, value: string) => {
  const regex =
    /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
  if (regex.test(value)) {
    state.loginType = 0;
  } else {
    state.loginType = 1;
  }
  return Promise.resolve();
};
const rulesRef = reactive({
  rememberMe: [{ trigger: "checked" }],
  phone: [
    {
      required: true,
      message: "请输入邮箱地址或手机号码",
    },
    {
      validator: handlephoneOrEmail,
      trigger: "change",
    },
  ],
  password: [{ required: true, message: "请输入登录密码！" }, {}],
  mobile: [
    {
      required: true,
      pattern: /^1[345678]\d{9}$/,
      message: "输入手机号",
      validateTrigger: "change",
    },
  ],
  captcha: [
    {
      required: true,
      message: "请输入验证码！",
      validateTrigger: "blur",
    },
  ],
});
const { validate, validateInfos } = useForm(formRef, rulesRef);

//#region 获取验证码
const getCaptcha = (e: Event) => {
  useGetCaptcha(e, validate, state, formRef, null);
};
//#endregion
</script>
<style lang='less' scoped>
.user-layout-login {
  label {
    font-size: 14px;
  }

  ::v-deep(.ant-tabs-nav-wrap) {
    justify-content: center;
  }

  .getCaptcha {
    display: block;
    width: 100%;
    height: 40px;
  }

  .forge-password {
    font-size: 14px;
  }

  button.login-button {
    padding: 0 15px;
    font-size: 16px;
    height: 40px;
    width: 100%;
  }

  .user-login-other {
    text-align: left;
    margin-top: 24px;
    line-height: 22px;

    .anticon {
      font-size: 24px;
      color: rgba(0, 0, 0, 0.2);
      margin-left: 16px;
      vertical-align: middle;
      cursor: pointer;
      transition: color 0.3s;

      &:hover {
        color: #1889f1;
      }
    }

    .register {
      float: right;
    }
  }
}
</style>
