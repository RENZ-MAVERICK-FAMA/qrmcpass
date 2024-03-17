<template>
    <div>
     
  
      <div class="container">
        <div class="form-container">
        
          <form @submit.prevent="login">
            <div class="form-group">
              <label for="username">Collector Username</label>
              <input v-model="formData.username" type="text" class="form-control" id="username" placeholder="Enter username">
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input v-model="formData.password" type="password" class="form-control" id="password" placeholder="Enter password">
            </div> 
            <RouterLink class="nav-link" id="reset"  to="/reset">forgot password?</RouterLink>
            <br>
            <button type="submit" class="btn btn-primary">Login</button>
           
          </form>
  
          <div v-if="loginError" class="alert alert-danger" role="alert">
            {{ loginError }}
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        formData: {
            username: '',
          password: ''
        },
        loginError: ''
      };
    },
    methods: {
    login() {
      axios.post('http://127.0.0.1:9000/loginTeller', this.formData)
        .then(response => {
          // Store the access token in local storage
          localStorage.setItem('access_token', response.data.access_token);
          // Redirect to the home page or perform any other action
          if (localStorage.getItem('access_token')) {
            
            this.$router.push('/homeTeller');
            
            window.location.href = '/homeTeller'; // No need for this line
          }
        })
        .catch(error => {
          this.loginError = error.response.data.message;
          console.error(this.loginError);
        });
    }
  },
    
    created() {
      if (localStorage.getItem('access_token')) {
        this.$emit('authenticated', { authenticated: true, show: true });
  
      }
    }
  };
  </script>
  <style scoped>
  /* Navbar styles */
  .navbar {
    display: flex;
    justify-content: flex-start;
  }
  
  
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* Adjust the height as needed */
  }
  #reset {
      color: black;
      transition: color 0.3s ease;
  }
  
  #reset:hover {
      color: rgb(3, 112, 255);
  }
  .alert {
    margin-top: 15px;
  }
  </style>
  