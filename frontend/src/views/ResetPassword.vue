<template>
    <div>
      <h3 align="center">Forgot Password</h3>
      <div class="form-group">
        <label for="email">Email Address</label>
        <input v-model="email" type="email" class="form-control" id="email" name="email" placeholder="Enter email" required>
      </div>
      <button @click="resetPassword" class="btn btn-primary">Reset Password</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: ''
      };
    },
    methods: {
      resetPassword() {
        // Make an HTTP POST request to the backend
        axios.post('http://127.0.0.1:9000/forgot_password', { 
            email: this.email 
        })
          .then(response => {
            // Check the response for success or error messages
            if (response.data.success) {
              // Display success message
              
              // Redirect or perform any other actions as needed
            } else {
              // Display error message
              alert(response.data.message);
            }
          })
          .catch(error => {
            console.error('Error resetting password:', error);
            alert('An error occurred. Please try again.');
          });
      }
    }
  };
  </script>
  
  <style>
  /* Add your CSS styles here */
  </style>
  