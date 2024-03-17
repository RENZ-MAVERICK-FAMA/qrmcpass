
<template>
    
    
        
        <button><RouterLink class="nav-link" to="/topup">Add Balance</RouterLink></button> 
        <br> 
        <button><RouterLink class="nav-link" to="/deduct">Deduct</RouterLink></button>  
        <br>       
      
  </template>
  RouterView
  <script>
  import { ref, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  
  export default {
    setup() {
      const authenticated = ref(false)
    
    
      const route = useRoute()
      const router = useRouter()
  
      // Check authentication status
      if (localStorage.getItem('access_token')) {
        authenticated.value = true
    
      
      }
  
      watch(authenticated, (newValue) => {
    if (newValue) {
      // User is authenticated
   
      router.push('/homeTeller');
    } else {
      // User is not authenticated
      
      router.push('/login');
    }
  })
     
  const teller = ref({ id: null, username: '', first_name: '', last_name: '' })

axios.get('http://127.0.0.1:9000/Teller', {
  headers: {
    Authorization: `Bearer ${localStorage.getItem('access_token')}`
  }
})
.then(response => {
  // Assuming response.data contains the user details
  teller.value = response.data
})
.catch(error => {
  console.error('Error fetching user:', error)
})
  
      const logout = () => {
        axios.post('http://127.0.0.1:9000/logout')
          .then(response => {
            // Handle successful logout
            console.log(response.data.message)
            // Remove access token from local storage
            localStorage.removeItem('access_token')
            // Redirect to the login page
            router.push('/login')
            
            // window.location.href = '/'; // Not needed if using router.push
            
          })
          .catch(error => {
            // Handle logout error
            console.error(error.response.data.message)
          })
      }
  
      return {
        authenticated,
        logout
      }
    }
  }
  </script>