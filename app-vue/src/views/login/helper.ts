// import { timeFix } from '@/utils/utils';
// import ls from '@/utils/Storage';
import { message, } from 'ant-design-vue';


export const useGetCaptcha = (e: Event, validate: any, state: any, form: any, registerBtn: any) => {
  e.preventDefault();
  validate(['mobile']).then((res: any) => {
    state.smsSendBtn = true;
    const interval = window.setInterval(() => {
      if (state.time-- <= 0) {
        state.time = 60;
        state.smsSendBtn = false;
        window.clearInterval(interval);
      }
    }, 1000);

    message.loading('验证码发送中..', 1);

    // getSmsCaptcha({ mobile: form.mobile })
    //   .then((res) => {
    //     notification['success']({
    //       message: '提示',
    //       description: '验证码获取成功，您的验证码为：' + res.result.captcha,
    //       duration: 8,
    //     });
    //   })
    //   .catch((err) => {
    //     clearInterval(interval);
    //     state.time = 60;
    //     state.smsSendBtn = false;
    //     requestFailed(err);
    //     registerBtn && (registerBtn.value = false);
    //   });
  });
};
