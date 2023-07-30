<template>
<div class="login-box">
  <div class="align-items-center">
    로그인
    <div>
      <input  class="btn btn-secondary login-form my-3" placeholder="username" type="text" v-model="credentials.username">
    </div>
    <div>
      <input  class="btn btn-secondary login-form my-3" placeholder="password" type="password" v-model="credentials.password" @keypress.enter="login">
    </div>
    <button class="btn btn-secondary login-form my-3" @click="login">login</button>
  </div>
</div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: '',
        password: '',
      }
    }
  },
  methods: {
    setToken : function () {
      const token = localStorage.getItem('jwt')
      const config = {
        headers : {
          Authorization : `JWT ${token}`,
        }
      }
      return config
    },
    login: function () {
      axios.post(`${SERVER_URL}/accounts/api-token-auth/`, this.credentials)
      .then((res) => {
        localStorage.setItem('jwt',res.data.token)
        const config = this.setToken()
        axios.get(`${SERVER_URL}/accounts/get_username/`,config)
        .then((res)=>{
          localStorage.setItem('username',res.data.username)
          localStorage.setItem('user_id',res.data.user_id)
          localStorage.setItem('is_superuser',res.data.is_superuser)
          localStorage.setItem('favorite_genres',JSON.stringify(res.data.favorite_genres))       
          this.$emit('login')
          window.location.href=`http://localhost:8080/home`

        })
        
        // this.$router.push({name : "Home"})
      })
    }
  }
}
</script>

<style>
.login-form {
  min-width: 5%;
}
::placeholder { 
  color: white;
  opacity: 1;
  font-weight: bold;
}
.login-box {
  position: relative;
  width : 100%;
  min-height: 90vh;
  display: flex;
  justify-content: center;
  align-items:center;
  overflow: hidden;
  padding: 100px;
}

</style>