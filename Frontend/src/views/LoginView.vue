<script setup>
import {ref} from "vue";
import {http} from "../api/http";
import {useToasts} from "../stores/toasts";

const toast = useToasts();

const username = ref("");
const password = ref("");
const loading = ref(false);

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

async function login() {
  loading.value = true;
  try {
    const res = await http.post("/auth/login", {
      username: username.value,
      password: password.value,
    });
    sessionStorage.setItem("token", res.data.access_token);
    sessionStorage.setItem("user_id", res.data.user_id);

    toast.push({ type: "success", title: "Welcome", message: "Login successful." });
    window.location.href = "/accounts";
  } catch (e) {
    toast.push({
      type: "error",
      title: "Login failed",
      message: e?.response?.data?.detail || "Invalid credentials",
    });
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="container" style="display:flex; justify-content:center; align-items:center; min-height:100vh;">
    <div class="panel" style="width:420px; padding:18px;">
      <div style="display:flex; flex-direction:column; gap:6px;">
        <div style="font-size:20px; font-weight:800;">Sign in</div>
        <div class="muted" style="font-size:13px;">Use your credentials</div>
      </div>

      <hr class="sep" />

      <div class="col" style="gap:10px;">
        <div class="col" style="gap:6px;">
          <label>Username</label>
          <input class="input" v-model="username" />
        </div>

        <div class="col" style="gap:6px;">
          <label>Password</label>
          <input class="input" type="password" v-model="password" />
        </div>

        <button class="btn btn-primary" :disabled="loading" @click="login">
          {{ loading ? "Signing in..." : "Login" }}
        </button>

        <div class="muted" style="font-size:12px;">
          API: <span style="font-family:monospace;">{{ apiBaseUrl }}</span>
        </div>
      </div>
    </div>
  </div>
</template>