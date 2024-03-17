
<template>
  <div>
    <p v-if="authenticated">Authenticated</p>
    <p v-else>Not Authenticated</p>
    <p v-if="show">show</p>
    <p v-else>Not show</p>
      <p>Email: {{ user.email }}</p>
      <p>Name: {{ user.first_name }} {{ user.last_name }}</p>
  </div>
  
      <button><RouterLink class="nav-link" to="/units">Units</RouterLink></button>
      <br>          
      <button><RouterLink class="nav-link" to="/addunit">Add Unit</RouterLink></button>  
      <br>    
      <button><RouterLink class="nav-link" to="/profile">Profile</RouterLink></button>  
      <br>  
      <button><RouterLink class="nav-link" to="/test">Test</RouterLink></button>  
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
    const show  = ref(false)
  
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
    show.value = true;
    router.push('/home');
  } else {
    // User is not authenticated
    show.value = false;
    router.push('/login');
  }
})
   
    const user = ref({ id: null, email: '', first_name: '', last_name: '' })

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
      show,
      user,
      logout
    }
  }
}
</script>