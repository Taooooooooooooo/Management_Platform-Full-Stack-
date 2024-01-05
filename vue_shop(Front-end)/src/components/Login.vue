<template>
    <div class="login_container">
        <div class="login_box">
            <div class="logo">
                <img src="../assets/logo.png" alt="">
            </div>
            <el-form ref="userRef" :rules="userRules" :model="userForm" label-width="0px" class="form_style">
                <el-form-item prop="name">
                    <el-input v-model="userForm.name" prefix-icon="el-icon-user-solid" placeholder="用户名"></el-input>
                </el-form-item>
                <el-form-item prop="pwd">
                    <el-input show-password v-model="userForm.pwd"  prefix-icon="el-icon-shopping-bag-2" placeholder="密码"></el-input>
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="primary" @click="login">登录</el-button>
                    <el-button @click="restForm">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      userForm: {
        name: 'dc',
        pwd: '123'
      },
      userRules: {
        name: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 6, message: '长度在 2 到 6 个字符', trigger: 'blur' }
        ],
        pwd: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    restForm () {
    //   console.log(this)
      this.$refs.userRef.resetFields()
    },
    login () {
      this.$refs.userRef.validate(async valid => {
        // console.log(valid)
        if (!valid) return
        const { data: res } = await this.$axios.post('/user/login', this.$qs.stringify(this.userForm))
        if (res.status === 200) {
          // 1. 登录成功后，获取到token, 保存token,保存到sessionStorage中
          window.sessionStorage.setItem('token', res.data.token)
          // 登录成功了
          this.$msg.success(res.msg)
          // 跳转成功页面
          this.$router.push('/home')
        } else {
          this.$msg.error(res.msg)
        }
      })
    }
  }
}
</script>

<style lang='less' scoped>
    .login_container {
      background-color:darksalmon;
      height: 100%;
    }
    .login_box {
        width: 450px;
        height: 300px;
        border-radius:5px;
        background-color: #fff;
        position: absolute;
        left:50%;
        top:50%;
        transform: translate(-50%,-50%)
    }
    .logo {
        height: 80px;
        width: 200px;
        border: 1px solid #eee;
        padding: 10px;
        border-radius: 10%;
        position: absolute;
        left:50%;
        transform: translate(-50%,-50%);
        box-shadow: 0 0 10px #ddd;
        img {
            width: 100%;
            height: 100%;
        }
    }
    .form_style{
        position:absolute;
        bottom: 0;
        width: 100%;
        padding: 0 10%;
        box-sizing: border-box;
    }
    .btns{
        display: flex;
        justify-content: flex-end;
    }
</style>
