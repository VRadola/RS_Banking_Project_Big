<script setup>
import {onMounted, ref, computed} from "vue";
import {http} from "../api/http";
import {eurToCents} from "../utils/money";
import {useToasts} from "../stores/toasts";

const toast = useToasts();

const accounts = ref([]);
const fromAccountId = ref("");
const toAccountId = ref("");
const amountEur = ref("");
const loading = ref(false);

const canSubmit = computed(() => {
  return (
    fromAccountId.value &&
    toAccountId.value &&
    fromAccountId.value !== toAccountId.value &&
    String(amountEur.value || "").trim().length > 0
  );
});

async function loadAccounts() {
  const res = await http.get("/accounts/");
  accounts.value = res.data || [];
  if (accounts.value.length) {
    fromAccountId.value ||= accounts.value[0].account_id;
    toAccountId.value ||= accounts.value[0].account_id;
  }
}

function newIdempotencyKey() {
  return crypto.randomUUID();
}

async function submit() {
  if (!canSubmit.value) {
    toast.push({ type: "error", title: "Invalid", message: "Provjeri odabrane račune i iznos." });
    return;
  }

  loading.value = true;
  try {
    await http.post("/transactions/transfer", {
      from_account_id: fromAccountId.value,
      to_account_id: toAccountId.value,
      amount_cents: eurToCents(amountEur.value),
      idempotency_key: newIdempotencyKey(),
    });

    toast.push({ type: "success", title: "Success", message: "Prijenos izvršen." });
    amountEur.value = "";
  } catch (e) {
    toast.push({
      type: "error",
      title: "Transfer failed",
      message: e?.response?.data?.detail || e?.message || "Error",
    });
  } finally {
    loading.value = false;
  }
}

onMounted(loadAccounts);
</script>

<template>
  <div class="col" style="max-width:820px;">
    <div>
      <div class="h1">Prijenos između vlastitih računa</div>
      <div class="muted" style="font-size:13px;">
        Transfer sa jednog tvog računa na drugi.
      </div>
    </div>

    <div class="card" style="padding:16px;">
      <div class="row wrap">
        <div class="col" style="flex:1; min-width:280px;">
          <label>S računa</label>
          <select class="select" v-model="fromAccountId">
            <option v-for="a in accounts" :key="a.account_id" :value="a.account_id">
              {{ a.name }} — {{ a.iban }}
            </option>
          </select>
        </div>

        <div class="col" style="flex:1; min-width:280px;">
          <label>Na račun</label>
          <select class="select" v-model="toAccountId">
            <option v-for="a in accounts" :key="a.account_id" :value="a.account_id">
              {{ a.name }} — {{ a.iban }}
            </option>
          </select>
        </div>
      </div>

      <div class="row wrap" style="margin-top:12px;">
        <div class="col" style="flex:1; min-width:280px;">
          <label>Iznos (EUR)</label>
          <input class="input" v-model="amountEur" placeholder="npr. 25.00" />
        </div>

        <div class="col" style="flex:1; min-width:280px; justify-content:flex-end;">
          <button class="btn btn-primary" :disabled="loading" @click="submit" style="width:100%;">
            {{ loading ? "Slanje..." : "Prenesi" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>