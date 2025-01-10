<!--
 * @Description: 注册
 * @Version: 1.0
 * @Autor: jiajun wu
 * @Date: 2021-11-30 14:11:00
 * @LastEditors: jiajun wu
 * @LastEditTime: 2021-12-01 14:55:30
-->
<!-- 注册 -->
<template>
  <div class="main user-layout-register">
    <h3>
      <span>注册</span>
    </h3>
    <a-form id="formRegister" :model="formState">
      <a-popover
        placement="rightTop"
        trigger="click"
        :visible="passwordLevelChecked"
      >
        <template #content>
          <div :style="{ width: '240px' }">
            <div :class="['user-register', passwordLevelClass]">
              {{ passwordLevelName }}
            </div>
            <a-progress
              :percent="state.percent"
              :showInfo="false"
              :strokeColor="passwordLevelColor"
            />
            <div style="margin-top: 10px">
              <span>请至少输入 6 个字符。请不要使用容易被猜到的密码。</span>
            </div>
          </div>
        </template>
        <a-form-item v-bind="validateInfos.password">
          <a-input-password
            size="large"
            @click="handlePasswordInputClick"
            placeholder="请至少输入 6 个字符。请不要使用容易被猜到的密码。"
            v-model:value="formState.password"
          ></a-input-password>
        </a-form-item>
      </a-popover>

      <a-form-item v-bind="validateInfos.confirmPassword">
        <a-input-password
          size="large"
          placeholder="确认密码"
          v-model:value="formState.confirmPassword"
        ></a-input-password>
      </a-form-item>

      <a-form-item v-bind="validateInfos.mobile">
        <a-input
          size="large"
          placeholder="输入手机号"
          v-model:value="formState.mobile"
        >
          <template #addonBefore>
            <a-select size="large" defaultValue="+86">
              <a-select-option value="+86">+86</a-select-option>
              <a-select-option value="+87">+87</a-select-option>
            </a-select>
          </template>
        </a-input>
      </a-form-item>

      <a-row :gutter="16">
        <a-col class="gutter-row" :span="16">
          <a-form-item v-bind="validateInfos.captcha">
            <a-input
              size="large"
              type="text"
              placeholder="输入验证码"
              v-model:value="formState.captcha"
            >
              <template #prefix>
                <MailOutlined :style="{ color: 'rgba(0,0,0,.25)' }" />
              </template>
            </a-input>
          </a-form-item>
        </a-col>
        <a-col class="gutter-row" :span="8">
          <a-button
            class="getCaptcha"
            size="large"
            :disabled="state.smsSendBtn"
            @click.stop.prevent="getCaptcha"
          >
            {{ (!state.smsSendBtn && "获取验证码") || state.time + " s" }}
          </a-button>
        </a-col>
      </a-row>

      <a-form-item>
        <a-button
          size="large"
          type="primary"
          htmlType="submit"
          class="register-button"
          :loading="registerBtn"
          @click.stop.prevent="handleSubmit"
          :disabled="registerBtn || true"
        >
          注册
        </a-button>
        <router-link class="login" :to="{ name: 'login' }">
          使用已有账户登录
        </router-link>
      </a-form-item>
    </a-form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed } from "vue";
import { Form } from "ant-design-vue";
import { scorePassword } from "@/utils/utils";
import { MailOutlined } from "@ant-design/icons-vue";
import { useRouter } from "vue-router";
import { useGetCaptcha } from "./helper";

const levelNames: any = {
  0: "强度：太短",
  1: "强度：低",
  2: "强度：中",
  3: "强度：强",
};
const levelClass: any = {
  0: "error",
  1: "error",
  2: "warning",
  3: "success",
};
const levelColor: any = {
  0: "#ff0000",
  1: "#ff0000",
  2: "#ff7e05",
  3: "#52c41a",
};

export default defineComponent({
  name: "Register",
  components: {
    MailOutlined,
  },
  setup() {
    const router = useRouter();
    const useForm = Form.useForm;
    let passwordLevelChecked = ref(false);

    // 表单相关
    const formState = reactive({
      email: "",
      password: "",
      confirmPassword: "",
      mobile: "",
      captcha: "",
    });
    const handlePasswordLevel = (_rule: any, value: string) => {
      if (value === "") {
        return Promise.resolve();
      }
      if (value.length >= 6) {
        if (scorePassword(value) >= 30) {
          state.level = 1;
        }
        if (scorePassword(value) >= 60) {
          state.level = 2;
        }
        if (scorePassword(value) >= 80) {
          state.level = 3;
        }
      } else {
        state.level = 0;
        return Promise.reject(new Error("密码强度不够"));
      }
      state.passwordLevel = state.level;
      state.percent = state.level * 33;

      return Promise.resolve();
    };
    const handlePasswordCheck = (rule: any, value: string | undefined) => {
      const password = formState.password;
      if (value === undefined) {
        return Promise.reject(new Error("请输入登录密码！"));
      }
      if (value && password && value.trim() !== password.trim()) {
        return Promise.reject(new Error("两次输入的密码不匹配!"));
      }
      return Promise.resolve();
    };
    const rules = reactive({
      email: [
        { required: true, type: "email", message: "请输入邮箱地址！" },
        { validateTrigger: ["change", "blur"] },
      ],
      password: [
        { required: true, message: "请输入登录密码！" },
        { validator: handlePasswordLevel },
        { validateTrigger: ["change", "blur"] },
      ],
      confirmPassword: [
        { required: true, message: "请输入登录密码！" },
        { validator: handlePasswordCheck },
        { validateTrigger: ["change", "blur"] },
      ],
      mobile: [
        {
          required: true,
          message: "请输入正确的手机号",
          pattern: /^1[3456789]\d{9}$/,
        },
        { validateTrigger: ["change", "blur"] },
      ],
      captcha: [
        { required: true, message: "请输入验证码" },
        { validateTrigger: ["change", "blur"] },
      ],
    });
    const { validate, validateInfos } = useForm(formState, rules);
    const handleSubmit = () => {
      validate().then((res) => {
        passwordLevelChecked.value = false;
        console.log({
          params: { ...formState },
        });

        // router.push({ name: "registerResult", params: { ...formState } });
      });
    };

    const state = reactive({
      time: 60,
      level: 0,
      smsSendBtn: false,
      passwordLevel: 0,
      percent: 10,
      progressColor: "#FF0000",
    });

    // 密码检查相关
    const registerBtn = ref(false);
    const passwordLevelClass = computed(() => {
      return levelClass[state.passwordLevel];
    });
    const passwordLevelName = computed(() => {
      return levelNames[state.passwordLevel];
    });
    const passwordLevelColor = computed(() => {
      return levelColor[state.passwordLevel];
    });
    const handlePasswordInputClick = () => {
      passwordLevelChecked.value = true;
    };

    /// 获取验证码
    const getCaptcha = (e: Event) => {
      useGetCaptcha(e, validate, state, formState, registerBtn);
    };

    return {
      state,
      registerBtn,
      validateInfos,
      formState,
      passwordLevelClass,
      passwordLevelName,
      passwordLevelColor,
      handlePasswordInputClick,
      handleSubmit,
      getCaptcha,
      rules,
      passwordLevelChecked,
    };
  },
});
</script>
<style lang="less">
.user-register {
  &.error {
    color: #ff0000;
  }

  &.warning {
    color: #ff7e05;
  }

  &.success {
    color: #52c41a;
  }
}

.user-layout-register {
  .ant-input-group-addon:first-child {
    background-color: #fff;
  }
}
</style>
<style lang="less" scoped>
.user-layout-register {
  & > h3 {
    font-size: 16px;
    margin-bottom: 20px;
  }

  .getCaptcha {
    display: block;
    width: 100%;
    height: 40px;
  }

  .register-button {
    width: 50%;
  }

  .login {
    float: right;
    line-height: 40px;
  }
}
</style>
