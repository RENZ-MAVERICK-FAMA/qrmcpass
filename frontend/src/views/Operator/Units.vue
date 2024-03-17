<template>
  <div>
    <h1>Units</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Unit Info</th>
          <th>Unit Type</th>
          <th>QR Code</th>
          <th>Color</th>
          <th>Balance</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="unit in units" :key="unit.id">
          <td>{{ unit.unit_info }}</td>
          <td>{{ unit.unit_type }}</td>
          <td><img :src="'http://127.0.0.1:9000/static/qrcodes/' + unit.qrcode" alt="QR Code" style="width: 70px; height: 70px;"></td>
          <td>{{ unit.color }}</td>
          <td v-for="balance in unit.balances" :key="balance.id">{{ balance.balance }}</td>
          <td>
            <button type="button" class="btn btn-primary" @click="fetchTransactions(unit)">
              View Transactions
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal -->
    <div class="modal fade" id="transactionsModal" tabindex="-1" role="dialog" aria-labelledby="transactionsModalLabel" aria-hidden="true" ref="transactionsModal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="transactionsModalLabel">Transactions</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="closeModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <table class="table">
              <thead>
                <tr>
                  <th>Amount</th>
                  <th>Date</th>
                  <th>Teller</th>
                  <th>Branch</th>
                  <th>Date of Payment</th>
                  <th>Type</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="transaction in selectedUnitTransactions" :key="transaction.id">
                  <td>{{ transaction.amount }}</td>
                  <td>{{ transaction.date }}</td>
                  <td>{{ transaction.teller }}</td>
                  <td>{{ transaction.branch }}</td>
                  <td>{{ transaction.date_of_payment }}</td>
                  <td><strong>{{ transaction.type.name.split('.')[-1] }}</strong></td>
                </tr>
              </tbody>
            </table>
          </div>
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
      units: [],
      selectedUnitTransactions: []
    };
  },
  created() {
    this.fetchUnits();
    
  },
  methods: {
    fetchUnits() {
      axios.get('http://127.0.0.1:9000/user/units', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      .then(response => {
        this.units = response.data.units;
        this.fetchBalances();
      })
      .catch(error => {
        console.error('Error fetching user units:', error);
      });
    },
    fetchTransactions(unit) {
      axios.get(`http://127.0.0.1:9000/unit/${unit.id}/transactions`, {
        headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      'Content-Type': 'application/json'
    }
      })
      .then(response => {
        this.selectedUnitTransactions = response.data.transactions;
        $('#transactionsModal').modal('show'); // Show the modal
        this.showModal = true;
      })
      .catch(error => {
        console.error('Error fetching transactions for unit:', unit.id, error);
      });
    },
    fetchBalances() {
      setInterval(() => {
        this.units.forEach(unit => {
          axios.get(`http://127.0.0.1:9000/unit/${unit.id}/balances`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
          })
          .then(response => {
            unit.balances = response.data.balances;
          })
          .catch(error => {
            console.error('Error fetching balances for unit:', unit.id, error);
          });
        });
      }, 500);
    }, showTransactions(unit) {
  this.selectedUnitTransactions = unit.transactions;
  $('#transactionsModal').modal('show'); // Show the modal
  this.showModal = true;
},
  
    closeModal() {
      $('#transactionsModal').modal('hide');
      this.showModal = false;
    }
  }
};
</script>
