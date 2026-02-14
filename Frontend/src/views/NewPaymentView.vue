<script setup>
import {onMounted, ref, computed} from "vue";
import {http} from "../api/http";
import {eurToCents} from "../utils/money";
import {useToasts} from "../stores/toasts";

const toast = useToasts();

const accounts = ref([]);
const fromAccountId = ref("");
const toIban = ref("");
const payeeName = ref("");
const amountEur = ref("");
const reference = ref("");
const loading = ref(false);

const canSubmit = computed(() => {
  return (
    fromAccountId.value &&
    toIban.value.trim().length >= 10 &&
    payeeName.value.trim().length >= 2 &&
    String(amountEur.value || "").trim().length > 0
  );
});

async function loadAccounts() {
  const res = await http.get("/accounts/");
  accounts.value = res.data || [];
  if (!fromAccountId.value && accounts.value.length)
    fromAccountId.value = accounts.value[0].account_id;
}

function newIdempotencyKey() {
  return crypto.randomUUID();
}

async function submit() {
  if (!canSubmit.value) {
    toast.push({ type: "error", title: "Invalid", message: "Provjeri polja." });
    return;
  }

  loading.value = true;
  try {
    const body = {
      from_account_id: fromAccountId.value,
      to_iban: toIban.value,
      payee_name: payeeName.value,
      amount_cents: eurToCents(amountEur.value),
      idempotency_key: newIdempotencyKey(),
      reference: reference.value || null,
    };

    await http.post("/payments/", body);

    toast.push({ type: "success", title: "Success", message: "Plaćanje poslano." });

    toIban.value = "";
    payeeName.value = "";
    amountEur.value = "";
    reference.value = "";
  } catch (e) {
    toast.push({
      type: "error",
      title: "Payment failed",
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
      <div class="h1">Novo plaćanje</div>
      <div class="muted" style="font-size:13px;">
        Unesi IBAN, naziv primatelja i iznos.
      </div>
    </div>

    <div class="card" style="padding:16px;">
      <div class="row wrap">
        <div class="col" style="flex:1; min-width:280px;">
          <label>S kojeg računa</label>
          <select class="select" v-model="fromAccountId">
            <option v-for="a in accounts" :key="a.account_id" :value="a.account_id">
              {{ a.name }} — {{ a.iban }}
            </option>
          </select>
        </div>

        <div class="col" style="flex:1; min-width:280px;">
          <label>Iznos (EUR)</label>
          <input class="input" v-model="amountEur" placeholder="npr. 12.34" />
        </div>
      </div>

      <div class="row wrap" style="margin-top:12px;">
        <div class="col" style="flex:1; min-width:280px;">
          <label>IBAN primatelja</label>
          <input class="input" v-model="toIban" placeholder="HR..." />
        </div>

        <div class="col" style="flex:1; min-width:280px;">
          <label>Naziv primatelja</label>
          <input class="input" v-model="payeeName" placeholder="npr. HEP" />
        </div>
      </div>

      <div class="row wrap" style="margin-top:12px;">
        <div class="col" style="flex:1; min-width:280px;">
          <label>Poziv na broj (optional)</label>
          <input class="input" v-model="reference" placeholder="npr. HR00-12345" />
        </div>

        <div class="col" style="flex:1; min-width:280px; justify-content:flex-end;">
          <button class="btn btn-primary" :disabled="loading" @click="submit" style="width:100%;">
            {{ loading ? "Slanje..." : "Plati" }}
          </button>
        </div>
      </div>

      <div class="muted" style="font-size:12px; margin-top:10px;">
        Napomena: backend provjerava podudaranje IBAN + naziv primatelja.
      </div>
    </div>
  </div>
</template>