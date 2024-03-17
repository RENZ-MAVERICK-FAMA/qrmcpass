<template>
  <div>
    <p v-if="authenticated">Authenticated</p>
    <p v-else>Not Authenticated</p>

    <p>Unit: {{ unit.unit_info }}</p>

    <div>
      <strong>Balance: {{ balance }}</strong>
    </div>
    <strong><img :src="'http://127.0.0.1:9000/static/qrcodes/' + unit.qrcode" alt="QR Code" style="width: 400px; height: 400px;"></strong>
  </div>
</template>

<script>
import { ref, watch, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

export default {
  setup() {
    const authenticated = ref(false)
    const route = useRoute()
    const router = useRouter()
    const unit = ref({ id: null, unit_info: '', qrcode: '' })
    const balance = ref(null)

    // Check authentication status
    if (localStorage.getItem('access_token')) {
      authenticated.value = true
    }

    // Watch for changes in the authenticated flag
    watch(authenticated, (newValue) => {
      if (newValue) {
        // User is authenticated
        router.push('/homeunit')
      } else {
        // User is not authenticated
        router.push('/loginUnit')
      }
    })

    const fetchBalances = (unitId) => {
      axios.get(`http://127.0.0.1:9000/unit/${unitId}/balances`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
        .then(response => {
          balance.value = response.data.balances[0].balance;
        })
        .catch(error => {
          console.error('Error fetching balances for unit:', unitId, error);
        });
    };

    const intervalId = setInterval(() => {
      fetchBalances(unit.value.id);
    }, 500);

    onUnmounted(() => {
      clearInterval(intervalId);
    });

    axios.get('http://127.0.0.1:9000/unitdetails', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
      .then(response => {
        // Assuming response.data contains the user details
        unit.value = response.data
        fetchBalances(unit.value.id);
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
        })
        .catch(error => {
          // Handle logout error
          console.error(error.response.data.message)
        })
    }

    return {
      authenticated,
      unit,
      balance,
      logout
    }
  },
}
</script>
