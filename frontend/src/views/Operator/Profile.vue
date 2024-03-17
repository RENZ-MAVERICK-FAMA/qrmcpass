<template>
    <div>
      <p v-if="authenticated">Authenticated</p>
      <p v-else>Not Authenticated</p>
      <p v-if="show">show</p>
      <p v-else>Not show</p>
      
      <div v-if="editable">
         <div class="form-group">
            <label for="email">Email Address</label>
            <input
              type="email"
              class="form-control"
              id="email"
              v-model="user.email"
              placeholder="Enter email"
              required />
          </div>
          <div class="form-group">
            <label for="firstName">First Name</label>
            <input
              type="text"
              class="form-control"
              id="firstName"
              v-model="user.first_name"
              placeholder="Enter first name"
              required minlength="1" />
          </div>
          <div class="form-group">
            <label for="lastName">Last Name</label>
            <input
              type="text"
              class="form-control"
              id="lastName"
              v-model="user.last_name"
              placeholder="Enter last name"
              required minlength="1" />
          </div>
          <div class="form-group">
            <label for="address">Address</label>
            <input
              type="text"
              class="form-control"
              id="address"
              v-model="user.address"
              placeholder="Enter address"
              required />
          </div>
          <div class="form-group">
            <label for="license">License Number</label>
            <input type="text" class="form-control" id="license" v-model="user.license" name="license" placeholder="Enter license number" required unique />
          </div>
          <div class="form-group">
            <label for="permit">Permit</label><br>
            <input type="file" id="permit" @change="handleFileChange" required />
          </div>   
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="user.password"
              placeholder="Enter new password"
              required minlength="7" />
          </div>
          <br />
          <button @click="updateUser">Update</button>
      </div>
      
      <div v-else>
        <p>Email: {{ user.email }}</p>
        <p>Name: {{ user.first_name }} {{ user.last_name }}</p>
        <p>Address: {{ user.address }}</p>
        <p>License: {{ user.license }}</p>
        <p>Permit:</p><img :src="'http://127.0.0.1:9000/static/permit/' + user.permit" alt="Permit" style="width: 220px; height: 220px;">
        <br>
      <button @click="editUser">Edit</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  
  export default {
    setup() {
      const authenticated = ref(false)
      const show = ref(false)
      const editable = ref(false)
  
      const route = useRoute()
      const router = useRouter()
  
      // Check authentication status
      if (localStorage.getItem('access_token')) {
        authenticated.value = true
        show.value = true
      }
  
      watch(authenticated, (newValue) => {
        if (newValue) {
          // User is authenticated
          show.value = true
          router.push('/home')
        } else {
          // User is not authenticated
          show.value = false
          router.push('/login')
        }
      })
  
      const user = ref({ id: null, email: '', first_name: '', last_name: '', address: '', license: '', password: '', permit: '' })
  
      axios.get('http://127.0.0.1:9000/user', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
        .then(response => {
          // Assuming response.data contains the user details
          user.value = response.data
        })
        .catch(error => {
          console.error('Error fetching user:', error)
        })
  
      const updateUser = () => {
        axios.put('http://127.0.0.1:9000/updateuser', user.value, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
          .then(response => {
            // Handle successful update
            console.log(response.data.message)
            editable.value = false
          })
          .catch(error => {
            // Handle update error
            console.error(error.response.data.message)
          })
      }
  
      const editUser = () => {
        editable.value = true
      }
  
      const logout = () => {
        axios.post('http://127.0.0.1:9000/logout')
          .then(response => {
            // Handle successful logout
            console.log(response.data.message)
            // Remove access token from local storage
            localStorage.removeItem('access_token')
            // Redirect to the login page
            router.push('/login')
          })
          .catch(error => {
            // Handle logout error
            console.error(error.response.data.message)
          })
      }
  
      const handleFileChange = (event) => {
        const file = event.target.files[0]
        user.value.permit = file
      }
  
      return {
        authenticated,
        show,
        editable,
        user,
        updateUser,
        editUser,
        logout,
        handleFileChange
      }
    }
  }
  </script>
  
  <style>
  /* Add any custom styles for the form here */
  </style>
  