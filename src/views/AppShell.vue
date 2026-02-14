<script setup>
import ToastHost from "../components/ToastHost.vue";

function logout() {
  sessionStorage.removeItem("token");
  sessionStorage.removeItem("user_id");
  window.location.href = "/login";
}
</script>

<template>
  <ToastHost />

  <div style="min-height:100vh;">
    <div class="container">
      <div class="panel" style="display:flex; overflow:hidden;">
        <aside style="width:260px; padding:18px; border-right:1px solid var(--border); background:rgba(0,0,0,0.10);">
          <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:16px;">
            <div style="font-weight:800; letter-spacing:.4px;">Banking App</div>
            <div class="muted" style="font-size:12px;">Microservices demo</div>
          </div>

          <nav class="col" style="gap:10px;">
            <router-link class="btn" to="/accounts">Dashboard / Računi</router-link>
            <router-link class="btn" to="/payments/new">Novo plaćanje</router-link>
            <router-link class="btn" to="/transfers/internal">Prijenos (moji računi)</router-link>
          </nav>

          <hr class="sep" />

          <button class="btn btn-danger" style="width:100%;" @click="logout">Logout</button>

          <div class="muted" style="font-size:12px; margin-top:14px;">
            Currency: EUR
          </div>
        </aside>

        <main style="flex:1; padding:18px;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:14px;">
            <div>
              <div style="font-size:18px; font-weight:800;">Digital Banking</div>
              <div class="muted" style="font-size:12px;">Accounts • Transactions • Payments</div>
            </div>
          </div>

          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>