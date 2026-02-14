<script setup>
import {onMounted, ref, computed, watch} from "vue";
import {http} from "../api/http";
import {centsToEur} from "../utils/money";
import {useToasts} from "../stores/toasts";

const toast = useToasts();

const accounts = ref([]);
const selectedAccountId = ref("");
const balanceCents = ref(0);
const history = ref([]);
const loading = ref(false);

const dateFrom = ref(""); // YYYY-MM-DD
const dateTo = ref("");

const selectedAccount = computed(() =>
  accounts.value.find((a) => a.account_id === selectedAccountId.value)
);

const filteredHistory = computed(() => {
  const from = dateFrom.value ? new Date(dateFrom.value).getTime() : null;
  const to = dateTo.value ? new Date(dateTo.value + "T23:59:59").getTime() : null;

  return (history.value || []).filter((tx) => {
    const t = new Date(tx.created_at || tx.SK || "").getTime();
    if (Number.isNaN(t)) return true;
    if (from && t < from) return false;
    if (to && t > to) return false;
    return true;
  });
});

const incomeCents = computed(() => {
  return filteredHistory.value.reduce((acc, tx) => {
    const v = Number(tx.amount_cents || 0);
    return v > 0 ? acc + v : acc;
  }, 0);
});

const outcomeCents = computed(() => {
  return filteredHistory.value.reduce((acc, tx) => {
    const v = Number(tx.amount_cents || 0);
    return v < 0 ? acc + Math.abs(v) : acc;
  }, 0);
});

async function loadAccounts() {
  const res = await http.get("/accounts/");
  accounts.value = res.data || [];
  if (!selectedAccountId.value && accounts.value.length) {
    selectedAccountId.value = accounts.value[0].account_id;
  }
}

async function loadBalanceAndHistory() {
  if (!selectedAccountId.value) return;
  loading.value = true;
  try {
    const [b, h] = await Promise.all([
      http.get(`/transactions/balance/${selectedAccountId.value}`),
      http.get(`/transactions/history/${selectedAccountId.value}`, { params: { limit: 200 } }),
    ]);
    balanceCents.value = b.data.available_cents || 0;
    history.value = h.data || [];
  } finally {
    loading.value = false;
  }
}

watch(selectedAccountId, async () => {
  await loadBalanceAndHistory();
});

onMounted(async () => {
  try {
    await loadAccounts();
    await loadBalanceAndHistory();
  } catch (e) {
    toast.push({
      type: "error",
      title: "Load failed",
      message: e?.response?.data?.detail || "Could not load accounts/transactions",
    });
  }
});

function amountColor(v) {
  const n = Number(v || 0);
  return n >= 0 ? "var(--good)" : "var(--bad)";
}
</script>

<template>
  <div class="col">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:12px; flex-wrap:wrap;">
      <div>
        <div class="h1">Računi & povijest</div>
        <div class="muted" style="font-size:13px;">
          Odaberi račun i pregledaj transakcije. Filtriranje po datumu radi na klijentu.
        </div>
      </div>

      <div style="min-width:320px;" class="col">
        <label>Odabrani račun</label>
        <select class="select" v-model="selectedAccountId">
          <option v-for="a in accounts" :key="a.account_id" :value="a.account_id">
            {{ a.name }} — {{ a.iban }}
          </option>
        </select>
      </div>
    </div>

    <div class="row wrap" style="margin-top:12px;">
      <div class="kpi" style="flex:1; min-width:240px;">
        <div class="muted">Stanje (EUR)</div>
        <div class="big">{{ centsToEur(balanceCents) }}</div>
        <div class="pill">
          <span>IBAN:</span>
          <span style="font-family: monospace;">{{ selectedAccount?.iban || "-" }}</span>
        </div>
      </div>

      <div class="kpi" style="flex:1; min-width:240px;">
        <div class="muted">Primanja u filteru</div>
        <div class="big" style="color:var(--good);">{{ centsToEur(incomeCents) }}</div>
        <div class="muted" style="font-size:12px;">Pozitivne stavke</div>
      </div>

      <div class="kpi" style="flex:1; min-width:240px;">
        <div class="muted">Izdaci u filteru</div>
        <div class="big" style="color:var(--bad);">{{ centsToEur(outcomeCents) }}</div>
        <div class="muted" style="font-size:12px;">Negativne stavke</div>
      </div>
    </div>

    <div class="card" style="padding:14px; margin-top:10px;">
      <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:12px; flex-wrap:wrap;">
        <div class="h2" style="margin:0;">Transakcije</div>

        <div class="row wrap" style="align-items:flex-end;">
          <div class="col" style="gap:6px;">
            <label>Od</label>
            <input class="input" type="date" v-model="dateFrom" />
          </div>
          <div class="col" style="gap:6px;">
            <label>Do</label>
            <input class="input" type="date" v-model="dateTo" />
          </div>
          <button class="btn" @click="dateFrom=''; dateTo='';">Reset</button>
        </div>
      </div>

      <div v-if="loading" class="muted" style="margin-top:10px;">Učitavanje...</div>

      <div style="margin-top:10px; overflow:auto;">
        <table class="table">
          <thead>
            <tr>
              <th>Vrijeme</th>
              <th>Tip</th>
              <th>Iznos</th>
              <th>Poziv na broj</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tx in filteredHistory" :key="tx.SK || tx.created_at">
              <td style="white-space:nowrap;">{{ tx.created_at || tx.SK }}</td>
              <td>{{ tx.type || tx.kind || "TX" }}</td>
              <td :style="{ color: amountColor(tx.amount_cents) }">
                {{ centsToEur(tx.amount_cents || 0) }} EUR
              </td>
              <td style="font-family: monospace;">{{ tx.reference || "" }}</td>
            </tr>

            <tr v-if="!loading && !filteredHistory.length">
              <td colspan="4" class="muted">Nema transakcija.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>