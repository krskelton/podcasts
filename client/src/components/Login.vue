<template>
  <div v-if="this.$parent.loggedIn"> 
  <!-- if the user is already logged in, tell them -->
    <h1>You're already logged in.</h1>
  </div>
  <div v-else class="login-contents">
  <!-- if there's not currently a user logged in, allow them to log in -->
    <h1>Login</h1>
    <p>Username:</p>
    <input v-model="username" @keyup.enter="login()" type="text" />
    <p>Password:</p><input type="password" v-model="password" @keyup.enter="login()"/>
    <br><br>
    <button @click="login()">Submit</button>
    <div class="error">{{ error }}</div>
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
      axios.post('/login', {username: this.username, password: this.password})
      .then((resp) => {
        if (resp.data.success == false){
          // if the response is a failure, the password wasn't correct - display an error
          this.error = "Your password was entered incorrectly. Try again.";
          return;
        } if (resp.data === "None") {
          // if the response is 'None', the username entered isn't valid - display an error
          this.error = "There's no user with that username. Please try again, or register as a new user."
          return;
        } else {
          this.$parent.userInSession = this.username;
          // otherwise, change the status of $parent.loggedIn and redirect to homepage
          this.username = '';
          this.password = '';
          this.$parent.loggedIn = true;
          this.$parent.modalText = "Welcome back, " + this.$parent.userInSession;
          this.$parent.openModal();
          this.$router.push('/subscriptions');
        }
      });
    }
  }
}
</script>

<style scoped>
.login-contents {
  padding-top: 20px;
}
.error {
  font-weight: bold;
  color: red;
  margin-top: 20px;
}
</style>
