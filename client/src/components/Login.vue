<template>
  <div class="login-contents">
    <div class="centered">
      <div v-if="!this.$parent.loggedIn">
      <!-- if there's not currently a user logged in, allow them to log in -->
        <h1>Login</h1>
        <p>Username:</p><input v-model="username" @keyup.enter="login()" type="text" />
        <p>Password:</p><input type="password" v-model="password" @keyup.enter="login()"/>
        <br><br>
        <button @click="login()">Submit</button>
        <div class="error">{{ error }}</div>
      </div>
      <div v-if="this.$parent.loggedIn"> 
      <!-- if the user is already logged in, tell them -->
        <h1>You're already logged in.</h1>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'login',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    login() {
      console.log("login.vue - login: pre-axios")
      axios.post('/login', {username: this.username, password: this.password})
      .then((resp) => {
        console.log("login.vue - post /login")
        if (resp.data.success == false){
          // if the response is a failure, the password wasn't correct - display an error
          this.error = "Your password was entered incorrectly. Try again.";
          return;
        } if (resp.data === "None") {
          // if the response is 'None', the username entered isn't valid - display an error
          this.error = "There's no user with that username. Please try again, or register as a new user."
          return;
        } else {
          console.log('test')
          // otherwise, change the status of $parent.loggedIn and redirect to homepage
          this.username = '';
          this.password = '';
          this.$parent.loggedIn = true;
        }
      });
    }
  }
}
</script>

<style scoped>
.login-contents {
  padding-top: 20px;
  display: flex;
}
.centered {
  justify-content: center;
}
.error {
  font-weight: bold;
  color: red;
  margin-top: 20px;
}
</style>
